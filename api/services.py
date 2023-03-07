from statistics import fmean

from django.db.models import Sum, Q

from rapihogar.models import Repairman, Pedido


class RepairmanService:
    """ Service layer for Repairman model"""

    @classmethod
    def get_summary(cls):
        """ Returns a summary of all the repairman's """
        repairman_list = cls.get_list()

        average_pay = fmean([r.get('total_pay', None) for r in repairman_list])

        data = {
            'average_pay': average_pay,
            'below_average': [],
        }

        for repairman in repairman_list:
            if repairman['total_pay'] < average_pay:
                data['below_average'].append(repairman)

        sorted_repairman_list = sorted(repairman_list, key=lambda x: x['added_at'], reverse=True)
        data['min_pay'] = min(sorted_repairman_list, key=lambda x: x['total_pay'])['full_name']
        data['max_pay'] = max(sorted_repairman_list, key=lambda x: x['total_pay'])['full_name']

        return data

    @classmethod
    def get_list(cls, query_params=None):
        """ Returns all the repairman's with fullname, hours worked, total pay and orders """
        fullname = query_params.get('fullname') if query_params else None
        if fullname:
            repairmans = Repairman.objects.filter(Q(first_name__icontains=fullname) | Q(last_name__icontains=fullname))
        else:
            repairmans = Repairman.objects.all()

        data = []
        for repairman in repairmans:
            repairman_data = {
                'full_name': repairman.full_name,
                'hours_worked': cls.calculate_hours_worked(repairman),
                'total_pay': cls.calculate_total_pay(repairman),
                'orders': Pedido.objects.filter(repairman=repairman).count(),
                'added_at': repairman.added_at
            }
            data.append(repairman_data)

        return data

    @classmethod
    def calculate_hours_worked(cls, repairman):
        """ Calculates the total hours worked of a repairman """
        hours_worked = Pedido.objects.filter(repairman=repairman).aggregate(Sum('hours_worked'))
        hours_worked_sum = hours_worked.get('hours_worked__sum')

        return hours_worked_sum if hours_worked_sum else 0

    @classmethod
    def calculate_total_pay(cls, repairman):
        """ Calculates the total pay of a repairman """
        hours_worked = cls.calculate_hours_worked(repairman=repairman)

        payment_rates_table = [
            [15, 200, 0.15],
            [29, 250, 0.16],
            [48, 300, 0.17],
            [float('inf'), 350, 0.18]
        ]

        for payment_rate in payment_rates_table:
            if hours_worked < payment_rate[0]:
                return (hours_worked * payment_rate[1]) - (hours_worked * payment_rate[1] * payment_rate[2])
