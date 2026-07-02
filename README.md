# 中国近代史刷题 SPA

基于 Vite + React + TypeScript + Tailwind CSS 构建的现代化本地刷题单页应用。

## 功能特性

- 📚 **199道选择题** — 涵盖中国近代史全部考点（鸦片战争至改革开放）
- ✅ **即时反馈** — 选择答案后立即显示正误与详细解析
- 📊 **进度追踪** — 顶部进度条 + 题目网格导航（绿色=正确，红色=错误）
- 🔄 **错题复习** — 完成所有题目后可专门复习错题
- 💾 **本地持久化** — 使用 localStorage 保存进度，刷新不丢失
- 🌙 **深色模式** — 支持明暗主题切换
- 🎨 **现代化 UI** — Shadcn/UI 风格卡片设计

## 技术栈

| 技术 | 用途 |
|------|------|
| Vite | 构建工具 |
| React 18 | 前端框架 |
| TypeScript | 类型安全 |
| Tailwind CSS | 样式框架 |
| localStorage | 本地数据持久化 |

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 项目结构

```
quiz-app/
├── scripts/           # 数据处理脚本
│   ├── parse_pdf.py   # PDF 解析
│   └── fix_*.py       # OCR 文字修复
├── src/
│   ├── data/          # 题目 JSON 数据
│   ├── types/         # TypeScript 类型
│   ├── hooks/         # React Hooks (状态管理)
│   ├── components/    # UI 组件
│   └── App.tsx        # 主应用
└── package.json
```

## 数据来源

题目数据来自《中国近代史期末复习资料》（共199题），通过 Python 脚本从 PDF 提取并清洗。
