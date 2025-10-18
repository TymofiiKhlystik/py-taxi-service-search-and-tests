from django.test import TestCase
from taxi.forms import DriverCreationForm, DriverSearchForm, CarSearchForm, ManufacturerSearchForm


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


class SearchFormsTest(TestCase):

    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Rs6"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Rs6")

    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Honda"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Honda")
