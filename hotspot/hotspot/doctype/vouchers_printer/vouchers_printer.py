# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.pdf import get_pdf



class VouchersPrinter(Document):
	@property
	def v_test(self):
		return 'Virtual Field Test'
	@frappe.whitelist()
	def dd(self):
		return 'dd'
	

@frappe.whitelist()	
def delete_vouchers(name):
	vouchers = frappe.get_doc("Vouchers Printer", name)
	vouchers.vouchers_table = []
	frappe.msgprint("Delete Vouchers")	