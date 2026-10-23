
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def execute():
    doctype = "Rental Booking"

    if not frappe.get_meta(doctype).has_field("booking_source"):
        create_custom_field(
            doctype,
            {
                "fieldname": "booking_source",
                "label": "Booking Source",
                "fieldtype": "Select",
                "options": "\nManual\nOnline\nPhone\nWalk-in",
            }
        )
        frappe.clear_cache(doctype=doctype)

    frappe.db.sql("""
        UPDATE `tabRental Booking`
        SET booking_source = 'Manual'
        WHERE booking_source IS NULL
           OR booking_source = ''
    """)
