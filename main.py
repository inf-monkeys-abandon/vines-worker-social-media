from dotenv import load_dotenv

# 在最开始的时候加载 .env，不要挪到下面
load_dotenv()

from src.worker import conductor_client

if __name__ == '__main__':
    conductor_client.start_polling()
