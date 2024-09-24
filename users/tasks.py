# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import MachineCheck, FaceCheck

@shared_task
def reset_status_after_24_hours():
    now = timezone.now()

    # MachineCheck modelini tekshirish
    machine_checks = MachineCheck.objects.filter(status='approved')
    for machine_check in machine_checks:
        if (now - machine_check.status_last_updated).total_seconds() > 86400:  # 86400 soniya = 24 soat
            machine_check.status = 'not_submitted'
            machine_check.save()
            print(f'MachineCheck status reset for user: {machine_check.user.phone_number}')

    # FaceCheck modelini tekshirish
    face_checks = FaceCheck.objects.filter(status='approved')
    for face_check in face_checks:
        if (now - face_check.status_last_updated).total_seconds() > 86400:  # 86400 soniya = 24 soat
            face_check.status = 'not_submitted'
            face_check.save()
            print(f'FaceCheck status reset for user: {face_check.user.phone_number}')
