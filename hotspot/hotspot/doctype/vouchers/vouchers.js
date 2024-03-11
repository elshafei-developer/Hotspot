// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vouchers", {
  refresh(frm) {
    // console.log(frm.doc.name);
  },
  before_save: (frm) => {
    if (!frm.is_new()) {
      //   console.log("is not new");
      //   frappe.call('hotspot.hotspot.doctype.vouchers.vouchers.update_voucher',
      //   );
    }
  },
  after_save: (frm) => {
    console.log("URL");
    console.log(URL);
    // window.location.reload(frm.doc.name1);
  },
});
