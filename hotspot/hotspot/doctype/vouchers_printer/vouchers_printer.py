# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class VouchersPrinter(Document):
	pass


@frappe.whitelist()
def delete_document(docname):
	try:
		frappe.delete_doc('Vouchers Printer', docname)
		return True
	except Exception as e:
		frappe.throw(e)