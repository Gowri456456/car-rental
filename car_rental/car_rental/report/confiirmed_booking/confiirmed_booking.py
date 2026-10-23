import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"label": _("Booking"), "fieldname": "name", "fieldtype": "Link", "options": "Rental Booking", "width": 160},
        {"label": _("Customers"), "fieldname": "customers", "fieldtype": "Link", "options": "Customers", "width": 150},
        {"label": _("Vehicles"), "fieldname": "vehicles", "fieldtype": "Link", "options": "Vehicles", "width": 130},
        {"label": _("Pickup Date"), "fieldname": "pickup_date", "fieldtype": "Date", "width": 110},
        {"label": _("Return Date"), "fieldname": "return_date", "fieldtype": "Date", "width": 110},
        {"label": _("Rental Amount"), "fieldname": "rental_amount", "fieldtype": "Currency", "width": 130},
    ]


def get_data(filters):
    return frappe.get_all(
        "Rental Booking",
        filters={"status": "Confirmed", "docstatus": ["<", 2]},
        fields=["name", "customers", "vehicles", "pickup_date", "return_date", "rental_amount"],
        order_by="pickup_date desc",
    )