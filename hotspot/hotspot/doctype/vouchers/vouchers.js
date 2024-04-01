frappe.ui.form.on("Vouchers", {
  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Vouchers", name1);
    frm.set_value("name1", frm.doc.name);
  },
  refresh(frm) {
    frm.add_custom_button(__("Create Printer Voucher"), () => {
      frappe.model.open_mapped_doc({
        method: "hotspot.hotspot.doctype.vouchers.vouchers.crete_from_vouchers",
        frm: frm,
      });
    });
  },
});
