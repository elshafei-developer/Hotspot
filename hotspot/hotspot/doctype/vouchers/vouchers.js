frappe.ui.form.on("Vouchers", {
  refresh: function (frm) {
    if (!frm.is_new()) {
      frm.add_custom_button(
        __("Print"),
        () => {
          var print_format = "Voucher";
          var w = window.open(
            frappe.urllib.get_full_url(
              "/api/method/frappe.utils.print_format.download_pdf?"
            ) +
              "doctype=" +
              encodeURIComponent("Vouchers") +
              "&name=" +
              encodeURIComponent(frm.doc.name) +
              "&format=" +
              encodeURIComponent(print_format) +
              "&no_letterhead=0" +
              "&_lang=en"
          );
          if (!w) {
            frappe.msgprint(__("Please enable pop-ups"));
            return;
          }
        },
        __("Actions")
      );
    }
  },

  after_save(frm) {
    name1 = frm.doc.name1.replace(/ /g, "_");
    frappe.set_route("Form", "Vouchers", name1);
    frm.set_value("name1", name1);
  },
});
