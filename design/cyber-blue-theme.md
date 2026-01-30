# Singularity Front - 赛博青蓝主题设计文档

## 版本信息
- **版本**: v1.0
- **日期**: 2026-01-30
- **文件**: `index-matrix-blue.html`
- **设计风格**: Cyberpunk Cyan + Matrix Terminal + IBM栅栏字体

---

## 1. 核心设计理念

### 视觉语言
- **风格定位**: 赛博青蓝 + 终端极简 + 微光玻璃态
- **参考**: 黑客帝国代码雨、IBM Plex设计系统、科幻终端界面
- **关键词**: 低调、精密、未来感、克制

### 设计原则
1. **极简克制** - 不使用过度动画，所有效果服务于可读性
2. **层次分明** - 通过透明度和模糊度建立视觉层级
3. **低对比度发光** - 发光效果微妙，不刺眼
4. **静态优先** - 背景网格固定，减少动态干扰

---

## 2. 配色系统

### 基础色彩
```css
--bg-primary: #05080F;              /* 主背景 - 接近纯黑 */
--bg-card: rgba(10, 15, 26, 0.8);   /* 卡片背景 - 半透明深蓝 */
```

### 青蓝主色调
```css
--color-accent: #00D9FF;            /* 赛博青蓝 - 主要强调色 */
--color-accent-dim: rgba(0, 217, 255, 0.2);
--color-accent-glow: rgba(0, 217, 255, 0.4);
--color-accent-dark: #4A9BAA;       /* 暗蓝色 - 导航、次要元素 */
```

### 文字层级
```css
--text-primary: #C0D8E8;            /* 主要文字 */
--text-secondary: #6B8A9A;          /* 次要文字 */
--text-muted: #4A6070;              /* 微弱文字 - 时间、元数据 */
```

### 边框与分隔
```css
--border: #1A2A35;                  /* 默认边框 */
--border-hover: #00D9FF;            /* hover边框 - 青蓝发光 */
```

### 应用规则
| 元素 | 颜色 | 透明度 |
|------|------|--------|
| 网站标题 | `--color-accent` | 0.45 |
| 新闻标题 | `--text-primary` | 1 |
| 导航链接 | `--color-accent-dark` | 1 |
| 时间线竖线 | `rgba(74, 155, 170, 0.4)` | 0.4 |
| 标签背景 | `rgba(74, 155, 170, 0.1)` | 0.1 |

---

## 3. 字体系统

### 引入方式
```html
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- 阿里巴巴普惠体 -->
<link href="https://puhuiti.oss-cn-hangzhou.aliyuncs.com/puhuiti.css" rel="stylesheet">
```

### 字体应用
| 用途 | 字体 | 字重 | 字号 |
|------|------|------|------|
| 网站标题 | Orbitron | 700 | 38px |
| 新闻标题 | Orbitron | 400 | 17px |
| 潮流标题 | Orbitron | 400 | 16px |
| 导航链接 | Orbitron | 600 | 16px |
| 正文 | Alibaba PuHuiTi | 400 | 14px |
| 元数据 | Alibaba PuHuiTi | 600 | 11-12px |

### IBM 栅栏字体效果
网站标题使用层叠阴影实现栅栏效果：
```css
.site-title {
    font-family: 'Orbitron', sans-serif;
    transform: skewX(-12deg);
    text-shadow:
        1px 1px 0 rgba(0, 217, 255, 0.15),
        2px 2px 0 rgba(0, 217, 255, 0.15),
        ...
        8px 8px 0 rgba(0, 217, 255, 0.10),
        0 0 16px rgba(0, 217, 255, 0.3);
}
```

---

## 4. 间距系统

```css
--spacing-xs: 24px;    /* 小间距 - 卡片内边距 */
--spacing-md: 48px;    /* 中间距 - 区块间距 */
--spacing-lg: 96px;    /* 大间距 - 页面区块 */
```

---

## 5. Header 区域

### 布局结构
```
┌─────────────────────────────────────────────────────┐
│  [网站Title]                    [导航: 新闻|奇点|前沿|关于] │
└─────────────────────────────────────────────────────┘
```

### 规格
- **高度**: 60px
- **背景**: `rgba(5, 8, 15, 0.9)` + 毛玻璃 `backdrop-filter: blur(10px)`
- **对齐**: `align-items: center`

### 网站标题
```css
.site-title {
    text-align: left;
    font-family: 'Orbitron', sans-serif;
    font-size: 38px;
    font-weight: 700;
    color: var(--color-accent);
    letter-spacing: 1px;
    opacity: 0.45;
    margin-left: 20px;
    transform: skewX(-12deg);
    /* IBM 栅栏层叠效果 */
}
```

