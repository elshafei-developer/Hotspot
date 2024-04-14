frappe.ui.form.on("Vouchers", {
  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Vouchers", name1);
    frm.set_value("name1", frm.doc.name);
    frm.refresh_field("url");
    frm.refresh();
  },
  refresh(frm) {
    frappe
      .call(
        "hotspot.hotspot.doctype.hotspot_controller.hotspot_controller.get_servers"
      )
      .then((r) => {
        if (!frm.is_new()) {
          if (!r.message.includes(frm.doc.server)) {
            if (frm.doc.server == "الكل") {
              frm.set_intro("This Voucher Run on All Hotspot Server", "green");
            } else {
              frm.set_intro(
                "Not Found Server Hotspot For This Voucher in Hotspot Controller",
                "red"
              );
            }
          }
        }
        set_field_options("server", r.message);
      });
  },
  server(frm) {
    frm.refresh_field("server");
    frappe
      .call(
        "hotspot.hotspot.doctype.hotspot_controller.hotspot_controller.get_server_details",
        {
          server: frm.doc.server,
        }
      )
      .then((r) => {
        cur_frm.set_value("url", r.message);
      });
  },
});
