frappe.listview_settings["Vouchers"] = {
  button: {
    show(doc) {
      return doc.status === "Active";
    },
    get_label() {
      return "Print";
    },
    get_description(doc) {
      return __([`Print ${doc.name}`]);
    },
    action(doc) {
      print(doc.name);
    },
  },
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
      __("Print Vouchers"),
      () => {
        frappe.call({
          method: "hotspot.hotspot.doctype.vouchers.vouchers.print_vouchers",
          args: {
            data: cur_list.get_checked_items(true),
          },
          callback: function (r) {
            if (r.message) {
              frappe.render_pdf(r.message, { orientation: "Portrait" });
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

print = (name) => {
  // var doc = {};
  // doc.test = "Mr. Test";
  // let result = frappe.render_template("<h1>Hello {{ doc.test }}</h1>", {
  //   doc: doc,
  // });
  // frappe.render_pdf(result, { orientation: "Portrait" });
  // var print_format = "Print Vouchers";
  // var w = window.open(
  //   frappe.urllib.get_full_url(
  //     "/api/method/frappe.utils.print_format.download_pdf?"
  //   ) +
  //     "doctype=" +
  //     encodeURIComponent("Vouchers") +
  //     "&name=" +
  //     encodeURIComponent(name) +
  //     "&format=" +
  //     encodeURIComponent(print_format) +
  //     "&no_letterhead=0" +
  //     "&_lang=en"
  // );
  // if (!w) {
  //   frappe.msgprint(__("Please enable pop-ups"));
  //   return;
  // }
};

// var doc = {};
// doc.test = "Mr. Test";
// let result = frappe.render_template("<h1>Hello {{ doc.test }}</h1>", {
//   doc: doc,
// });
// frappe.render_pdf(result, { orientation: "Portrait" }); // orientation takes "Portrait" or "Landscape"
