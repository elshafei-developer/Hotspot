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
      "Delete Inactive Vouchers",
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

frappe.realtime.on("hotspot_disconnected", (data) => {
  for (let i = 0; i < data.length; i++) {
    frappe.show_alert(`Hotspot "${data[i]}" is Not Connected.`, 5);
  }
});

print = (name) => {
  var print_format = "Voucher";
  var w = window.open(
    frappe.urllib.get_full_url(
      "/api/method/frappe.utils.print_format.download_pdf?"
    ) +
      "doctype=" +
      encodeURIComponent("Vouchers") +
      "&name=" +
      encodeURIComponent(name) +
      "&format=" +
      encodeURIComponent(print_format) +
      "&no_letterhead=0" +
      "&_lang=en"
  );
  if (!w) {
    frappe.msgprint(__("Please enable pop-ups"));
    return;
  }
};
