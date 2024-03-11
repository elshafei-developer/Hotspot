// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vouchers", {
  refresh(frm) {},
  before_save: (frm) => {
    if (!frm.is_new()) {
      console.log("is not new");
      //   frappe.call('hotspot.hotspot.doctype.vouchers.vouchers.update_voucher',
      //   );
    }
  },
});
