frappe.ui.form.on("Rental Booking", {
    vehicles: async function(frm) {
        if (!frm.doc.vehicles) {
            await frm.set_value("daily_rate", 0);
            calculate_amount(frm);
            return;
        }

        let r = await frappe.db.get_value(
            "Vehicles",
            frm.doc.vehicles,
            "daily_rate"
        );

        let rate = r.message ? (r.message.daily_rate || 0) : 0;

        await frm.set_value("daily_rate", rate);
        calculate_amount(frm);
    },

    pickup_date: function(frm) {
        calculate_amount(frm);
    },

    return_date: function(frm) {
        calculate_amount(frm);

        if (
            frm.doc.vehicles &&
            frm.doc.pickup_date &&
            frm.doc.return_date &&
            frm.doc.return_date > frm.doc.pickup_date
        ) {
            check_vehicle_booking(frm);
        }
    },

    daily_rate: function(frm) {
        calculate_amount(frm);
    }
});


function calculate_amount(frm) {
    if (!frm.doc.pickup_date || !frm.doc.return_date) {
        frm.set_value("rental_days", 0);
        frm.set_value("rental_amount", 0);
        return;
    }

    let days = frappe.datetime.get_diff(
        frm.doc.return_date,
        frm.doc.pickup_date
    );

    if (days <= 0) {
        frappe.msgprint(
            "Return Date must be after Pickup Date."
        );

        frm.set_value("rental_days", 0);
        frm.set_value("rental_amount", 0);
        return;
    }

    frm.set_value("rental_days", days);

    frm.set_value(
        "rental_amount",
        days * (frm.doc.daily_rate || 0)
    );
}


async function check_vehicle_booking(frm) {
    let bookings = await frappe.db.get_list(
        "Rental Booking",
        {
            filters: [
                ["vehicles", "=", frm.doc.vehicles],
                ["status", "=", "Confirmed"],
                ["pickup_date", "<", frm.doc.return_date],
                ["return_date", ">", frm.doc.pickup_date],
                ["name", "!=", frm.doc.name || ""]
            ],
            fields: ["name"],
            limit: 1
        }
    );

    if (bookings.length > 0) {
        frappe.msgprint(
            "This vehicle is already booked for these dates."
        );
    }
}
function refresh(frm) {
    if (frm.doc.docstatus === 1) {
        frm.add_custom_button(__("Mark as Returned"), () => {
            frappe.confirm(
                __("Are you sure you want to mark this booking as returned?"),
                () => {
                    frappe.msgprint(__("Booking marked as returned"));
                }
            );
        });
    }
}