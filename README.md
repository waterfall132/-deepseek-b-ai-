# -deepseek-b-ai-
这是一个用于监控B站直播弹幕并进行实时内容审核的Python程序。系统能够自动抓取直播间弹幕，使用AI模型例如deepseek-v3/R1进行内容审核，并将违规内容记录到CSV文件中。
# B站直播弹幕监控与违规内容检测系统


## 功能特点
- 实时抓取B站直播弹幕
- 支持AI智能内容审核
- 违规内容实时记录
- CSV格式数据存储
- 完整的异常处理机制

## 系统架构
### 主要组件
1. **弹幕抓取模块**
   - 负责与B站API交互
   - 实时获取直播间弹幕数据
   - 支持自定义抓取间隔

2. **内容审核模块**
   - 集成OpenAI API
   - 智能识别违规内容
   - 支持多种违规类型判断

3. **数据存储模块**
   - CSV格式数据存储
   - 实时写入违规记录
   - 按日期自动分文件存储

## 安装说明
### 环境要求
- Python 3.7+
- 必要的Python包：
```bash
pip install requests pandas openai
```

### 配置说明
1. OpenAI API配置
```python
client = OpenAI(api_key="your_api_key", base_url="https://twohornedcarp.com/v1")这里替换成官方的openai key或者Deepseek官方api key以及url
```

2. 直播间配置
```python
room_id = "your_room_id"  # 替换为目标直播间ID
```
3.user-agent配置
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...换成你自己的


## 使用说明
### 基本使用
1. 运行程序
```bash
python danmaku_monitor.py
```

2. 停止程序
```
使用 Ctrl+C 终止程序运行
```

### 数据格式
CSV文件包含以下字段：
- timestamp: 违规时间
- uid: 用户ID
- nickname: 用户昵称
- content: 违规内容
- violation_type: 违规类型

### 违规类型
当前支持的违规类型包括：
- 攻击性言论
- 侮辱性言论
- 色情内容
- 违法内容
- 其他违规

## 代码结构
```
danmaku_monitor/
├── danmaku_monitor.py    # 主程序
├── requirements.txt      # 依赖包列表
└── violations/          # 违规记录存储目录
    └── violations_YYYYMMDD.csv
```


## 注意事项
1. API密钥安全
   - 请妥善保管OpenAI API密钥
   - 建议使用环境变量存储敏感信息

2. 数据存储
   - 定期备份违规记录
   - 注意磁盘空间使用情况

3. 异常处理
   - 程序包含完整的错误处理机制
   - 建议定期检查日志信息

## 更新日志
### v1.0.0 (2024-02-10)
- 初始版本发布
- 实现基本功能
- 支持CSV格式数据存储

## 待优化功能
1. 数据库支持
   - 添加SQLite/MySQL支持
   - 优化数据存储结构

2. 用户界面
   - 添加Web管理界面
   - 实现可视化数据展示

3. 审核能力
   - 扩展违规类型
   - 优化AI模型提示词

## 贡献指南
欢迎提交Issue和Pull Request来改进项目。

## 许可证
Apache2.0 License
禁止用作者的名号进行商业广告,原作者仅用于学术研究收集不合规弹幕用途。
原作者不承担代码使用后风险。

## 联系方式
- 项目维护者：waterfall132


## 致谢
感谢使用本项目，如有问题或建议，欢迎反馈。

---

