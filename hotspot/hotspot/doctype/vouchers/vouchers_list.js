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
    listview.refresh_button.on("click", () => {
      listview.refresh();
      frappe
        .call("hotspot.hotspot.doctype.vouchers.action_hotspot.clear_cache")
        .then((r) => {
          listview.refresh();
        });
    });
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
        return r;
      })
      .then((r) => {
        listview.page.add_inner_button("Create Vouchers", () => {
          let dialog = new frappe.ui.Dialog({
            title: "Create Vouchers",
            fields: [
              {
                label: "Number of Vouchers",
                fieldname: "number_voucher",
                fieldtype: "Int",
                reqd: 1,
              },
              {
                label: "Voucher Server",
                fieldname: "server",
                fieldtype: "Select",
                options: r.message.servers,
                reqd: 1,
              },
              {
                label: "Voucher Time",
                fieldname: "limit_uptime",
                fieldtype: "Select",
                options: r.message.times,
                reqd: 1,
              },
              {
                label: "Create Vouchers Printer",
                fieldname: "create_print",
                fieldtype: "Check",
              },
            ],
            primary_action_label: "Create",
            primary_action(values) {
              frappe.call({
                method:
                  "hotspot.hotspot.doctype.vouchers.action_hotspot.crete_vouchers_background",
                args: {
                  number_vouchers: values.number_voucher,
                  server: values.server,
                  limit_uptime: values.limit_uptime,
                  create_print: values.create_print == 1 ? true : false,
                },
              });
              dialog.hide();
            },
          });
          dialog.show();
        });
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
              "hotspot.hotspot.doctype.vouchers.action_hotspot.create_printer_voucher",
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
          () => {
            frappe
              .call({
                method:
                  "hotspot.hotspot.doctype.vouchers.action_hotspot.delete_inactive_vouchers_background",
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

frappe.realtime.on("realtime_vouchers", (data) => {
  if (data.message == "delete") {
    cur_list.refresh();
  } else {
    cur_list.refresh();
    frappe.show_alert(
      {
        message: __(data.message),
        indicator: data.indicator,
        title: __(data.title),
      },
      7
    );
  }
});
