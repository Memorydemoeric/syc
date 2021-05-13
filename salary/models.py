from django.db import models

# Create your models here.

class WorkerIndex(models.Model):
    worker_name = models.CharField(max_length=32)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'syc_salary_worker_index'