# 新闻过滤模块技术规格

## 概述

新闻过滤模块负责根据配置的关键词筛选新闻文章，只保留与奇点人物、公司和话题相关的新闻。

## 配置文件

**路径**: `config/news_keywords.yaml`

### 配置结构

```yaml
# 人物关键词（按人物分组，仅用于管理，匹配仍是 OR）
people:
  musk:
    - "马斯克"
    - "埃隆·马斯克"
    - "Elon Musk"
    - "老马"

  huang:
    - "黄仁勋"
    - "Jensen Huang"
    - "老黄"
    - "皮衣刀客"

  altman:
    - "奥尔特曼"
    - "Sam Altman"
    - "萨姆·奥尔特曼"

# 公司关键词（按公司分组，仅用于管理，匹配仍是 OR）
companies:
  TSLA:
    - "特斯拉"
    - "Tesla"
    - "TSLA"

  SPACEX:
    - "SpaceX"
    - "星舰"
    - "Starship"
    - "星链"
    - "Starlink"

  XAI:
    - "xAI"
    - "Grok"

  NVDA:
    - "英伟达"
    - "NVIDIA"
    - "NVDA"
    - "辉达"

  OPENAI:
    - "OpenAI"
    - "ChatGPT"
    - "GPT"

# 话题关键词（数组格式仅用于分组，匹配时命中任意一个即可）
topics:
  # 马斯克相关
  - ["FSD", "自动驾驶", "Autopilot"]
  - ["Tesla Bot", "擎天柱", "机器人"]
  - ["星舰", "Starship", "火星"]
  - ["星链", "Starlink", "卫星互联网"]
  - ["超级工厂", "Gigafactory"]
  - ["Dojo", "训练芯片"]

  # 黄仁勋相关
  - ["GPU", "显卡"]
  - ["CUDA", "英伟达生态"]
  - ["Blackwell", "H100", "H200"]
  - ["AI 芯片", "算力"]
  - ["数据中心"]

  # AI 通用
  - ["AGI", "通用人工智能"]
  - ["大模型", "LLM"]
  - ["生成式 AI", "AIGC"]
  - ["深度学习", "神经网络"]

  # 中国大模型
  - ["deepseek", "kimi", "智谱", "glm", "minimax", "qwen", "豆包"]

  # 国外大模型
  - ["ChatGPT", "claude", "gemini"]

  # 大模型工具
  - ["claude code", "opencode", "claudecode", "Clawdbot"]

  # 机器人
  - ["人形机器人", "具身", "宇树", "开元"]

  # 太空产业
  - ["卫星", "星链", "星座计划", "低轨", "太空光伏", "太空算力", "钙钛矿"]
```

## 匹配规则

### 逻辑规则
- **OR 逻辑**: 标题或内容中包含【任意一个】关键词即匹配
- **不区分大小写**: 匹配时统一转换为小写比较
- **部分匹配**: 关键词是字符串的子串即匹配（如"马斯克"匹配"埃隆·马斯克"）

### 关键词格式要求

**错误格式** ❌:
```yaml
topics:
  - "kimi"        # 字符串格式会被 split() 成单个字符
  - "claude code"
```

**正确格式** ✅:
```yaml
topics:
  - ["kimi"]      # 数组格式，单个关键词
  - ["claude code"]  # 数组格式，含空格的关键词
  - ["deepseek", "kimi", "智谱"]  # 数组格式，多个相关关键词
```

**原因**: Python `set.update("string")` 会将字符串拆分成字符：
```python
>>> s = set()
>>> s.update("kimi")
>>> s
{'k', 'i', 'm'}  # 错误：变成了单个字符

>>> s = set()
>>> s.update(["kimi"])
>>> s
{'kimi'}  # 正确：保持了完整关键词
```

## 实现位置

**文件**: `src/crawlers/universal.py`

**方法**: `_filter_keywords(articles: List[Article]) -> List[Article]`

```python
def _filter_keywords(self, articles: List[Article]) -> List[Article]:
    """根据关键词过滤文章

    匹配规则：
    1. 标题或 URL 中包含任意关键词即匹配
    2. 不区分大小写
    3. OR 逻辑（命中任意一个即可）
    """
    all_keywords = self._load_all_keywords()

    filtered = []
    for article in articles:
        text_to_check = f"{article.title} {article.url}".lower()

        if any(kw.lower() in text_to_check for kw in all_keywords):
            filtered.append(article)

    return filtered
```

## 关键词精度问题

### 问题案例
关键词 `"生态"` 导致误匹配：
- "生态环境部：加快推动聚氯乙烯行业无汞化转型" ❌ 不相关
- 原因：`"生态"` 是 `"生态环境"` 的子串

### 解决方案
使用更精确的关键词：
- `"生态"` → `"英伟达生态"` 或 `"AI 生态"`
- `"芯片"` → `"AI 芯片"` 或 `"训练芯片"`

## 调试

### 查看已加载关键词

在代码中添加日志：
```python
all_keywords = self._load_all_keywords()
logger.info(f"[Filter] 关键词数量: {len(all_keywords)}, 前5个: {list(all_keywords)[:5]}")
```

### 检查关键词格式

```python
# 错误示例：单字符出现说明格式有问题
['Blackwell', '萨姆·奥尔特曼', 'l', 'GPT', 'h']
#                          ^  ^   单个字符

# 正确示例：都是完整词语
['Blackwell', '萨姆·奥尔特曼', '英伟达生态', 'GPT', 'H100']
```

## 维护建议

1. **定期审查误匹配**: 发现不相关新闻时，检查是否有过于通用的关键词
2. **优先使用精确关键词**: 如 "英伟达生态" 而非 "生态"
3. **保持分组清晰**: 使用 YAML 分组便于管理，但匹配时仍是 OR 逻辑
4. **测试新增关键词**: 添加新关键词后检查是否产生误匹配
