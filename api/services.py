from statistics import fmean

from django.db.models import Sum, Q

from rapihogar.models import Repairman, Pedido


class RepairmanService:
    """ Service layer for Repairman model"""

    @classmethod
    def get_summary(cls):
        """ Returns a summary of all the repairman's """
        queryset = Repairman.objects.all()
        average_pay = cls.calculate_average_pay(queryset)
        data = {
            'average_pay': average_pay, 'below_average': [],
            'min_pay': (cls.get_latest_min_and_max_pay(queryset))[0],
            'max_pay': (cls.get_latest_min_and_max_pay(queryset))[1]
        }

        repairman_list = cls.get_list({})
        for repairman in repairman_list:
            if repairman['total_pay'] < average_pay:
                data['below_average'].append(repairman)

        return data

    @classmethod
    def get_list(cls, query_params):
        """ Returns all the repairman's with fullname, hours worked, total pay and orders """
        fullname = query_params.get('fullname')
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
                'orders': Pedido.objects.filter(repairman=repairman).count()
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

        if not hours_worked:
            return 0

        payment_rates_table = [
            [15, 200, 0.15],
            [29, 250, 0.16],
            [48, 300, 0.17],
            [float('inf'), 350, 0.18]
        ]

        for payment_rate in payment_rates_table:
            if hours_worked < payment_rate[0]:
                return (hours_worked * payment_rate[1]) - (hours_worked * payment_rate[1] * payment_rate[2])

    @classmethod
    def calculate_average_pay(cls, queryset):
        """ Calculates the average of all the repairman's pay """
        total_pay_list = []
        for repairman in queryset:
            total_pay_list.append(cls.calculate_total_pay(repairman))

        return fmean(total_pay_list)

    @classmethod
    def get_latest_min_and_max_pay(cls, queryset):
        """ Get the latest added repairman with max total pay """
        repairman_list = []
        for repairman in queryset:
            data = {'repairman': repairman, 'total_pay': cls.calculate_total_pay(repairman)}
            repairman_list.append(data)

        sorted_repairman_list = sorted(repairman_list, key=lambda x: x['repairman'].added_at, reverse=True)
        repairman_with_min_pay = min(sorted_repairman_list, key=lambda x: x['total_pay'])['repairman']
        repairman_with_max_pay = max(sorted_repairman_list, key=lambda x: x['total_pay'])['repairman']

        return repairman_with_min_pay.full_name, repairman_with_max_pay.full_name
