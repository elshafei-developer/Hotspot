frappe.listview_settings["Vouchers"] = {
  onload: function (listview) {
    listview.page.add_inner_button(
      __("Delete Inactive Vouchers"),
      () => {
        frappe.confirm(
          "Are you sure you want to delete all inactive vouchers?",
          function () {
            frappe
              .call({
                method:
                  "hotspot.hotspot.doctype.vouchers.vouchers.delete_inactive_vouchers",
                callback: function (r) {
                  if (r.message) {
                    frappe.msgprint(r.message);
                  }
                },
                freeze: true,
                freeze_message: "Deleting Inactive Vouchers...",
              })
              .then(() => {
                listview.refresh();
              });
          }
        );
      },
      "Actions"
    );
    listview.page.add_inner_button(
      "Create Printer Voucher",

      // () => {
      //   frappe.model.open_mapped_doc({
      //     method: "hotspot.hotspot.doctype.vouchers.vouchers.make_B_from_A",
      //     frm: cur_list,
      //   });
      // },

      // Create and move
      () => {
        if (cur_list.get_checked_items(true).length >= 1) {
          frappe.call({
            method:
              "hotspot.hotspot.doctype.vouchers.vouchers.create_printer_voucher",
            args: {
              vouchers: cur_list.get_checked_items(true),
            },
            callback: function (r) {
              if (r.message != false) {
                frappe.set_route("Form", "Vouchers Printer", r.message);
              }
            },
          });
        } else {
          frappe.throw(__("Please select vouchers to create printer voucher"));
          return;
        }
      },
      "Actions"
    );
  },
};
