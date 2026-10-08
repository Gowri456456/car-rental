// Copyright (c) 2026, gowri k and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rental Booking", {

    pickup_date: function(frm) {
        calculate_rental(frm);
    },

    return_date: function(frm) {
        calculate_rental(frm);
    },

    daily_rate: function(frm) {
        calculate_rental(frm);
    }

});

function calculate_rental(frm) {

    if (!frm.doc.pickup_date || !frm.doc.return_date) {
        return;
    }

    let pickup = frappe.datetime.str_to_obj(frm.doc.pickup_date);
    let return_date = frappe.datetime.str_to_obj(frm.doc.return_date);

    let days = frappe.datetime.get_diff(return_date, pickup);

    if (days <= 0) {
        frappe.throw("Return date must be after pickup date");
    }

    frm.set_value("rental_days", days);

    let rental_amount = days * (frm.doc.daily_rate || 0);

    frm.set_value("rental_amount", rental_amount);
}