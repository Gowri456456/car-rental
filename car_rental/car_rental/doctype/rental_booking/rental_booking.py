import frappe
from frappe.website.website_generator import WebsiteGenerator


class RentalBooking(WebsiteGenerator):

    def validate(self):
        self.validate_date_overlap()

    def validate_date_overlap(self):

        if not self.vehicle or not self.pickup_date or not self.return_date:
            return

        new_pickup = frappe.utils.getdate(self.pickup_date)
        new_return = frappe.utils.getdate(self.return_date)

        existing_bookings = frappe.get_all(
            "Rental Booking",
            filters={
                "vehicle": self.vehicle,
                "name": ["!=", self.name]
            },
            fields=["name", "pickup_date", "return_date"]
        )

        for booking in existing_bookings:

            existing_pickup = frappe.utils.getdate(booking.pickup_date)
            existing_return = frappe.utils.getdate(booking.return_date)

            if (
                new_pickup <= existing_return
                and new_return >= existing_pickup
            ):
                frappe.throw(
                    f"Vehicle {self.vehicle} is already booked "
                    f"from {existing_pickup} to {existing_return}."
                )