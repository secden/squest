from django.urls import reverse

from tests.test_service_catalog.base import BaseTest


class OperationListTestCase(BaseTest):

    def setUp(self):
        super(OperationListTestCase, self).setUp()

        self.url = reverse('service_catalog:operation_list')

    def test_get_operation_list(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_customer_can_get_operation_list(self):
        self.client.force_login(self.standard_user)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_cannot_get_operation_list_logout(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)
