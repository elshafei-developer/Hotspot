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
        set_field_options("server", r.message);
      });
  },
  server(frm) {
    console.log("server");
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
let r = frappe.realtime.on("notFound", (data) => {
  frappe.show_alert(data.message);
  console.log("notFound");
});
