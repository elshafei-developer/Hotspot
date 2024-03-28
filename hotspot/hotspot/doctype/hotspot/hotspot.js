// Copyright (c) 2024, hassan elsahfei and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotspot", {
  refresh(frm) {
    frappe.call({
      method: "hotspot.hotspot.doctype.hotspot.hotspot.get_all_users",
      args: {
        doctype: "Hotspot",
      },
      freeze: true,
      freeze_message: "Getting All Users",
      callback: function (r) {
        for (let i = 0; i < r.message.length; i++) {
          frm.add_child("table", {
            name1: r.message[i].name,
            password: r.message[i].password ? r.message[i].password : "123",
          });
        }
        frm.refresh_field("table");
      },
    });
    frm.add_custom_button(
      "Add User",
      () => {
        let = dialog = new frappe.ui.Dialog({
          title: "Information User",
          fields: [
            {
              label: "Name User",
              fieldname: "name",
              fieldtype: "Data",
            },
            // {
            //   label: "Password",
            //   fieldname: "password",
            //   fieldtype: "password",
            // },
          ],
          primary_action_label: "Add User",
          primary_action(data) {
            frappe.call({
              method: "hotspot.hotspot.doctype.hotspot.hotspot.add_user",
              args: {
                name: data.name,
                password: data.password,
              },
              freeze: true,
              callback: (r) => {
                console.log(r);
              },
            });
            dialog.hide();
          },
        });
        dialog.show();
      },
      "Action"
    );
  },
});

frappe.ui.form.on("table", {
  // name1(frm, cdt, cdn) {
  //   console.log("name1");
  // },
  add_child: (frm, cdt, cdn) => {
    console.log("add_child");
  },
  name1: function (frm) {
    console.log("name1_add");
  },
  add_row: (frm, cdt, cdn) => {
    console.log("add");
  },
  password(frm, cdt, cdn) {
    console.log("password");
  },
  form_render(frm, cdt, cdn) {
    console.log("from_render");
  },
  add_row(frm, cdt, cdn) {
    console.log("add_row");
  },
  item_code(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    console.log(row);
    console.log("item_code");
  },
});
