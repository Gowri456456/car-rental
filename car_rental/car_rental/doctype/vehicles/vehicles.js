
vehicle: async function(frm) {
    if (!frm.doc.vehicle) {
        frm.set_value("daily_rate", 0);
        return;
    }

    const result = await frappe.db.get_value(
        "Vehicle",
        frm.doc.vehicle,
        "daily_rate"
    );

    console.log(result);

    if (result.message) {
        frm.set_value(
            "daily_rate",
            result.message.daily_rate || 0
        );
    }

    calculate_amount(frm);
},

