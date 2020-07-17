import os

broker_url = os.environ['REDIS_LOCATION']#'redis://127.0.0.1:6379/'
accept_content = ['json']
task_serializer = 'json'
