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
      () => {
        let d = new frappe.ui.Dialog({
          title: "Enter details",
          fields: [
            {
              label: "Name DocType",
              fieldname: "name_doc",
              fieldtype: "Data",
            },
          ],
          size: "small",
          primary_action_label: "Create",
          primary_action(values) {
            frappe.call({
              method:
                "hotspot.hotspot.doctype.vouchers.vouchers.create_printer_voucher",
              args: {
                name: this.get_value("name_doc"),
                vouchers: cur_list.get_checked_items(true),
              },
              callback: function (r) {
                if (r.message != false) {
                  d.hide();
                  frappe.show_alert({
                    message: __("Vouchers Printer Created"),
                    indicator: "green",
                  });
                  frappe.confirm(
                    __("Do You Want Move To This Vouchers Printer"),
                    () => {
                      frappe.set_route("Form", "Vouchers Printer", r.message);
                    }
                  );
                }
              },
            });
          },
        });
        if (cur_list.get_checked_items(true).length >= 1) {
          d.show();
        } else {
          frappe.throw(__("Please select vouchers to create printer voucher"));
          return;
        }
      },
      "Actions"
    );
    listview.page.add_inner_button(
      __("Download Vouchers Printr"),
      () => {
        frappe.call({
          method: "hotspot.hotspot.doctype.vouchers.vouchers.print_vouchers",
          args: {
            data: cur_list.get_checked_items(true),
          },
          callback: function (r) {
            if (r.message) {
              pdf = frappe.render_pdf(r.message, { orientation: "Portrait" });
            }
          },
          freeze: true,
          freeze_message: "Printing Vouchers...",
        });
      },
      "Actions"
    );
  },
};
