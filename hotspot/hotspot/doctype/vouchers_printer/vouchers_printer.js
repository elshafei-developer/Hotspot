// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vouchers Printer", {
//   refresh: function (frm) {
//     frm.add_custom_button(__("Delete"), function () {
//       frappe.confirm(
//         "Do you want to delete this document?",
//         function () {
//           frappe.call({
//             method:
//               "hotspot.hotspot.doctype.vouchers_printer.vouchers_printer.delete_document",
//             args: {
//               docname: frm.docname,
//             },
//             freeze: true,
//             freeze_message: "Deleting...",
//             callback: function (r) {
//               console.log(r);
//               if (r.message) {
//                 frappe.show_alert({
//                   message: __("Document has been deleted"),
//                   indicator: "green",
//                 });
//                 frappe.set_route("List", "Vouchers Printer");
//               }
//             },
//           });
//         },
//         function () {
//           return false;
//         }
//       );
//     });
//   },
});
