// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotspot Controller", {
  onload(frm) {
    frm.set_intro("The Hotspot connection is checked...", "blue");
    frappe
      .call({
        method:
          "hotspot.hotspot.doctype.vouchers.rest_api_hotspot.connect_hotspot",
        args: {
          method: "GET",
        },
      })
      .then((r) => {
        frm.refresh();
        if (r.message) {
          if (r.message == "ERROR") {
            frm.set_intro(__("You are not authorized to this Hotspot"), "red");
          } else {
            frm.set_intro(__("Successfully Connected to the Hotspot"), "green");
          }
        } else {
          frm.set_intro(__("The Hotspot is Not Connected"), "red");
        }
      });
  },
  after_save(frm) {
    frm.reload_doc();
  },
});
