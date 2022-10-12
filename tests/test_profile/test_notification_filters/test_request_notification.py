from django.urls import reverse

from profiles.models import RequestNotification
from tests.test_profile.base_test_profile import BaseTestProfile


class TestRequestNotification(BaseTestProfile):

    def setUp(self):
        super(TestRequestNotification, self).setUp()
        self.notification_filter_create_url = reverse('profiles:request_notification_create')
        self.kwargs_detail = {
            "request_notification_id": self.request_notification_filter_test.id
        }
        self.notification_filter_edit_url = reverse('profiles:request_notification_edit',
                                                    kwargs=self.kwargs_detail)
        self.notification_filter_delete_url = reverse('profiles:request_notification_delete',
                                                      kwargs=self.kwargs_detail)
        self.switch_notif_url = reverse('profiles:request_notification_switch')

        self.create_notification_filter_data = {
            "name": "new_notification_filter",
            "profile": self.superuser.profile.id
        }

    def test_notification_switch(self):
        # by default notification are enabled
        self.assertTrue(self.superuser.profile.request_notification_enabled)
        # switch to disabled
        response = self.client.get(self.switch_notif_url)
        self.assertEqual(302, response.status_code)
        self.superuser.refresh_from_db()
        self.assertFalse(self.superuser.profile.request_notification_enabled)
        # switch back to enabled
        response = self.client.get(self.switch_notif_url)
        self.assertEqual(302, response.status_code)
        self.superuser.refresh_from_db()
        self.assertTrue(self.superuser.profile.request_notification_enabled)

    def test_admin_can_create_notification_filter(self):
        response = self.client.get(self.notification_filter_create_url)
        self.assertEqual(200, response.status_code)
        before = RequestNotification.objects.count()
        response = self.client.post(self.notification_filter_create_url, data=self.create_notification_filter_data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(before + 1, RequestNotification.objects.count())

    def test_admin_cannot_create_notification_filter_for_other_admin(self):
        self.create_notification_filter_data["profile"] = self.superuser_2.profile.id
        before = RequestNotification.objects.count()
        response = self.client.post(self.notification_filter_create_url, data=self.create_notification_filter_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(before, RequestNotification.objects.count())

    def test_customer_cannot_create_notification_filter(self):
        self.client.force_login(user=self.standard_user)
        response = self.client.get(self.notification_filter_create_url)
        self.assertEqual(302, response.status_code)
        before = RequestNotification.objects.count()
        response = self.client.post(self.notification_filter_create_url, data=self.create_notification_filter_data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(before, RequestNotification.objects.count())

    def test_admin_can_update_notification_filter(self):
        response = self.client.get(self.notification_filter_edit_url)
        self.assertEqual(200, response.status_code)
        self.create_notification_filter_data["name"] = "new_name"
        response = self.client.post(self.notification_filter_edit_url, data=self.create_notification_filter_data)
        self.assertEqual(302, response.status_code)
        self.request_notification_filter_test.refresh_from_db()
        self.assertEqual(self.request_notification_filter_test.name, "new_name")

    def test_admin_cannot_update_notification_filter_for_other_admin(self):
        self.client.force_login(self.superuser_2)
        response = self.client.post(self.notification_filter_edit_url, data=self.create_notification_filter_data)
        self.assertEqual(200, response.status_code)
        self.request_notification_filter_test_2.refresh_from_db()
        self.assertEqual(self.request_notification_filter_test_2.name, "request_test_filter_2")

    def test_admin_can_delete_notification_filter(self):
        before = RequestNotification.objects.count()
        response = self.client.post(self.notification_filter_delete_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(before - 1, RequestNotification.objects.count())

    def test_admin_cannot_delete_notification_of_other_admin(self):
        self.client.force_login(self.superuser_2)
        response = self.client.post(self.notification_filter_delete_url)
        self.assertEqual(403, response.status_code)
        before = RequestNotification.objects.count()
        self.assertEqual(before, RequestNotification.objects.count())