from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve
from django.conf import settings
from taxi.urls import urlpatterns
from taxi.models import Driver, Car, Manufacturer

class PublicAccessTest(TestCase):
    def test_login_required_for_protected_pages(self):
        exempt_urls = [
            reverse("taxi:index"),
            reverse("login"),
        ]
        for urlpattern in urlpatterns:
            if hasattr(urlpattern, "name") and urlpattern.name is not None:
                try:
                    url = reverse(f"taxi:{urlpattern.name}")
                except:
                    continue
                if url in exempt_urls:
                    continue
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code, 302,
                    msg=f"URL '{url}' повинен вимагати логін, але повернув {response.status_code}"
                )
                self.assertIn(settings.LOGIN_URL, response.url)


class PrivateCarListViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "New_user",
            "password1": "zaq123edc",
            "password2": "zaq123edc",
            "license_number": "ABC12345",
            "first_name": "test first",
            "last_name": "test last",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        driver = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(driver.first_name, "test first")
        self.assertEqual(driver.last_name, "test last")
        self.assertEqual(driver.username, "New_user")
        self.assertEqual(driver.license_number, "ABC12345")

class PrivateCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)


    def test_create_driver(self):
        self.assertEqual(self.car.model, "Test Car")
        self.assertEqual(self.car.manufacturer, self.manufacturer)
        self.assertEqual(self.driver, self.car.drivers.all().first())


class ManufacturerTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)


    def test_create_manufacturer(self):
        manufacturer_test = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.assertEqual(manufacturer_test.name, "Test Manufacturer")
        self.assertEqual(manufacturer_test.country, "US")

