frappe.listview_settings["Vouchers"] = {
  hide_name_filter: true,
  get_indicator(doc) {
    if (doc.server == null) {
      return [__("ERROR"), "red"];
    }
  },
  formatters: {
    server: function (doc) {
      if (doc == "") {
        return [__("ERROR").bold()];
      } else {
        return doc;
      }
    },
  },
  onload: function (listview) {
    frappe
      .call(
        "hotspot.hotspot.doctype.hotspot_controller.hotspot_controller.get_info_table"
      )
      .then((r) => {
        listview.page.fields_dict.server.set_options(
          (listview.page.fields_dict.server.df.options = [
            "",
            ...r.message.servers,
          ])
        );
        listview.page.fields_dict.limit_uptime.set_options(
          (listview.page.fields_dict.limit_uptime.df.options = [
            "",
            ...r.message.times,
          ])
        );
      });
    listview.page.add_inner_button(
      "Create Printer Voucher",
      () => {
        if (cur_list.get_checked_items(true).length >= 1) {
          vouchers = cur_list.data.filter((voucher) => {
            return cur_list.get_checked_items(true).includes(voucher.name);
          });
          frappe.call({
            method:
              "hotspot.hotspot.doctype.vouchers.vouchers.create_printer_voucher",
            args: {
              vouchers: vouchers,
            },
            freeze: true,
            freeze_message: "Creating Printer Vouchers...",
            callback: function (r) {
              if (r.message != false) {
                frappe.set_route("Form", "Vouchers Printer", r.message);
              } else {
                frappe.throw(`ERROR => ${r.massage}`);
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
  },
};
