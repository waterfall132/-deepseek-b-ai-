# -*- coding: UTF-8 -*-
import requests
import json
from time import sleep
import pandas as pd
from collections import deque
from openai import OpenAI
import datetime
import csv
import os
from datetime import datetime

class DanmakuBuffer:
    def __init__(self):
        self.buffer = []  # 存储弹幕
        self.csv_filename = f"violations_{datetime.now().strftime('%Y%m%d')}.csv"
        self.violation_records = []  # 存储违规记录
        self.client = OpenAI(api_key="换你自己的", base_url="换网址")

    def add_danmaku(self, msg):
        """添加弹幕到缓冲区"""
        danmaku = {
            'uid': msg['uid'],
            'nickname': msg['nickname'],
            'content': msg['text'],
            'timestamp': msg['timeline'] if 'timeline' in msg else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.buffer.append(danmaku)

        # 当累积50条弹幕时进行检查
        if len(self.buffer) >= 50:
            self.check_danmaku()
            self.buffer = []  # 清空缓冲区

    def check_danmaku(self):
        """检查弹幕内容"""
        if not self.buffer:
            return

        # 组合弹幕内容
        combined_text = "\n".join([f"用户{d['nickname']},uid{d['uid']}说：{d['content']}" for d in self.buffer])

        try:
            response = self.client.chat.completions.create(
                model="deepseek-v3",
                messages=[
                    {"role": "system",
                     "content": "你是一个严格的内容审核助手，请帮我检查以下直播弹幕是否包含明显违规内容（包括攻击性、侮辱性、违法、色情等），如果发现违规内容，请返回违规用户的昵称,uid和具体违规内容,类似：点关注，看动态置顶，今天抽礼物这种不属于攻击性言论属于正常宣传。"},
                    {"role": "user", "content": combined_text}
                ],
                stream=False
            )

            result = response.choices[0].message.content
            self.process_violations(result)

        except Exception as e:
            print(f"AI检查出错: {e}")

    def initialize_csv(self):
        """初始化CSV文件，如果不存在则创建并写入表头"""
        file_exists = os.path.isfile(self.csv_filename)

        with open(self.csv_filename, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['timestamp', 'uid', 'nickname', 'content', 'violation_type'])
            if not file_exists:
                writer.writeheader()

    def write_violation_to_csv(self, violation):
        """将单条违规记录写入CSV文件"""
        try:
            with open(self.csv_filename, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'uid', 'nickname', 'content', 'violation_type'])
                writer.writerow(violation)
            print(f"违规记录已写入文件: {self.csv_filename}")
        except Exception as e:
            print(f"写入CSV文件时出错: {e}")

    def determine_violation_type(self, ai_result):
        """根据AI返回结果判断违规类型"""
        if "攻击" in ai_result:
            return "攻击性言论"
        elif "侮辱" in ai_result:
            return "侮辱性言论"
        elif "色情" in ai_result:
            return "色情内容"
        elif "违法" in ai_result:
            return "违法内容"
        else:
            return "其他违规"

    def process_violations(self, ai_result):
        """处理违规内容"""
        try:
            # 这里假设AI返回的是文本描述
            if "违规" in ai_result:
                for danmaku in self.buffer:
                    if danmaku['content'] in ai_result:
                        # 创建违规记录
                        violation = {
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'uid': danmaku['uid'],
                            'nickname': danmaku['nickname'],
                            'content': danmaku['content'],
                            'violation_type': self.determine_violation_type(ai_result)  # 根据AI返回结果判断违规类型
                        }

                        # 打印违规信息
                        print(f"发现违规内容: {violation}")

                        # 实时写入CSV文件
                        self.write_violation_to_csv(violation)
        except Exception as e:
            print(f"处理违规内容时出错: {e}")

    def save_violations(self):
        """保存违规记录到Excel"""
        if self.violation_records:
            df = pd.DataFrame(self.violation_records)
            filename = f"violations_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            df.to_excel(filename, index=False)
            print(f"违规记录已保存到: {filename}")


def parse_danmaku(data, danmaku_buffer):
    """解析弹幕数据"""
    # 处理admin列表中的弹幕
    if 'admin' in data:
        for msg in data['admin']:
            print(f"UID: {msg['uid']}")
            print(f"用户主页url链接: https://space.bilibili.com/{msg['uid']}")
            name=msg['nickname']
            name = name.encode('gbk', errors='ignore').decode('gbk')
            print(f"昵称: {name}")
            content = msg['text']
            content = content.encode('gbk', errors='ignore').decode('gbk')
            print(f"弹幕内容: {content}")
            print("-" * 50)
            danmaku_buffer.add_danmaku(msg)

    # 处理room列表中的弹幕
    if 'room' in data:
        for msg in data['room']:
            print(f"UID: {msg['uid']}")
            name=msg['nickname']
            name = name.encode('gbk', errors='ignore').decode('gbk')
            print(f"昵称: {name}")
            content=msg['text']
            content=content.encode('gbk', errors='ignore').decode('gbk')
            print(f"弹幕内容: {content}")
            print("-" * 50)
            danmaku_buffer.add_danmaku(msg)



def get_bilibili_danmaku(room_id, danmaku_buffer):
    """获取B站直播间弹幕"""
    url = f'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'

    params = {
        'roomid': room_id,
        'room_type': 0
    }

    headers = {
        'authority': 'api.live.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7',
        'origin': 'https://live.bilibili.com',
        'referer': f'https://live.bilibili.com/{room_id}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...换你自己的'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        if data['code'] == 0:
            parse_danmaku(data['data'], danmaku_buffer)
        else:
            print(f"请求失败: {data['message']}")

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except KeyError as e:
        print(f"数据结构错误: {e}")


def main():
    room_id = "1977214140"  # 直播间ID
    danmaku_buffer = DanmakuBuffer()

    try:
        while True:
            print("\n获取最新弹幕...")
            get_bilibili_danmaku(room_id, danmaku_buffer)
            sleep(5)  # 每5秒更新一次
    except KeyboardInterrupt:
        print("\n程序结束，保存违规记录...")
        danmaku_buffer.save_violations()


if __name__ == "__main__":
    main()