### 导航栏
```css
.nav {
    margin-left: auto;
    margin-right: 20px;
    align-self: flex-end;
    padding-bottom: 8px;
    gap: 32px;
}

.nav a {
    font-family: 'Orbitron', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: var(--color-accent-dark);
    letter-spacing: 0.2em;
}

/* 选中 + hover 都有下划线 */
.nav a.active::after,
.nav a:hover::after {
    height: 2px;
    background: var(--color-accent);
    box-shadow: var(--glow-subtle);
}
```

---

## 6. 背景特效

### 静态透视网格
```css
body::before {
    background:
        linear-gradient(90deg, rgba(0, 217, 255, 0.02) 1px, transparent 1px),
        linear-gradient(rgba(0, 217, 255, 0.02) 1px, transparent 1px);
    background-size: 60px 60px;
    transform: perspective(500px) rotateX(75deg);
    transform-origin: center top;
}
```

### 极淡扫描线
```css
body::after {
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 0, 0, 0.015) 2px,
        rgba(0, 0, 0, 0.015) 4px
    );
    opacity: 0.5;
}
```

### 环境光晕
```css
.ambient-glow {
    width: 600px;
    height: 600px;
    filter: blur(150px);
    opacity: 0.03;
}
```

---

## 7. 内容区域

### 布局
```css
.content {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 6fr 4fr;  /* 60% : 40% */
    gap: var(--spacing-md);
}
```

### 时间线卡片
```css
.timeline-card {
    background: rgba(10, 15, 26, 0.85);
    border: 1px solid rgba(0, 217, 255, 0.2);
    box-shadow: 0 4px 30px rgba(0, 217, 255, 0.1);
    border-radius: 4px;
    padding: var(--spacing-xs);
}

/* 人物半透明背景 */
.timeline-card::before {
    content: '';
    background-image: url('assets/images/people/马斯克-1.png');
    background-size: contain;
    background-position: center top;
    opacity: 0.2;
}
```

### 潮流卡片
```css
.trending-card {
    background: rgba(10, 15, 26, 0.85);
    border: 1px solid rgba(0, 217, 255, 0.2);
    border-radius: 4px;
    padding: var(--spacing-xs);
    transition: all 0.2s ease;
}

.trending-card:hover {
    border-color: var(--color-accent);
    transform: translateY(-1px);
}
```

---

## 8. 组件细节

### 时间线竖线
```css
.timeline-item::before {
    width: 1px;
    background: rgba(74, 155, 170, 0.4);
}
```

### 时间线圆点
```css
.timeline-dot::after {
    width: 5px;
    height: 5px;
    background: var(--color-accent-dark);
    border-radius: 50%;
}
```

### 标签样式
```css
.timeline-tag,
.trending-tag {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border: 1px solid rgba(74, 155, 170, 0.3);
    background: rgba(74, 155, 170, 0.1);
    border-radius: 4px;
    color: var(--color-accent-dark);
    letter-spacing: 0.05em;
}
```

---

## 9. 动画规范

### 过渡时长
- **标准过渡**: 0.2s ease
- **标题 hover**: 0.3s ease

### Hover 效果
| 元素 | 效果 |
|------|------|
| 网站标题 | 栅栏层数增加 + 发光增强 |
| 导航链接 | 下划线 + 颜色变化 |
| 卡片 | 边框变青蓝 + Y轴-1px |
| 卡片背景 | 背景略微提亮 |

---

## 10. 响应式断点

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
}

.site-title {
    font-size: 20px;
}

.nav {
    display: none;  /* 或替换为汉堡菜单 */
}
```

---

## 11. 关键文件

| 文件 | 说明 |
|------|------|
| `index-matrix-blue.html` | 赛博青蓝主题页面 |
| `design/cyber-blue-theme.md` | 本设计文档 |

---

## 12. 设计亮点总结

1. **IBM 栅栏字体** - 使用多层 text-shadow 创造层叠效果，配合 skewX 斜切
2. **静态透视网格** - 75度旋转的透视网格，营造空间感但无动画干扰
3. **人物背景融合** - 半透明人物图片作为卡片背景，低调传达人物关联
4. **极淡扫描线** - 1.5% 透明度的扫描线，致敬CRT但不影响阅读
5. **克制发光** - 所有发光效果使用低透明度，避免过度赛博朋克
6. **暗蓝色导航** - 使用 `#4A9BAA` 而非亮色，保持低调
