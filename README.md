### Assumptions

If we want to make it more reliable to prevent memory leaks, we can use Flask + Celery workers to run constant tasks

rq-scheduler requires redis as well and to design a worker pattern for jobs to be taken