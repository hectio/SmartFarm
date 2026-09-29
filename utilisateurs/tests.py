import io
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ProfilUtilisateur


User = get_user_model()


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ProfilPhotoTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='photo_user', password='test-password-123')
		self.client.login(username='photo_user', password='test-password-123')

	def test_profile_photo_is_saved_and_displayed(self):
		image_data = io.BytesIO()
		Image.new('RGB', (2, 2), 'red').save(image_data, format='JPEG')
		image = SimpleUploadedFile('avatar.jpg', image_data.getvalue(), content_type='image/jpeg')

		response = self.client.post(reverse('utilisateurs:profil'), {
			'first_name': '',
			'last_name': '',
			'username': 'photo_user',
			'is_active': 'on',
			'email': 'photo@example.com',
			'telephone': '',
			'adresse': '',
			'role': 'agriculteur',
			'exploitation': '',
			'photo': image,
		})

		self.assertRedirects(response, reverse('utilisateurs:profil'))
		profile = ProfilUtilisateur.objects.get(user=self.user)
		self.assertTrue(profile.photo.name)
		self.assertContains(self.client.get(reverse('utilisateurs:profil')), profile.photo.url)


class UserManagementAccessTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='regular_user',
			password='test-password-123',
		)
		self.target = User.objects.create_user(username='target_user')

	def test_anonymous_user_cannot_access_user_management(self):
		response = self.client.get(reverse('utilisateurs:liste'))

		self.assertRedirects(
			response,
			f'/login/?next={reverse("utilisateurs:liste")}',
		)

	def test_regular_user_cannot_access_user_management(self):
		self.client.force_login(self.user)

		response = self.client.get(reverse('utilisateurs:liste'))

		self.assertRedirects(
			response,
			f'/login/?next={reverse("utilisateurs:liste")}',
		)

	def test_staff_user_can_access_user_management(self):
		self.user.is_staff = True
		self.user.save(update_fields=['is_staff'])
		self.client.force_login(self.user)

		response = self.client.get(reverse('utilisateurs:liste'))

		self.assertEqual(response.status_code, 200)
