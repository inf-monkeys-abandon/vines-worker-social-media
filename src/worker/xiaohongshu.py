from src.xhs.sign import sign
from src.xhs.core import XhsClient
from src.xhs.utils import beauty_print

BLOCK_NAME = 'xiaohongshu'
BLOCK_DEF = {
    "type": "SIMPLE",
    "name": BLOCK_NAME,
    "categories": ["im"],
    "displayName": "小红书",
    "description": "自动发布小红书帖子",
    "icon": 'emoji:🤏:#fef8a3',
    "input": [
        {
            "displayName": "帖子类型",
            "name": "note_type",
            "type": "options",
            "default": "image",
            "required": True,
            "options": [
                {
                    "name": "图文",
                    "value": "image"
                },
                {
                    "name": "视频",
                    "value": "video"
                }
            ]
        },
        {
            "displayName": "标题",
            "name": "title",
            "type": "string",
            "default": "",
            "required": True,
        },
        {
            "displayName": "描述信息",
            "name": "desc",
            "type": "string",
            "default": "",
            "required": True,
        },
        {
            "displayName": "图片列表",
            "name": "images",
            "type": "collection",
            "default": None,
            "required": True,
            "displayOptions": {
                "show": {
                    "note_type": [
                        "image"
                    ]
                }
            }
        },
        {
            "displayName": "视频封面",
            "name": "video_cover_url",
            "type": "string",
            "default": None,
            "required": False,
            "displayOptions": {
                "show": {
                    "note_type": [
                        "video"
                    ]
                }
            }
        },
        {
            "displayName": "视频链接",
            "name": "video_url",
            "type": "string",
            "default": None,
            "required": True,
            "displayOptions": {
                "show": {
                    "note_type": [
                        "video"
                    ]
                }
            }
        },
        {
            "displayName": "设置定时发布时间",
            "description": "时间格式：2023-07-25 23:59:59",
            "name": "post_time",
            "type": "string",
            "default": None,
            "required": False,
        },
        {
            "displayName": "@用户信息",
            "name": "ats",
            "type": "collection",
            "default": [],
            "required": False,
        },
        {
            "displayName": "话题信息",
            "name": "topics",
            "type": "collection",
            "default": [],
            "required": False,
        },
        {
            "displayName": "是否私密发布",
            "name": "is_private",
            "type": "boolean",
            "default": False,
            "required": True,
        },
    ],
    "output": [
        {
            "name": "id",
            "displayName": "小红书帖子 id",
            "type": "string",
        },
        {
            "name": "score",
            "displayName": "分数",
            "type": "number",
        },
        {
            "name": "link",
            "displayName": "链接",
            "type": "string",
        },
    ],
    "credentials": [
        {
            "name": "xiaohongshu",
            "required": True
        }
    ],
    "extra": {
        "estimateTime": 5,
    },
}


def handler(task, workflow_context, credential_data):
    if not credential_data:
        raise Exception("请先配置小红书账号")
    workflow_id = task.get('workflowType')
    workflow_instance_id = task.get('workflowInstanceId')
    task_id = task.get('taskId')
    task_type = task.get('taskType')
    print(
        f"开始执行任务：workflow_id={workflow_id}, workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")

    input_data = task.get("inputData")
    print(input_data)
    cookie = credential_data.get('cookie')
    is_private = input_data.get("is_private", False)
    note_type = input_data.get("note_type", "image")
    ats = input_data.get("ats", [])
    topics = input_data.get("topics", [])
    video_url = input_data.get("video_url", None)
    video_cover_url = input_data.get('video_cover_url', None)
    images = input_data.get("images", [])
    if isinstance(images, str):
        images = [images]
    title = input_data.get('title')
    post_time = input_data.get('post_time')
    desc = input_data.get('desc')

    xhs_client = XhsClient(cookie, sign=sign)
    result = None
    if note_type == 'image':
        result = xhs_client.create_image_note(
            title=title,
            desc=desc,
            files=images,
            is_private=is_private,
            topics=topics,
            post_time=post_time,
            ats=ats
        )
    elif note_type == 'video':
        result = xhs_client.create_video_note(
            title=title,
            desc=desc,
            video_path=video_url,
            is_private=is_private,
            topics=topics,
            post_time=post_time,
            ats=ats,
            cover_path=video_cover_url
        )
    beauty_print(result)
    id, score = result['id'], result['score']
    link = f"https://www.xiaohongshu.com/explore/{id}"
    return {
        "id": id,
        "score": score,
        "link": link
    }
