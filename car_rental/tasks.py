import frappe
from frappe.utils import today

def expire_bookings():
    bookings = frappe.get_all(
        "Rental Booking",
        filters={"return_date": ["<", today()], "status": "Confirmed"},
        pluck="name"
    )
    for name in bookings:
        frappe.db.set_value("Rental Booking", name, "status", "Completed")
    frappe.db.commit()





def send_booking_email(booking):
    doc = frappe.get_doc("Rental Booking", booking)

    # customer email edukkanum (unga field name-ku maathunga)
    email = frappe.db.get_value("Customers", doc.customers, "email")
    if not email:
        return
    frappe.sendmail(
        recipients=[email],
        subject=f"Booking Confirmed: {doc.name}",
         now=True,
        message=f"""
       
            <p>Hi,</p>
            <p>Your booking <b>{doc.name}</b> confirmed.</p>
            <p>Pickup: {doc.pickup_date}<br>Return: {doc.return_date}</p>
            <p>Nandri!</p>
        """,
    )