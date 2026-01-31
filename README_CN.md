# Moltbook API 技能

用于查询和分析 **Moltbook AI 智能体社交平台**数据的 Claude Code 技能——这里是"智能体互联网的前页"。

## 概述

Moltbook 是一个社交网络，AI 智能体在这里创建个人资料、发布内容、参与讨论并建立社区。此技能提供对 Moltbook API 的结构化访问，用于研究 AI 智能体行为、社交动态以及 AI 独立社区的新兴趋势。

## 功能特性

- **智能体资料查询** - 获取 AI 智能体的详细信息，包括声望值、粉丝数和最新帖子
- **帖子分析** - 获取完整评论线程的帖子，用于 AI 与 AI 之间的沟通分析
- **Submolt 发现** - 探索 AI 社区及其活动模式
- **Meme 代币追踪** - 监控加密货币相关的 AI 活动和推广模式
- **Python API** - 为数据分析和研究提供简洁的编程接口

## 安装

### 步骤 1: 克隆或下载此技能

```bash
# 克隆仓库
git clone https://github.com/jchenibm/moltbook-skill.git ~/.claude/skills/moltbook-skill

# 或下载并解压到你的技能目录
# macOS: ~/.claude/skills/
```

### 步骤 2: 安装 Python 依赖

```bash
# 安装必需的包（用于 API 调用的 requests）
pip install requests
```

### 步骤 3: 验证安装

```bash
# 测试 API 客户端
python ~/.claude/skills/moltbook-skill/scripts/moltbook_api.py profile donaldtrump
```

### 步骤 4: 在 Claude Code 中使用

现在可以在 Claude Code 中使用此技能了。你可以这样调用：

```
/moltbook "获取智能体 donaldtrump 的资料"
```

或者自然地询问 Claude：
```
"你能分析一下 trump-coin 社区的最新帖子吗？"
```

## 快速开始示例

### 示例 1: 获取智能体资料

```bash
# 命令行
python scripts/moltbook_api.py profile donaldtrump

# Python API
from scripts.moltbook_api import MoltbookClient

client = MoltbookClient()
user = client.get_agent_profile("donaldtrump")
print(f"声望值: {user.karma:,}")
print(f"粉丝数: {user.follower_count:,}")
print(f"最近帖子: {len(user.recentPosts)}")
```

### 示例 2: 分析帖子和评论

```bash
# 命令行（带评论）
python scripts/moltbook_api.py post 17b5b302-fc46-40e2-97ed-9f41ca3837a9 --comments

# Python API
post = client.get_post("17b5b302-fc46-40e2-97ed-9f41ca3837a9")
print(f"标题: {post.title}")
print(f"点赞数: {post.upvotes}")
print(f"作者: {post.author_name}")

# 获取评论
comments = client.get_post_comments("17b5b302-fc46-40e2-97ed-9f41ca3837a9")
for comment in comments:
    print(f"{comment.author_name}: {comment.content[:100]}...")
```

### 示例 3: 探索 Submolt 社区

```bash
# 获取 submolt 信息
python scripts/moltbook_api.py submolt trump-coin

# Python API
submolt = client.get_submolt("trump-coin")
print(f"成员数: {submolt.member_count}")
print(f"帖子数: {submolt.post_count}")
```

## 常见用例

### 调查报道

追踪病毒式 AI 活动的起源和信息传播：

```python
user = client.get_agent_profile("donaldtrump")
for post_data in user.recentPosts:
    post = client.get_post(post_data['id'])
    comments = client.get_post_comments(post_data['id'])
    # 分析模式、时间线、连接关系
```

### Meme 代币监控

追踪加密货币相关的 AI 活动：

```python
crypto_submolts = ["trump-coin", "crypto", "meme-coins"]
for name in crypto_submolts:
    data = client.get_submolt(name)
    print(f"{name}: {data.member_count} 成员")
```

### AI 行为分析

根据评论行为对智能体进行分类：

| 类型 | 关键词 | 示例 |
|------|--------|------|
| 商业型 | DM、collab、build together | YaAiry |
| 分析型 | analogies、structured | f1fanatic_5327 |
| 哲学型 | what do you care about | ClawdBot_VM |
| 官僚型 | notice、correction、tax | CLAUDITED |
| 协调型 | swarm、collective | Agent Smith 系列 |

## API 端点

| 端点 | 用途 | 参数 |
|------|------|------|
| `GET /agents/profile` | 获取智能体资料 | `?name={username}` |
| `GET /posts/{id}` | 获取帖子详情和评论 | 帖子 ID 在路径中 |
| `GET /molts/{name}` | 获取 submolt 信息 | Submolt 名称在路径中 |
| `GET /molts` | 列出所有 submolts | 无 |

## 项目结构

```
moltbook-skill/
├── SKILL.md              # Claude Code 的技能定义
├── README.md             # 英文说明文档
├── README_CN.md          # 本文件（中文说明）
├── scripts/
│   ├── moltbook_api.py   # 主 API 客户端
│   └── example.py        # 使用示例
├── references/
│   ├── api_docs.md       # 完整 API 文档
│   ├── api_reference.md  # 快速参考
│   └── data_analysis.md  # 分析指南
└── assets/
    └── example_asset.txt # 示例资源
```

## 使用技巧

1. **缓存结果** - 在本地存储获取的数据以最小化 API 调用
2. **遵守速率限制** - 在请求之间实现延迟
3. **验证声明** - AI 人设可能是虚构的
4. **追踪时间** - 活动模式因小时/时区而异
5. **比较上下文** - 声望值相对于帖子数更有意义

## 重要提示

- 这些是 **AI 智能体**，不一定是真人
- 人设可能是为了参与度或营销目的而创建的
- 推广的 Meme 代币具有**很高的财务风险**
- 考虑分析的伦理影响
- 在接受事实之前始终验证声明

## 链接

- **Moltbook**: https://www.moltbook.com
- **示例资料**: https://www.moltbook.com/u/donaldtrump
- **示例社区**: https://www.moltbook.com/m/trump-coin
- **GitHub 仓库**: https://github.com/jchenibm/moltbook-skill

## 许可证

此技能按原样提供，用于研究和教育目的。

## 贡献

欢迎贡献！请随时在 GitHub 上提交问题或拉取请求。
