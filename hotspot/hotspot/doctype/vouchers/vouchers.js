// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vouchers", {
  refresh(frm) {},
});
frappe.listview_settings["Vouchers"] = {
  get_indicator(doc) {
    // customize indicator color
    if (doc.disabled == "false") {
      doc.status = "Active";
    } else {
      return [__("Inactive"), "darkgrey", "status,=,else"];
    }
  },
  before_render(doc) {
    if (doc.disabled == "false") {
      doc.status = "Active";
    } else {
      return [__("Inactive"), "red", "status,=,else"];
    }
  },
};
