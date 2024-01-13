# Path: api/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            email=instance.email,
            name=instance.first_name + ' ' + instance.last_name
        )
        print('Customer created!')
    else:
        if instance.customer:
            # Check if the Customer instance exists before attempting to save
            instance.customer.save()
            print('Customer updated!')
        else:
            print('Customer not found!')
