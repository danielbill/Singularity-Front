# 奇点前沿首页 - 极简蓝紫主题设计

## 版本信息
- **版本**: v1.0
- **日期**: 2025-01-30
- **设计风格**: 极简主义 + 蓝紫主色调

---

## 1. 配色系统

### 基础色彩
```css
--bg-primary: #FAFAFA;      /* 主背景 - 极简白 */
--bg-card: #FFFFFF;          /* 卡片背景 - 纯白 */
--text-primary: #111111;     /* 主要文字 - 黑 */
--text-secondary: #666666;   /* 次要文字 - 灰 */
--text-muted: #999999;       /* 微文字 - 浅灰 */
--border: #E0E0E0;           /* 边框 - 浅灰 */
--border-hover: #111111;     /* hover 边框 - 黑 */
```

### 主色调系统
```css
--color-primary: #3b4274;           /* 主色 - 蓝紫 */
--color-primary-light: #5E66A3;      /* 浅色 - 次要强调 */
--color-primary-lighter: #E8E9F0;    /* 极浅 - 背景装饰 */
--color-primary-dark: #2A3057;       /* 深色 - hover/active */
```

### 应用规则
- **网站标题**: `var(--color-primary)` + `opacity: 0.25`
- **新闻标题**: `var(--color-primary)` (主色，不透明)
- **标签**: `background: var(--color-primary-lighter)` + `color: var(--color-primary)`

---

## 2. 字体系统

### 主字体
```css
font-family: 'Alibaba PuHuiTi', -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
```

### 字体引入
```html
<link href="https://puhuiti.oss-cn-hangzhou.aliyuncs.com/puhuiti.css" rel="stylesheet">
```

### 字号层级
| 用途 | 字号 | 字重 |
|------|------|------|
| 网站标题 | 56px | 350 |
| 新闻标题 | 17px | 400 |
| 潮流标题 | 16px | 400 |
| 导航 | 14px | 400 |
| 摘要 | 14px | 400 |
| 元数据 | 11-12px | 600 |

---

## 3. 间距系统

```css
--spacing-xs: 24px;    /* 小间距 - 卡片内边距 */
--spacing-md: 48px;    /* 中间距 - 区块间距 */
--spacing-lg: 96px;    /* 大间距 - 页面区块 */
```

---

## 4. Header 区域

### 结构
```
┌─────────────────────────────────────────────────────┐
│  [Tab区]     网站标题(居中)     [新闻|奇点|前沿|关于] │
└─────────────────────────────────────────────────────┘
```

### 规格
- **高度**: 120px
- **背景**: `rgba(250, 250, 250, 0.9)` + 毛玻璃 `backdrop-filter: blur(10px)`
- **对齐**: `align-items: flex-end` (底部对齐)

### 网站标题
```css
.site-title {
    flex: 1;
    text-align: center;
    font-size: 56px;
    font-weight: 350;
    color: var(--color-primary);
    letter-spacing: 20px;
    opacity: 0.25;
    padding-bottom: 20px;
}
```

### 导航
- **间距**: `calc(var(--spacing-xs) + 8px)` = 32px
- **左侧偏移**: `-30px`
- **激活态**: 颜色变黑 + 底部 2px 横线

---

## 5. 人物 Tab 区

### 规格
- **容器**: 300px × 120px
- **单个 Tab**: 180px × 120px
- **重叠间距**: 50px (130px - 80px)

### 扑克牌效果
```css
/* 第一个 */
.person-tab-wrapper:nth-child(1) {
    left: 0;
    z-index: 3;
    transform: scale(1);
}

/* 第二个 */
.person-tab-wrapper:nth-child(2) {
    left: 130px;
    z-index: 2;
    transform: scale(0.95);
}

/* 第三个 */
.person-tab-wrapper:nth-child(3) {
    left: 260px;
    z-index: 1;
    transform: scale(0.9);
}
```

### Tab 样式
```css
.person-tab {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: none;
    border-right: none;
}
```

---

## 6. 内容区域

### 布局
```css
.content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 var(--spacing-xs) var(--spacing-md);
    display: grid;
    grid-template-columns: 6fr 4fr;  /* 60% : 40% */
    gap: var(--spacing-md);
}
```

### 左侧时间线卡片
```css
.timeline-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 1px solid var(--border);
    border-radius: 0 0 4px 4px;
    padding: var(--spacing-xs);
}
```

### 时间线样式
- **圆点**: 5px 圆形，黑色
- **竖线**: 1px，浅灰
- **标题**: 主色调 `#3b4274`
- **标签**: 极浅蓝背景 + 主色文字

### 右侧潮流卡片
```css
.trending-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: var(--spacing-xs);
}
```

---

## 7. 动画规范

### 过渡时长
- **标准**: 0.2s
- **Tab 动画**: 0.3s cubic-bezier(0.4, 0, 0.2, 1)

### Hover 效果
- **卡片**: 边框颜色变黑
- **Tab**: scale(1.02)
- **导航**: 颜色变化

---

## 8. 响应式断点

### 平板 (≤1024px)
```css
.content {
    grid-template-columns: 1fr;
}
```

### 移动端 (≤768px)
```css
:root {
    --spacing-xs: 16px;
    --spacing-md: 32px;
    --spacing-lg: 64px;
}

.site-title {
    font-size: 20px;
    letter-spacing: 6px;
}

.nav {
    display: none;
}
```

---

## 9. HTML 结构模板

```html
<header class="header">
    <div class="header-content">
        <!-- 人物 Tab 区 -->
        <div class="person-tabs">
            <div class="person-tab-wrapper active">
                <div class="person-tab">
                    <img src="assets/images/people/xxx.png">
                </div>
            </div>
        </div>

        <!-- 网站标题 -->
        <h1 class="site-title">奇点前沿</h1>

        <!-- 导航 -->
        <nav class="nav">
            <a href="#" class="active">新 闻</a>
            <a href="#">奇 点</a>
            <a href="#">前 沿</a>
            <a href="#">关 于</a>
        </nav>
    </div>
</header>

<main class="content">
    <!-- 左侧时间线 -->
    <article class="timeline-card">
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <div class="timeline-meta">
                <span class="timeline-source">Reuters</span>
                <span class="timeline-separator">|</span>
                <time class="timeline-time">2小时前</time>
                <span class="timeline-tag">航天</span>
            </div>
            <h3 class="timeline-title">新闻标题</h3>
            <p class="timeline-summary">摘要内容...</p>
        </div>
    </article>

    <!-- 右侧潮流 -->
    <aside class="trending-list">
        <article class="trending-card">
            <h3 class="trending-title">潮流标题</h3>
            <p class="trending-summary">摘要...</p>
            <div class="trending-meta">
                <span class="trending-source">OpenAI</span>
                <span class="trending-tag">AI</span>
            </div>
        </article>
    </aside>
</main>
```

---

## 10. 关键文件
- **HTML**: `index.html`
- **设计文档**: `design/minimal-blue-theme.md`
