# Core Minimalism 设计系统

## 核心原则

> **Less is More** - 通过去除一切非必要元素，让内容成为主角

---

## 1. 色彩系统 - 极致克制

### 配色原则
- **5色法则**: 主色、背景、文字、次要文字、边框
- **低饱和度**: 避免鲜艳色彩，用中性色调
- **高对比度**: 确保文字清晰可读（WCAG AA 标准）

### 基础色彩变量模板
```css
:root {
    --bg-primary: #FAFAFA;      /* 主背景 */
    --bg-card: #FFFFFF;          /* 卡片背景 */
    --text-primary: #111111;     /* 主要文字 */
    --text-secondary: #666666;   /* 次要文字 */
    --border: #E0E0E0;           /* 边框 */
}
```

---

## 2. 字体系统 - 系统原生

### 字体选择
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
```

### 字重层级
| 用途 | 字重 | 示例 |
|------|------|------|
| 大标题 | 300 / Light | 奇点前沿 |
| 小标题 | 600 / SemiBold | 新闻标题 |
| 正文 | 400 / Regular | 新闻摘要 |
| 次要文字 | 400 / Regular | 时间戳 |
| 微文字（标签） | 600 / Semi-Bold | 来源标识 |

### 字号比例
- 大标题: 24px
- 导航/小标题: 14-16px
- 正文: 14-16px
- 次要/微文字: 11-13px

---

## 3. 间距系统 - 24px 倍数

```css
:root {
    --spacing-xs: 24px;    /* 卡片内边距、小间距 */
    --spacing-md: 48px;    /* 区块间距 */
    --spacing-lg: 96px;    /* 大区块间距 */
}
```

### 应用规则
- 卡片内边距: `var(--spacing-xs)` = 24px
- 卡片间距: 20-24px
- 区块顶部间距: `var(--spacing-md)` = 48px
- 容器左右边距: `var(--spacing-xs)` = 24px

---

## 4. 卡片设计 - 去装饰化

### 基础卡片样式
```css
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;          /* 极小圆角或 0 */
    padding: var(--spacing-xs);
    transition: border-color 0.2s ease;  /* 只变边框色 */
}

.card:hover {
    border-color: var(--text-primary);  /* hover 时边框变深 */
}
```

### 禁用元素
- ❌ 复杂阴影 (box-shadow)
- ❌ 大圆角 (border-radius > 4px)
- ❌ 渐变背景
- ❌ 发光效果
- ❌ 复杂动画

### 允许元素
- ✅ 1px 纯色边框
- ✅ 0.2s 快速过渡
- ✅ 边框颜色变化

---

## 5. 导航 - 固定 + 毛玻璃

```css
.header {
    position: sticky;
    top: 0;
    background: rgba(250, 250, 250, 0.9);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
    height: 72px;
}
```

### 导航链接
```css
.nav a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.2s ease;
}

.nav a:hover {
    color: var(--text-primary);
}
```

---

## 6. 版式 - 大留白

### 容器
```css
.container {
    max-width: 1200px;  /* 或 1400px */
    margin: 0 auto;
    padding: 0 var(--spacing-xs);
}
```

### 区块间距
- Hero 区块: `padding: var(--spacing-lg) 0` = 96px
- 内容区块: `padding: var(--spacing-md) 0` = 48px

---

## 7. 动画 - 极速过渡

```css
/* 标准过渡 */
transition: border-color 0.2s ease;
transition: color 0.2s ease;

/* 禁用复杂动画 */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition-duration: 0.01ms !important;
    }
}
```

---

## 8. 响应式断点

```css
/* 平板 */
@media (max-width: 1024px) {
    :root {
        --spacing-xs: 20px;
        --spacing-md: 40px;
        --spacing-lg: 64px;
    }
}

/* 手机 */
@media (max-width: 768px) {
    :root {
        --spacing-xs: 16px;
        --spacing-md: 32px;
        --spacing-lg: 48px;
    }
}
```

---

## 9. 组件规范

### 按钮
```css
.btn {
    border: 1px solid var(--border);
    background: transparent;
    padding: 8px 20px;
    font-size: 14px;
    font-weight: 400;
    transition: border-color 0.2s ease;
}

.btn:hover {
    border-color: var(--text-primary);
}
```

### 标签
```css
.tag {
    font-size: 11px;
    font-weight: 600;
    padding: 4px 12px;
    border: 1px solid var(--border);
    letter-spacing: 0.05em;
}
```

### 新闻卡片
```css
.news-card {
    padding: var(--spacing-xs);
    border: 1px solid var(--border);
}

.news-source {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
}

.news-title {
    font-size: 18px;
    font-weight: 400;
    color: var(--text-primary);
    margin-bottom: 8px;
}

.news-summary {
    font-size: 14px;
    font-weight: 400;
    color: var(--text-secondary);
}
```

---

## 10. 检查清单

设计完成前，确认：

- [ ] 只使用 5 种以内的颜色
- [ ] 无复杂阴影和发光效果
- [ ] 无外部字体加载
- [ ] 圆角 ≤ 4px
- [ ] 所有动画 ≤ 0.2s
- [ ] 间距遵循 24px 倍数
- [ ] 过渡只改变 border-color 或 color
- [ ] 有足够的留白空间
- [ ] 文字对比度 ≥ 4.5:1

---

## 应用到奇点前沿的改动建议

| 当前元素 | 极简风格改造 |
|---------|-------------|
| 霓虹色 #00F5FF、#FF00FF | 改为单色系统 |
| Rain/Scan 动画 | 完全移除 |
| 发光效果 (glow) | 完全移除 |
| Orbitron/Exo 2 字体 | 改用系统字体 |
| 12px 圆角 | 改为 4px |
| 毛玻璃卡片 | 改用纯色卡片 |
| 0.3s 过渡 | 改为 0.2s |
| transform 移位动画 | 改为只变边框色 |
