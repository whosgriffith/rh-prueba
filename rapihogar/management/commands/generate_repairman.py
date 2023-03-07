from django.core.management.base import BaseCommand, CommandError

from faker import Faker

from rapihogar.models import Repairman

fake = Faker('es_AR')


class Command(BaseCommand):
    help = "Generates n amount of repairman's"

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        for _ in range(options['amount']):
            try:
                first_name = fake.first_name()
                last_name = fake.last_name()

                repairman = Repairman(first_name=first_name, last_name=last_name)
                repairman.save()
            except Exception as ex:
                raise CommandError(f"Couldn't create new Repairman: {ex}")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {options['amount']} Repairman"))
