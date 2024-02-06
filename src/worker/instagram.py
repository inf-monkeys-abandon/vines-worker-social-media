import os
from pathlib import Path
from vines_worker_sdk.conductor.worker import Worker
from instagrapi import Client
from src.logger import logger
from src.utils import download_image, base64_to_bytes, get_and_ensure_exists_tmp_files_folder, save_bytes_to_image
import uuid
import json

PROXY_URL = os.environ.get("PROXY_URL")


class InstagramWorker(Worker):
    block_name = 'instagram'
    block_def = {
        "type": "SIMPLE",
        "name": block_name,
        "categories": ["auto"],
        "displayName": "Instagram",
        "description": "自动发布 Instagram 帖子",
        "icon": 'emoji:🤖️:#7fa3f8',
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
                "type": "string",
                "default": None,
                "required": True,
                "displayOptions": {
                    "show": {
                        "note_type": [
                            "image"
                        ]
                    }
                },
                "typeOptions": {
                    "multipleValues": True
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
                "type": "string",
                "default": [],
                "required": False,
                "typeOptions": {
                    "multipleValues": True
                }
            },
            {
                "displayName": "话题信息",
                "name": "topics",
                "type": "string",
                "default": [],
                "required": False,
                "typeOptions": {
                    "multipleValues": True
                }
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

    def handler(self, task, workflow_context, credential_data):
        workflow_id = task.get('workflowType')
        workflow_instance_id = task.get('workflowInstanceId')
        task_id = task.get('taskId')
        task_type = task.get('taskType')
        print(
            f"开始执行任务：workflow_id={workflow_id}, workflow_instance_id={workflow_instance_id}, task_id={task_id}, task_type={task_type}")
        input_data = task.get("inputData")

        if credential_data is None:
            raise Exception("请先配置 Instagram 账号")

        username = credential_data.get('username')
        password = credential_data.get('password')

        if PROXY_URL:
            print(f"使用代理 {PROXY_URL} 访问 Instagram")

        cl = Client(
            proxy=PROXY_URL,
            logger=logger
        )
        login_success = cl.login(username, password)
        if not login_success:
            raise Exception("登录 Instagram 失败")

        image_type = input_data.get('image_type')
        image_url = input_data.get("image_url")
        image_base64 = input_data.get('image_base64')

        image_buffer = None
        extension = ''
        if image_type == 'url':
            image_buffer = download_image(
                url=image_url
            )
            try:
                extension = image_url.split('/')[-1].split('.')[-1]
            except Exception as e:
                logger.warn(f"图像链接 {image_url} 无法获取后缀，使用 jpg 作为 fallback")
                extension = 'jpg'
        elif image_type == 'base64':
            extension = image_base64.split(';')[0].split('/')[1]
            if extension not in ['jpg', 'jpeg']:
                raise Exception("传入的 base64 图片不是 jpg 或者 jpeg 格式")
            image_buffer = base64_to_bytes(
                base64_string=image_base64
            )
        base_folder = get_and_ensure_exists_tmp_files_folder()
        file_path = Path(base_folder, f"{uuid.uuid4()}.{extension}")
        logger.info(f"保存图片到本地临时文件：{file_path}")
        save_bytes_to_image(
            bytes_data=image_buffer,
            file_path=file_path
        )
        caption = input_data.get("caption")
        custom_accessibility_caption = input_data.get("custom_accessibility_caption", None)
        like_and_view_counts_disabled = input_data.get("like_and_view_counts_disabled", False)
        disable_comments = input_data.get("disable_comments", False)

        try:
            media = cl.photo_upload(
                file_path,
                caption,
                extra_data={
                    "custom_accessibility_caption": custom_accessibility_caption,
                    "like_and_view_counts_disabled": 1 if like_and_view_counts_disabled else 0,
                    "disable_comments": 1 if disable_comments else 0,
                }
            )

            logger.info(f"上传图片成功：{media}")
            result_str = media.json()
            return json.loads(result_str)
        except Exception as e:
            err_msg = f"发布失败：{str(e)}"
            if 'Request processing failed' in err_msg:
                err_msg += "请检查图片是否为 jpg 或者 jpeg 格式（注意不能直接修改文件后缀，需要进行实际转换）"
            raise Exception(err_msg)
