import frappe
from frappe.website.website_generator import WebsiteGenerator


class RentalBooking(WebsiteGenerator):
    def validate(self):
        self.validate_date_overlap()

    def validate_date_overlap(self):
        if not self.vehicles or not self.pickup_date or not self.return_date:
            return

        new_pickup = frappe.utils.getdate(self.pickup_date)
        new_return = frappe.utils.getdate(self.return_date)

        existing_bookings = frappe.get_all(
            "Rental Booking",
            filters={
                "vehicles": self.vehicles,
                "name": ["!=", self.name],
                "docstatus": ["<", 2],
            },
            fields=["name", "pickup_date", "return_date"],
        )

        for booking in existing_bookings:
            existing_pickup = frappe.utils.getdate(booking.pickup_date)
            existing_return = frappe.utils.getdate(booking.return_date)

            if new_pickup <= existing_return and new_return >= existing_pickup:
                frappe.throw(
                    f"Vehicle {self.vehicles} is already booked "
                    f"from {existing_pickup} to {existing_return}."
                )

    def on_submit(self):
        if self.status == "Confirmed":
            frappe.enqueue(
                "car_rental.tasks.send_booking_email",
                booking=self.name,
                queue="short",
                enqueue_after_commit=True,
            )