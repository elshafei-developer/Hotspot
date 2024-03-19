frappe.ui.form.on("Vouchers", {
  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Vouchers", name1);
    frm.set_value("name1", frm.doc.name);
  },
  refresh(frm) {
    frm.add_custom_button(__("Button Name 1"), function () {
      // cur_frm.set_value("print_format_selector", "format_1");
      frm.print_doc();
    });
  },
});
