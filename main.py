from dotenv import load_dotenv

# 在最开始的时候加载 .env，不要挪到下面
load_dotenv()

from src.worker import conductor_client
from src.worker.xiaohongshu import BLOCK_NAME, BLOCK_DEF, handler

if __name__ == '__main__':
    conductor_client.register_block(BLOCK_DEF)
    conductor_client.register_handler(BLOCK_NAME, handler)

    conductor_client.start_polling()
