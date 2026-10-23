# Copyright (c) 2026, gowri k and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


import frappe
from frappe.tests import IntegrationTestCase

class IntegrationTestRentalBooking(IntegrationTestCase):
    def test_date_overlap_blocked(self):
        first = frappe.get_doc({
            "doctype": "Rental Booking",
            "customers": "Boopathi",
            "vehicles": "CAR-003",
            "pickup_date": "2035-01-10",
            "return_date": "2035-01-15",
            "rental_days": 5,
            "daily_rate": 8000,
            "rental_amount": 40000,
            "status": "Confirmed",
        }).insert()

        second = frappe.get_doc({
            "doctype": "Rental Booking",
            "customers": "Boopathi",
            "vehicles": "CAR-003",
            "pickup_date": "2035-01-12",
            "return_date": "2035-01-18",
            "rental_days": 6,
            "daily_rate": 8000,
            "rental_amount": 48000,
            "status": "Confirmed",
        })

        with self.assertRaises(frappe.ValidationError):
            second.insert()