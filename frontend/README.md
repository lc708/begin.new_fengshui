# 风水命理大师 - 前端应用

一个基于 Next.js 和 React 构建的现代化风水命理应用前端。

## 🌟 特性

- **响应式设计** - 完美适配桌面端和移动端
- **传统中式风格** - 采用红、金、黑传统配色方案
- **现代化框架** - 基于 Next.js 14 + React 18 + TypeScript
- **优雅的UI组件** - 自定义的传统风格组件库
- **交互式罗盘** - 数字化风水罗盘功能

## 🚀 快速开始

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本

```bash
npm run build
npm start
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── components/          # 可复用组件
│   │   ├── Hero.tsx        # 首页头部组件
│   │   ├── NavigationCard.tsx  # 导航卡片
│   │   ├── BirthInfoForm.tsx   # 生辰信息表单
│   │   └── DigitalCompass.tsx  # 数字风水罗盘
│   ├── pages/              # 页面组件
│   │   ├── index.tsx       # 首页
│   │   ├── bazi.tsx        # 八字分析页
│   │   ├── fengshui.tsx    # 风水罗盘页
│   │   └── daily.tsx       # 每日宜忌页
│   └── styles/             # 样式文件
│       └── globals.css     # 全局样式
├── public/                 # 静态资源
├── package.json           # 项目配置
└── tailwind.config.js     # Tailwind CSS 配置
```

## 🎨 设计系统

### 颜色主题

- **主色调**: 深红色 (#8B0000)
- **辅助色**: 金色 (#FFD700)  
- **强调色**: 黑色 (#000000)
- **背景色**: 米色 (#FFF8DC)
- **文字色**: 深灰绿 (#2F4F4F)

### 字体

- **标题**: Noto Serif SC (思源宋体)
- **正文**: Noto Sans SC (思源黑体)

### 组件样式

- **卡片**: `.traditional-card` - 圆角、阴影、金色边框
- **按钮**: `.traditional-button` - 红底金字、悬停效果
- **输入框**: `.traditional-input` - 金色边框、聚焦时红色边框

## 🔧 技术栈

- **框架**: Next.js 14
- **语言**: TypeScript
- **样式**: Tailwind CSS 3
- **图标**: Lucide React
- **状态管理**: Zustand (可选)
- **HTTP客户端**: Axios

## 📱 页面功能

### 首页 (/)
- 传统风格英雄头部
- 三大功能模块导航
- 响应式卡片布局

### 八字分析 (/bazi)
- 生辰信息录入表单
- 八字计算和展示
- 五行分析图表
- 性格特点解读

### 风水罗盘 (/fengshui)
- 交互式数字罗盘
- 八方位选择功能
- 方位建议展示
- 通用风水指导

### 每日宜忌 (/daily)
- 当日运势概览
- 宜忌事项展示
- 详细时辰信息
- 温馨提示功能

## 🌐 API 集成

前端预留了与后端 API 的集成接口：

- `POST /api/bazi/analyze` - 八字分析
- `POST /api/fengshui/advice` - 风水建议  
- `GET /api/daily/fortune` - 每日运势

## 📱 响应式设计

- **移动端**: 320px - 768px
- **平板端**: 768px - 1024px  
- **桌面端**: 1024px+

所有组件都经过精心设计以确保在不同设备上的最佳体验。

## 🔮 特色功能

### 数字风水罗盘
- 八方位可点击选择
- 实时方位建议显示
- 五行元素对应
- 传统文化元素融入

### 智能表单验证
- 实时输入验证
- 友好错误提示
- 数据格式校验

### 加载动画
- 优雅的加载效果
- 传统元素动画
- 用户体验优化

## 🚧 开发说明

### 环境要求
- Node.js 18+
- npm 或 yarn

### 代码规范
- TypeScript 严格模式
- ESLint 代码检查
- Prettier 代码格式化

### 构建优化
- 自动代码分割
- 图片优化
- CSS 压缩

## 📄 许可证

本项目仅供学习和演示使用。

---

🏮 传承千年智慧，服务现代生活 🏮
