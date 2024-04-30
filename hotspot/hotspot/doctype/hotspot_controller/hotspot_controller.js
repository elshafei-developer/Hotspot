// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotspot Controller", {
  refresh(frm) {
    frm.add_custom_button(__("Check Connection"), () => {
      frm.set_intro("The Hotspot connection is checked...", "blue");
      frappe
        .call({
          method:
            "hotspot.hotspot.doctype.vouchers.action_hotspot.check_connection",
        })
        .then((r) => {
          console.log(r);
          frm.refresh();
          if (r.message) {
            if (r.message.status == "false") {
              frm.set_intro(__("Failed Authorization to this Hotspot"), "red");
            } else {
              frm.set_intro(
                __("Successfully Connected to the Hotspot"),
                "green"
              );
            }
          } else {
            frm.set_intro(__("The Hotspot is Not Connected"), "red");
          }
        });
    });
  },
});
