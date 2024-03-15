from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'main.settings')

app = Celery('main' , broker = 'amqp://guest:guest@localhost:5672')


app.autodiscover_tasks()

app.config_from_object('main.celery_routes')

app.conf.result_backend = 'rpc://'
app.conf.task_serilizer = 'json'
app.conf.result_serializer = 'pickle'
app.conf.accept_content =['json' ,'pickle']
app.conf.result_expires = timedelta(days=1)





