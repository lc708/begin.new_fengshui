# 🚀 部署准备检查清单

## 📋 Railway 后端部署

### 必需文件
- ✅ `requirements.txt` - Python依赖
- ✅ `backend_api.py` - 主应用文件
- ✅ `railway.json` - Railway配置
- ✅ `Procfile` - 启动命令
- ✅ `runtime.txt` - Python版本

### 环境变量设置（在Railway项目中配置）
```bash
# LLM API密钥（至少设置一个）
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key  
DEEPSEEK_API_KEY=your_deepseek_api_key

# LLM提供商（可选，默认openai）
LLM_PROVIDER=openai

# Flask环境
FLASK_ENV=production
```

### Railway自动设置的变量
- `PORT` - Railway自动分配端口
- `RAILWAY_ENVIRONMENT=production`

---

## 🌐 Vercel 前端部署

### 必需文件
- ✅ `frontend/package.json` - 项目配置
- ✅ `frontend/vercel.json` - Vercel配置
- ✅ `frontend/next.config.js` - Next.js配置

### 环境变量设置（在Vercel项目中配置）
```bash
# API地址（部署后端后获得）
NEXT_PUBLIC_API_URL=https://your-railway-domain.railway.app
```

---

## 🔗 部署顺序

1. **先部署后端到Railway**
   - 获得Railway分配的域名
   - 测试API接口是否正常

2. **再部署前端到Vercel**
   - 设置`NEXT_PUBLIC_API_URL`为Railway域名
   - 测试前后端连接

---

## ✅ 部署验证

### 后端健康检查
- 访问: `https://your-domain.railway.app/api/health`
- 预期响应: `{"status":"healthy","message":"风水命理大师API服务运行正常"}`

### 前端功能验证
- 八字分析页面能正常提交和显示结果
- 风水罗盘点击方位有正确反应
- 每日运势显示真实数据而非mock数据

### API集成测试
- 所有前端页面都能正常调用后端API
- 没有CORS错误
- 响应时间在可接受范围内（<90秒）

---

## 🛠️ 生产环境优化

### 已包含的优化
- ✅ 90秒API超时适应LLM调用
- ✅ Railway PORT环境变量支持
- ✅ 生产环境错误处理
- ✅ CORS配置支持跨域
- ✅ 健康检查端点

### 性能监控
- Railway提供实时日志和指标
- Vercel提供访问分析和性能数据
- 可监控API响应时间和错误率
