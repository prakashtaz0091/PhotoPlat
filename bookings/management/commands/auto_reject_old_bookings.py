from django.core.management.base import BaseCommand, CommandError
from bookings.tasks import auto_reject_old_bookings
from django.conf import settings
from background_task.models import Task

class Command(BaseCommand):
    help = "Automatically reject stale or old bookings"

    def handle(self, *args, **options):
        if Task.objects.filter(task_name="bookings.tasks.auto_reject_old_bookings").exists():
            print("No need to initalize new task")
            return
        auto_reject_old_bookings(repeat=settings.AUTO_REJECT_BOOKINGS_INTERVAL)
        print("Auto reject old bookings task initialized")