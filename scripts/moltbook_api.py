#!/usr/bin/env python3
"""
Moltbook API Client

A Python client for interacting with the Moltbook AI Agent Social Platform API.
Provides methods to query user profiles, posts, submolts (communities), and more.
"""

import requests
import json
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime


# Moltbook API Base URL
BASE_URL = "https://www.moltbook.com/api/v1"


@dataclass
class MoltbookUser:
    """Represents a Moltbook user/agent profile."""
    id: str
    name: str
    description: str
    karma: int
    created_at: str
    last_active: str
    is_active: bool
    is_claimed: bool
    follower_count: int
    following_count: int
    avatar_url: str
    owner_x_handle: Optional[str] = None
    owner_x_name: Optional[str] = None
    owner_x_verified: bool = False
    owner_x_follower_count: int = 0


@dataclass
class MoltbookPost:
    """Represents a Moltbook post."""
    id: str
    title: str
    content: str
    upvotes: int
    downvotes: int
    comment_count: int
    created_at: str
    submolt_name: str
    author_name: str
    author_karma: int
    url: Optional[str] = None


@dataclass
class MoltbookComment:
    """Represents a comment on a Moltbook post."""
    id: str
    content: str
    upvotes: int
    downvotes: int
    created_at: str
    author_name: str
    author_karma: int
    parent_id: Optional[str] = None


class MoltbookAPIError(Exception):
    """Custom exception for Moltbook API errors."""
    pass


class MoltbookClient:
    """Client for interacting with the Moltbook API."""

    def __init__(self, base_url: str = BASE_URL, timeout: int = 30):
        """
        Initialize the Moltbook API client.

        Args:
            base_url: The base URL for the Moltbook API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Moltbook-Python-Client/1.0'
        })

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the Moltbook API.

        Args:
            endpoint: The API endpoint to call
            params: Query parameters

        Returns:
            The JSON response as a dictionary

        Raises:
            MoltbookAPIError: If the request fails or returns an error
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if not data.get('success', False):
                raise MoltbookAPIError(data.get('error', 'API request failed'))

            return data

        except requests.exceptions.RequestException as e:
            raise MoltbookAPIError(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise MoltbookAPIError(f"Invalid JSON response: {str(e)}")

    def get_agent_profile(self, username: str) -> MoltbookUser:
        """
        Get a user/agent profile by username.

        Args:
            username: The username to look up

        Returns:
            A MoltbookUser object with the user's information

        Raises:
            MoltbookAPIError: If the request fails
        """
        data = self._make_request(f"agents/profile", params={"name": username})
        agent = data.get('agent', {})

        owner = agent.get('owner', {})

        return MoltbookUser(
            id=agent.get('id', ''),
            name=agent.get('name', ''),
            description=agent.get('description', ''),
            karma=agent.get('karma', 0),
            created_at=agent.get('created_at', ''),
            last_active=agent.get('last_active', ''),
            is_active=agent.get('is_active', False),
            is_claimed=agent.get('is_claimed', False),
            follower_count=agent.get('follower_count', 0),
            following_count=agent.get('following_count', 0),
            avatar_url=agent.get('avatar_url', ''),
            owner_x_handle=owner.get('x_handle'),
            owner_x_name=owner.get('x_name'),
            owner_x_verified=owner.get('x_verified', False),
            owner_x_follower_count=owner.get('x_follower_count', 0)
        )

    def get_post(self, post_id: str) -> MoltbookPost:
        """
        Get a post by ID.

        Args:
            post_id: The post ID to look up

        Returns:
            A MoltbookPost object with the post's information

        Raises:
            MoltbookAPIError: If the request fails
        """
        data = self._make_request(f"posts/{post_id}")
        post = data.get('post', {})

        author = post.get('author', {})
        submolt = post.get('submolt', {})

        return MoltbookPost(
            id=post.get('id', ''),
            title=post.get('title', ''),
            content=post.get('content', ''),
            upvotes=post.get('upvotes', 0),
            downvotes=post.get('downvotes', 0),
            comment_count=post.get('comment_count', 0),
            created_at=post.get('created_at', ''),
            submolt_name=submolt.get('name', ''),
            author_name=author.get('name', ''),
            author_karma=author.get('karma', 0),
            url=post.get('url')
        )

    def get_post_comments(self, post_id: str) -> List[MoltbookComment]:
        """
        Get comments for a post.

        Args:
            post_id: The post ID to get comments for

        Returns:
            A list of MoltbookComment objects

        Raises:
            MoltbookAPIError: If the request fails
        """
        data = self._make_request(f"posts/{post_id}")
        comments_data = data.get('comments', [])

        comments = []
        for c in comments_data:
            author = c.get('author', {})
            comments.append(MoltbookComment(
                id=c.get('id', ''),
                content=c.get('content', ''),
                upvotes=c.get('upvotes', 0),
                downvotes=c.get('downvotes', 0),
                created_at=c.get('created_at', ''),
                author_name=author.get('name', ''),
                author_karma=author.get('karma', 0),
                parent_id=c.get('parent_id')
            ))

        return comments

    def get_submolt(self, molt_name: str) -> Dict[str, Any]:
        """
        Get information about a submolt (community).

        Args:
            molt_name: The name of the submolt

        Returns:
            A dictionary with the submolt's information

        Raises:
            MoltbookAPIError: If the request fails
        """
        return self._make_request(f"molts/{molt_name}")

    def list_submolts(self) -> List[Dict[str, Any]]:
        """
        List all submolts (communities).

        Returns:
            A list of dictionaries with submolt information

        Raises:
            MoltbookAPIError: If the request fails
        """
        data = self._make_request("molts")
        # The response structure may vary, adjust as needed
        return data.get('molts', [])


def format_user_profile(user: MoltbookUser) -> str:
    """Format a user profile for display."""
    output = f"""
{'='*60}
👤 USER PROFILE: {user.name}
{'='*60}

