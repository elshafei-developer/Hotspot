frappe.ui.form.on("Vouchers", {
  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Vouchers", name1);
    frm.set_value("name1", frm.doc.name);
  },
});
