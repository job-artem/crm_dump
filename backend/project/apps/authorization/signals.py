from django.db.models import QuerySet
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from ..authorization.models import User
from ..crm.models import CoachForClient, NewClientCoach


@receiver(pre_save, sender=User)
def change_type_user(sender, instance: User, *args, **kwargs):
    if instance.user_type == User.USER:
        instance.is_superuser = False
        instance.is_staff = False
        instance.user_group = User.EMPTY
    elif instance.user_type == User.ADMIN:
        instance.is_superuser = True
        instance.is_staff = True
        instance.user_group = User.EMPTY
    elif instance.user_type == User.COACH:
        instance.is_superuser = False
        instance.is_staff = True
        instance.user_group = User.EMPTY
    elif instance.user_type == User.HEAD_COACH:
        instance.is_superuser = False
        instance.is_staff = True
    elif instance.user_type == User.OPERATOR:
        instance.is_superuser = True
        instance.is_staff = True
        instance.user_group = User.EMPTY


@receiver(pre_delete, sender=User)
def delete_coach(sender, instance: User, *args, **kwargs):
    first_admin = User.objects.filter(user_type=User.ADMIN).first()
    worker(CoachForClient.objects.filter(coach=instance), first_admin)
    worker(NewClientCoach.objects.filter(coach=instance), first_admin)


def worker(data: QuerySet, admin: User):
    for element in data:
        element.coach = admin
        element.save()
