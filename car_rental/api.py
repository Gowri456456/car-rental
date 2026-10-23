import frappe
from frappe.utils import getdate

@frappe.whitelist()
def get_available_vehicles(pickup_date, return_date):

    pickup_date = getdate(pickup_date)
    return_date = getdate(return_date)

    if return_date <= pickup_date:
        frappe.throw("Invalid date range")

    vehicles = frappe.get_all(
        "Vehicle",
        fields=["name", "daily_rate"]
    )

    bookings = frappe.get_all(
        "Rental Booking",
        filters={"docstatus": ["!=", 2]},
        fields=["vehicle", "pickup_date", "return_date"]
    )

    booked = set()

    for b in bookings:
        if not b.pickup_date or not b.return_date:
            continue

        start = getdate(b.pickup_date)
        end = getdate(b.return_date)

        if pickup_date < end and return_date > start:
            booked.add(b.vehicle)

    available = []

    for v in vehicles:
        if v.name not in booked:
            available.append(v)

    return available

    