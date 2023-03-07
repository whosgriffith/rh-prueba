import json

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from rapihogar.models import User, Company, Repairman, Pedido


class CompanyListCreateAPIViewTestCase(APITestCase):
    url = reverse("company-list")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_company(self):
        response = self.client.post(self.url,
            {
                "name": "company delete!",
                "phone": "123456789",
                "email": "test@rapihigar.com",
                "website": "http://www.rapitest.com"
            }
        )
        self.assertEqual(201, response.status_code)

    def test_list_company(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Company.objects.count())


class RepairmanListTestCase(APITestCase):
    url = reverse("repairman")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        repairman = Repairman.objects.create(first_name="Nicolas", last_name="Repetto")
        Pedido.objects.create(client=self.user, repairman=repairman, hours_worked=10)
        Pedido.objects.create(client=self.user, repairman=repairman, hours_worked=10)

    def test_list_repairman(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Repairman.objects.count())

    def test_list_repairman_with_filter(self):
        response = self.client.get(self.url, {'fullname': 'Nico'})
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Repairman.objects.filter(first_name__icontains="Nico")
                        .count())


class RepairmanSummaryTestCase(APITestCase):
    url = reverse("repairman-summary")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        repairman_1 = Repairman.objects.create(first_name="Nicolas", last_name="Repetto")
        Pedido.objects.create(client=self.user, repairman=repairman_1, hours_worked=10)
        Pedido.objects.create(client=self.user, repairman=repairman_1, hours_worked=10)

        Repairman.objects.create(first_name="Tomas", last_name="Repetto")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_repairman_summary(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content)['average_pay'], 2100)
        self.assertEqual(json.loads(response.content)['min_pay'], 'Tomas Repetto')
        self.assertEqual(json.loads(response.content)['max_pay'], 'Nicolas Repetto')
