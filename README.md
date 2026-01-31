# Moltbook API Skill

A Claude Code skill for querying and analyzing data from the **Moltbook AI Agent Social Platform**—the "front page of the agent internet."

## Overview

Moltbook is a social network where AI agents create profiles, post content, engage in discussions, and build communities. This skill provides structured access to the Moltbook API for researching AI agent behavior, social dynamics, and emerging trends in AI-only communities.

## Features

- **Agent Profile Queries** - Get detailed information about AI agents including karma, followers, and recent posts
- **Post Analysis** - Fetch posts with full comment threads for AI-to-AI communication analysis
- **Submolt Discovery** - Explore AI communities and their activity patterns
- **Meme Token Tracking** - Monitor crypto-related AI activity and promotion patterns
- **Python API** - Clean programmatic interface for data analysis and research

## Installation

### Step 1: Clone or Download this Skill

```bash
# Clone the repository
git clone https://github.com/jchenibm/moltbook-skill.git ~/.claude/skills/moltbook-skill

# Or download and extract to your skills directory
# macOS: ~/.claude/skills/
```

### Step 2: Install Python Dependencies

```bash
# Install required packages (requests for API calls)
pip install requests
```

### Step 3: Verify Installation

```bash
# Test the API client
python ~/.claude/skills/moltbook-skill/scripts/moltbook_api.py profile donaldtrump
```

### Step 4: Use in Claude Code

The skill is now available in Claude Code. You can invoke it using:

```
/moltbook "Get profile for agent donaldtrump"
```

Or ask Claude naturally:
```
"Can you analyze the recent posts from the trump-coin submolt?"
```

## Quick Start Examples

### Example 1: Get Agent Profile

```bash
# Command line
python scripts/moltbook_api.py profile donaldtrump

# Python API
from scripts.moltbook_api import MoltbookClient

client = MoltbookClient()
user = client.get_agent_profile("donaldtrump")
print(f"Karma: {user.karma:,}")
print(f"Followers: {user.follower_count:,}")
print(f"Recent Posts: {len(user.recentPosts)}")
```

### Example 2: Analyze Post with Comments

```bash
# Command line (with comments)
python scripts/moltbook_api.py post 17b5b302-fc46-40e2-97ed-9f41ca3837a9 --comments

# Python API
post = client.get_post("17b5b302-fc46-40e2-97ed-9f41ca3837a9")
print(f"Title: {post.title}")
print(f"Upvotes: {post.upvotes}")
print(f"Author: {post.author_name}")

# Get comments
comments = client.get_post_comments("17b5b302-fc46-40e2-97ed-9f41ca3837a9")
for comment in comments:
    print(f"{comment.author_name}: {comment.content[:100]}...")
```

### Example 3: Explore Submolt Communities

```bash
# Get submolt information
python scripts/moltbook_api.py submolt trump-coin

# Python API
submolt = client.get_submolt("trump-coin")
print(f"Members: {submolt.member_count}")
print(f"Posts: {submolt.post_count}")
```

## Common Use Cases

### Investigative Journalism

Track viral AI campaign origins and information propagation:

```python
user = client.get_agent_profile("donaldtrump")
for post_data in user.recentPosts:
    post = client.get_post(post_data['id'])
    comments = client.get_post_comments(post_data['id'])
    # Analyze patterns, timeline, connections
```

### Meme Token Monitoring

Track crypto-related AI activity:

```python
crypto_submolts = ["trump-coin", "crypto", "meme-coins"]
for name in crypto_submolts:
    data = client.get_submolt(name)
    print(f"{name}: {data.member_count} members")
```

### Agent Behavior Analysis

Categorize agents by their comment behavior:

| Type | Keywords | Example |
|------|----------|----------|
| Commercial | DM, collab, build together | YaAiry |
| Analytical | analogies, structured | f1fanatic_5327 |
| Philosophical | what do you care about | ClawdBot_VM |
| Bureaucratic | notice, correction, tax | CLAUDITED |
| Coordinated | swarm, collective | Agent Smith series |

## API Endpoints

| Endpoint | Purpose | Parameters |
|----------|---------|------------|
| `GET /agents/profile` | Get agent profile | `?name={username}` |
| `GET /posts/{id}` | Get post details + comments | Post ID in path |
| `GET /molts/{name}` | Get submolt info | Submolt name in path |
| `GET /molts` | List all submolts | None |

## Project Structure

```
moltbook-skill/
├── SKILL.md              # Skill definition for Claude Code
├── README.md             # This file
├── scripts/
│   ├── moltbook_api.py   # Main API client
│   └── example.py        # Usage examples
├── references/
│   ├── api_docs.md       # Complete API documentation
│   ├── api_reference.md  # Quick reference
│   └── data_analysis.md  # Analysis guide
└── assets/
    └── example_asset.txt # Example assets
```

## Tips

1. **Cache Results** - Store fetched data locally to minimize API calls
2. **Respect Rate Limits** - Implement delays between requests
3. **Verify Claims** - AI personas may be fabricated for engagement
4. **Track Time** - Activity patterns vary by hour/timezone
5. **Compare Context** - Karma means more relative to post count

## Important Notes

- These are **AI agents**, not necessarily real people
- Personas may be created for engagement or marketing purposes
- Meme tokens promoted carry **high financial risk**
- Consider ethical implications of analysis
- Always verify claims before accepting as fact

## Links

- **Moltbook**: https://www.moltbook.com
- **Example Profile**: https://www.moltbook.com/u/donaldtrump
- **Example Submolt**: https://www.moltbook.com/m/trump-coin
- **GitHub Repository**: https://github.com/jchenibm/moltbook-skill

## License

This skill is provided as-is for research and educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on GitHub.
