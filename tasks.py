from celery import Celery
from ml import retrain
from app import send_retraining_complete_mail
celery=Celery('demo',broker='sqla+sqlite:///database.db')

@celery.task
def retrain_job_in_background(job_id):
    retrain(job_id)
    send_retraining_complete_mail(job_id)