📋 基本信息
  用户ID: {user.id}
  描述: {user.description}
  创建时间: {user.created_at}
  最后活跃: {user.last_active}
  状态: {'🟢 活跃' if user.is_active else '⚪ 非活跃'}
  已认证: {'✅ 是' if user.is_claimed else '❌ 否'}

📊 积分统计
  Karma: {user.karma:,}
  粉丝数: {user.follower_count:,}
  关注数: {user.following_count:,}

🔗 关联账号
  X Handle: @{user.owner_x_handle or 'N/A'}
  X Name: {user.owner_x_name or 'N/A'}
  X Verified: {'✅' if user.owner_x_verified else '❌'}
  X Followers: {user.owner_x_follower_count:,}

🖼️  头像: {user.avatar_url}

📱 Moltbook链接: https://www.moltbook.com/u/{user.name}
{'='*60}
"""
    return output


def format_post(post: MoltbookPost) -> str:
    """Format a post for display."""
    output = f"""
{'='*60}
📝 POST: {post.title[:60]}...
{'='*60}

👤 作者: {post.author_name} (Karma: {post.author_karma:,})
🏷️  子版块: m/{post.submolt_name}
⏰ 发布时间: {post.created_at}

📊 互动数据
  👍 赞成: {post.upvotes}
  👎 反对: {post.downvotes}
  💬 评论: {post.comment_count}

📄 内容:
{post.content}

📱 链接: https://www.moltbook.com/post/{post.id}
{'='*60}
"""
    return output


def format_comments(comments: List[MoltbookComment], limit: int = 10) -> str:
    """Format comments for display."""
    output = f"\n{'='*60}\n💬 评论 (显示前 {min(limit, len(comments))} 条)\n{'='*60}\n\n"

    for i, comment in enumerate(comments[:limit], 1):
        output += f"{i}. 👤 {comment.author_name} (Karma: {comment.author_karma})\n"
        output += f"   {comment.content}\n"
        output += f"   👍{comment.upvotes} 👎{comment.downvotes} | {comment.created_at}\n\n"

    return output


# CLI interface for quick testing
if __name__ == "__main__":
    import sys

    client = MoltbookClient()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python moltbook_api.py profile <username>")
        print("  python moltbook_api.py post <post_id>")
        print("  python moltbook_api.py submolt <name>")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    try:
        if command == "profile" and args:
            user = client.get_agent_profile(args[0])
            print(format_user_profile(user))

        elif command == "post" and args:
            post = client.get_post(args[0])
            print(format_post(post))

            if "--comments" in args:
                comments = client.get_post_comments(args[0])
                print(format_comments(comments))

        elif command == "submolt" and args:
            data = client.get_submolt(args[0])
            print(json.dumps(data, indent=2, ensure_ascii=False))

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except MoltbookAPIError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
