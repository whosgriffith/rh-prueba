import random

from django.core.management.base import BaseCommand, CommandError

from rapihogar.models import Repairman, Pedido, User


class Command(BaseCommand):
    help = 'Generates n amount of Pedidos.'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        amount = options['amount']

        if not 1 <= amount <= 100:
            raise CommandError("Amount flag must be between 1 and 100")

        for _ in range(amount):
            try:
                clients = list(User.objects.all())
                random_client = random.choice(clients)
                repairmans = list(Repairman.objects.all())
                random_repairman = random.choice(repairmans)
                hours_worked = random.randint(1, 10)

                pedido = Pedido(client=random_client, repairman=random_repairman, hours_worked=hours_worked)
                pedido.save()
            except Exception as ex:
                raise CommandError(f"Couldn't create new Pedido: {ex}")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {amount} Pedidos"))
