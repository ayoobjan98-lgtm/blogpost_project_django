from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import BlogPost


class MyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(username="ali")
        cls.post1 = BlogPost.objects.create(
            title="Post 1",
            description="desc 1",
            author=cls.user,
        )

    def setUp(self):
        return super().setUp()

    def test_links_is_in_main_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "لینک های همکاران")

    def test_is_username_in_main_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_create_post_when_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("add"))
        self.assertEqual(response.status_code, 200)
        blogpost = {"title": "title 1", "description": "description"}
        response = self.client.post(reverse("add"), blogpost)
        self.assertEqual(response.status_code, 302)

    def test_create_post_when_logged_out_fail(self):
        response = self.client.get(reverse("add"))
        self.assertEqual(response.status_code, 302)

    def test_other_user_cant_delete_other_user_blogpost(self):
        user = get_user_model().objects.create(username="ahmad")
        self.client.force_login(user)
        response = self.client.get(reverse("delete", args=[self.post1.id]))
        self.assertEqual(response.status_code, 403)

    def test_user_can_delete_his_own_blogpost(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete", args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("delete", args=[self.post1.id]))
        self.assertEqual(response.status_code, 302)
