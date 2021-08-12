from django.core.management.base import BaseCommand
from downtimes.models import Tag
from django.utils.crypto import get_random_string
import time

class Command(BaseCommand):
    help = "Populate Tag model"

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **kwargs):
        amount: int = kwargs["amount"]
        chunk_size: int = 10000
        for i in range(amount):
	        Tag.objects.bulk_create([
	        	Tag(name=get_random_string()) for i in range(chunk_size)
	        ])
	        time.sleep(0.5)