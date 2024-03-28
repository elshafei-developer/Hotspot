// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vouchers Printer", {
  before_load(frm) {
    frappe.db.get_doc("Vouchers Printer", frm.doc.name).then((doc) => {
      console.log(doc);
      console.log(doc.vouchers_table);
      doc.vouchers_table = [];
      console.log(doc.vouchers_table);
      // frm.save();
    });
  },

  onload(frm) {
    frm.refresh_field("vouchers_table");
    frappe.call({
      method: "hotspot.hotspot.doctype.vouchers.vouchers.get_vouchers",
      freeze: true,
      freeze_message: "Getting All Vouchers...",
      callback: function (r) {
        frm.doc.vouchers_table = [];
        for (let i = 0; i < r.message.length; i++) {
          frm.add_child("vouchers_table", {
            voucher: r.message[i].name,
            uptime: r.message[i].uptime,
          });
        }
        frm.refresh_field("vouchers_table");
      },
    });
  },
});
