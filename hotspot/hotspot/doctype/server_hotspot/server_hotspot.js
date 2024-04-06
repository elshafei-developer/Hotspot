// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Server Hotspot", {
  after_save(frm) {
    server = frm.doc.server.replace(/ /g, "_");
    frm.set_value("server", frm.doc.name);
    frappe.set_route("Form", "Server Hotspot", server);
  },
});
