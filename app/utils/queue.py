from celery import Celery
from .config import get_settings

# Initialize settings
settings = get_settings()

# Initialize Celery application
celery_app = Celery(
    "evaluator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configure task routes
celery_app.conf.task_routes = {
    "app.tasks.evaluate_job": {"queue": "evaluate"},
}

# Configure Celery settings
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    worker_cancel_long_running_tasks_on_connection_loss=True,
    task_time_limit=600,  # 10 minutes hard time limit
    task_soft_time_limit=540,  # 9 minutes soft time limit
)