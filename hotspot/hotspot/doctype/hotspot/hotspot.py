# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt
import  requests
import frappe
from frappe.model.document import Document


class Hotspot(Document):
	def before_save(self):
		self.table = []
	def validate(self):
		pass
	@frappe.whitelist()
	def get_all_users(self):
		frappe.msgprint("GET all")
		return 'GET All User'


@frappe.whitelist()
def get_all_users():
	api = requests.request("GET","https://192.168.88.1/rest/ip/hotspot/user",auth=('admin','123'),verify=False)
	return api.json()

@frappe.whitelist()
def add_user(name,password):
	requests.request("PUT","http://192.168.88.1/rest/ip/hotspot/user",auth=('admin','123'),json={"name":f"user"})
	return {name,password}
