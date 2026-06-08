# AI学习助手

> 面向小学到高中学生的AI智能学习助手小程序

## 功能特色

- 🤖 **AI问答** - 智能解答各学科问题
- 📝 **作业辅导** - 拍照上传，AI批改解析
- 📊 **学习进度** - 数据追踪，可视化成长
- 📚 **学科专项** - 系统学习，逐个突破

## 技术栈

### 前端
- 微信小程序原生框架
- 黑金古典UI风格

### 后端
- Flask API服务
- 支持多AI模型接入

## 项目结构

```
ai-study-assistant/
├── app.js              # 小程序入口
├── app.json            # 小程序配置
├── app.wxss            # 全局样式
├── pages/              # 页面目录
│   ├── index/          # 首页
│   ├── login/          # 登录
│   ├── chat/           # AI问答
│   ├── homework/       # 作业辅导
│   ├── progress/       # 学习进度
│   └── subject/        # 学科专项
├── backend/            # 后端API
│   ├── app.py          # Flask应用
│   └── requirements.txt
└── README.md
```

## 部署说明

### 1. 后端部署

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 2. 小程序配置

1. 用微信开发者工具打开项目
2. 修改 `app.js` 中的 `apiBaseUrl` 为你的服务器地址
3. 填入小程序 AppID

### 3. 服务器要求

- Python 3.8+
- HTTPS证书（小程序正式上线需要）
- 在小程序后台配置服务器域名

## API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/chat/message | POST | AI问答 |
| /api/homework/analyze | POST | 作业分析 |
| /api/progress/stats | GET | 学习统计 |
| /api/user/profile | GET | 用户信息 |

## 后续规划

- [ ] 接入大模型API
- [ ] 添加错题本功能
- [ ] 学习打卡激励
- [ ] 家长端数据同步

## License

MIT