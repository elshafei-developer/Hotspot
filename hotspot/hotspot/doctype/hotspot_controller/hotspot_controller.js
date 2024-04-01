// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotspot Controller", {
  refresh(frm) {
    frm.add_custom_button(__("Create Printer Voucher"), () => {
      frappe.model.open_mapped_doc({
        method:
          "hotspot.hotspot.doctype.vouchers.vouchers.crete_from_controller",
        frm: frm,
      });
    });
  },
});
