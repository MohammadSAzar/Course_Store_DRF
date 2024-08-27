from django.dispatch import receiver
from store.signals import order_creation

@receiver(order_creation)
def after_order_created(sender, **kwargs):
    print(f'New order is created {kwargs["order"].id}')


