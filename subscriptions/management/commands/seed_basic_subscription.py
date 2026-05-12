import logging
from django.core.management.base import BaseCommand, CommandError
from subscriptions.models import Subscription

logger = logging.getLogger(__name__)

SUBSCRIPTIONS = [
    {"type": "Free Trial", "valid_no_of_days": 7,   "price": 0,    "currency": Subscription.CURRENCY_CHOICES.NPR},
    {"type": "Monthly",    "valid_no_of_days": 30,  "price": 200,  "currency": Subscription.CURRENCY_CHOICES.NPR},
    {"type": "Semi-Annually", "valid_no_of_days": 180, "price": 800,  "currency": Subscription.CURRENCY_CHOICES.NPR},
    {"type": "Annually",   "valid_no_of_days": 365, "price": 1500, "currency": Subscription.CURRENCY_CHOICES.NPR},
]


class Command(BaseCommand):
    help = "Seed basic subscription plans"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing subscriptions before seeding",
        )

    def handle(self, *args, **options):
        try:
            if options["clear"]:
                count, _ = Subscription.objects.all().delete()
                self.stdout.write(self.style.WARNING(f"Cleared {count} existing subscriptions."))
                logger.debug("Cleared %d subscriptions before seeding", count)

            created_count = 0
            skipped_count = 0

            for data in SUBSCRIPTIONS:
                obj, created = Subscription.objects.get_or_create(
                    type=data["type"],
                    defaults={
                        "valid_no_of_days": data["valid_no_of_days"],
                        "price":            data["price"],
                        "currency":         data["currency"],
                    },
                )
                if created:
                    created_count += 1
                    logger.debug("Created subscription: %s", obj)
                    self.stdout.write(f"  Created → {obj.type} ({obj.currency} {obj.price})")
                else:
                    skipped_count += 1
                    logger.debug("Skipped existing subscription: %s", obj)
                    self.stdout.write(self.style.WARNING(f"  Skipped → {obj.type} (already exists)"))

            self.stdout.write(
                self.style.SUCCESS(f"\nDone! {created_count} created, {skipped_count} skipped.")
            )

        except Exception as e:
            logger.exception("seed_subscriptions failed: %s", e)
            raise CommandError(f"Seeding failed: {e}")