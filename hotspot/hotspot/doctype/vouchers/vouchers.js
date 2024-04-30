frappe.ui.form.on("Vouchers", {
  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Vouchers", name1);
    frm.set_value("name1", frm.doc.name);
  },
  onload(frm) {
    frappe
      .call(
        "hotspot.hotspot.doctype.hotspot_controller.hotspot_controller.get_info_table"
      )
      .then((r) => {
        if (!frm.is_new()) {
          if (!r.message.servers.includes(frm.doc.server)) {
            if (frm.doc.server == "الكل") {
              frm.set_intro("This Voucher Run on All Hotspot Server", "yellow");
            } else {
              frm.set_intro(
                "Not Found Server Hotspot For This Voucher in Hotspot Controller",
                "red"
              );
            }
          }
        }
        set_field_options("server", r.message.servers);
        set_field_options("limit_uptime", r.message.times);
      });
  },
});
