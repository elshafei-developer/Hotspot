frappe.pages["printer-vouchers"].on_page_load = function (wrapper) {
  let page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "None",
    single_column: true,
  });
  $(frappe.render_template("printer-vouchers", { data: "data" })).appendTo(
    page.body
  );
  console.log("page", page);
  console.log("wrapper", wrapper);
};
