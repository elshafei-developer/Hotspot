# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import requests
import frappe
from frappe import _
from frappe.utils import date_diff, add_days, nowdate
from frappe.model.document import Document


class Vouchers(Document):
	hotspot_controllers = frappe.get_all('Hotspot Controllers', fields=['*'])

	def db_insert(self, *args, **kwargs):
		insert_user(self.as_dict())

		
	def db_update(self, *args, **kwargs):
		pass
	
	# def save(self, *args, **kwargs):
	# 	if self.name is exist:
	# 		self.name = self.name1
	# 	insert_user(self.as_dict())
	# 	return super().save(*args, **kwargs)
		
	def delete(args):
		delete_user(args.name)

	def load_from_db(self):
		d = get_info_user(self.name)
		d['name1'] = d['name']
		super(Document, self).__init__(d)

	
	# def modified(self, *args, **kwargs):
	# 	return super().save(*args, **kwargs)


	@staticmethod
	def get_list(self, *args):
		return get_all_users()

	@staticmethod
	def get_count(args):
		pass	

	@staticmethod
	def get_stats(args):
		pass


# FUNCTIONS

def get_all_users():
	frappe.db.commit()
	for hotspot_controller in Vouchers.hotspot_controllers:
		try:
			api = requests.request("GET",f"https://{hotspot_controller['ip']}/rest/ip/hotspot/user",auth=(hotspot_controller['user'],hotspot_controller['password']),verify=False)
			return api.json()
		except:
			frappe.throw(_(f"Error: ''{hotspot_controller['name']}'' is not reachable. Please check the connection and try again."))
			return None

def get_info_user(user):
	hotspot_controller = Vouchers.hotspot_controllers[0]
	api = requests.request("GET",f"https://{hotspot_controller['ip']}/rest/ip/hotspot/user/{user}",auth=(hotspot_controller['user'],hotspot_controller['password']),verify=False)
	return api.json()

def insert_user(data):
	data = {
			"name": data['name'],
			'disabled': data['disabled'],
			}
	hotspot_controller = Vouchers.hotspot_controllers[0]
	requests.request("PUT",f"https://{hotspot_controller['ip']}/rest/ip/hotspot/user",
			auth=(hotspot_controller['user'],
			hotspot_controller['password']),
			verify=False,
			json=data)
	frappe.db.commit()


def delete_user(name):
	hotspot_controller = Vouchers.hotspot_controllers[0]
	requests.request("DELETE",f"https://{hotspot_controller['ip']}/rest/ip/hotspot/user/{name}",
			auth=(hotspot_controller['user'],
			hotspot_controller['password']),
			verify=False)
	return True

