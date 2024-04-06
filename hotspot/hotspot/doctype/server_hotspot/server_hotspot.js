// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Server Hotspot", {
  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Server Hotspot", name1);
    frm.set_value("name1", frm.doc.name);
  },
});
