from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm
)
from taxi.models import Manufacturer, Car


class DriverFormTest(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "XYZ12345",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "newdriver",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "abc123",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class SearchViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)
        # Manufacturers
        self.honda = Manufacturer.objects.create(name="Honda", country="Japan")
        self.bmw = Manufacturer.objects.create(name="BMW", country="Germany")

        # Drivers
        self.driver1 = get_user_model().objects.create_user(
            username="driver_one", password="test12345", license_number="ABC123"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver_two", password="test12345", license_number="XYZ789"
        )

        # Cars
        self.car1 = Car.objects.create(model="Civic", manufacturer=self.honda)
        self.car2 = Car.objects.create(model="M5", manufacturer=self.bmw)

    # ---------- DRIVER SEARCH ----------
    def test_driver_search_matching_query(self):
        url = reverse("taxi:driver-list") + "?username=driver_one"
        response = self.client.get(url)
        self.assertContains(response, "driver_one")
        self.assertNotContains(response, "driver_two")

    def test_driver_search_non_matching_query(self):
        url = reverse("taxi:driver-list") + "?username=unknown"
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context["driver_list"], [])

    def test_driver_search_no_query(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(len(response.context["driver_list"]), 3)

    # ---------- CAR SEARCH ----------
    def test_car_search_matching_query(self):
        url = reverse("taxi:car-list") + "?model=Civic"
        response = self.client.get(url)
        self.assertContains(response, "Civic")
        self.assertNotContains(response, "M5")

    def test_car_search_non_matching_query(self):
        url = reverse("taxi:car-list") + "?model=unknown"
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context["car_list"], [])

    def test_car_search_no_query(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(len(response.context["car_list"]), 2)

    # ---------- MANUFACTURER SEARCH ----------
    def test_manufacturer_search_matching_query(self):
        url = reverse("taxi:manufacturer-list") + "?name=Honda"
        response = self.client.get(url)
        self.assertContains(response, "Honda")
        self.assertNotContains(response, "BMW")

    def test_manufacturer_search_non_matching_query(self):
        url = reverse("taxi:manufacturer-list") + "?name=unknown"
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context["manufacturer_list"], [])

    def test_manufacturer_search_no_query(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)