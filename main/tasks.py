# main/tasks.py
from celery import shared_task

@shared_task
def fetch_latest_news():
    # 작업 내용 비활성화 또는 주석 처리
    pass

