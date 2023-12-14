import os
from vines_worker_sdk.oss import OSSClient
from vines_worker_sdk.conductor import ConductorClient
from .xiaohongshu import BLOCK_DEF, BLOCK_NAME

SERVICE_REGISTRATION_URL = os.environ.get("SERVICE_REGISTRATION_URL")
SERVICE_REGISTRATION_TOKEN = os.environ.get("SERVICE_REGISTRATION_TOKEN")
CONDUCTOR_BASE_URL = os.environ.get("CONDUCTOR_BASE_URL")

if not CONDUCTOR_BASE_URL:
    raise Exception("请在环境变量中配置 CONDUCTOR_BASE_URL")

CONDUCTOR_USERNAME = os.environ.get("CONDUCTOR_USERNAME")
CONDUCTOR_PASSWORD = os.environ.get("CONDUCTOR_PASSWORD")
WORKER_ID = os.environ.get("WORKER_ID")
if not WORKER_ID:
    raise Exception("请在环境变量中配置 WORKER_ID")

CONDUCTOR_CLIENT_NAME_PREFIX = os.environ.get("CONDUCTOR_CLIENT_NAME_PREFIX", None)
REDIS_URL = os.environ.get("REDIS_URL")

if not REDIS_URL:
    raise Exception("请在环境变量中配置 REDIS_URL")

S3_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL")
S3_REGION_NAME = os.environ.get("S3_REGION_NAME")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_BASE_URL = os.environ.get("S3_BASE_URL")
oss_client = OSSClient(
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    endpoint_url=S3_ENDPOINT_URL,
    region_name=S3_REGION_NAME,
    bucket_name=S3_BUCKET_NAME,
    base_url=S3_BASE_URL,
)

conductor_client = ConductorClient(
    service_registration_url=SERVICE_REGISTRATION_URL,
    service_registration_token=SERVICE_REGISTRATION_TOKEN,
    conductor_base_url=CONDUCTOR_BASE_URL,
    redis_url=REDIS_URL,
    worker_id=WORKER_ID,
    worker_name_prefix=CONDUCTOR_CLIENT_NAME_PREFIX,
    authentication_settings={
        "username": CONDUCTOR_USERNAME,
        "password": CONDUCTOR_PASSWORD,
    },
    external_storage=oss_client,
)
