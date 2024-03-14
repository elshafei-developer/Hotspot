import requests
import frappe
from frappe import _
from frappe.model.document import Document

class Vouchers(Document):

	def db_insert(self, *args, **kwargs):
		insert_voucher(self.as_dict())
		self.modified = False

	def db_update(self, *args, **kwargs):
		update_voucher(self.name, self.as_dict())
		self.modified = False
		
	def delete(args):
		delete_voucher(args.name)
	
	def load_from_db(self):
		self.modified = False
		voucher = get_info_voucher(self.name)
		super(Document, self).__init__(voucher)
	
	@staticmethod
	def get_list(self, *args,limit_page_length=2):
		print(args, '\n\n\n')
		print(*args, '\n\n\n')
		return get_vouchers()

	@staticmethod
	def get_count(args):
		pass	

	@staticmethod
	def get_stats(args):
		pass

# FUNCTIONS
def get_vouchers():
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])
	try:
		api = requests.request("GET",f"https://{IP}/rest/ip/hotspot/user",auth=(admin,password),verify=False)
		all_vouchers = api.json()
		all_vouchers.pop(0)
		data_map = lambda x: {'name': x['name'],
								'status': 'Active' if x['disabled'] == 'false' else 'Inactive',
								'uptime': x['uptime'],
								'limit_uptime': extract_time(x['limit-uptime']) if 'limit-uptime' in x else None,}
		all_vouchers_map = list(map(data_map, all_vouchers))
		return all_vouchers_map
	except:
		frappe.throw(_(f"Error: hotspot is not reachable. Please check the connection and try again."))

def get_info_voucher(user):
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])

	api = requests.request("GET",f"https://{IP}/rest/ip/hotspot/user/{user}",auth=(admin,password),verify=False)
	if api.status_code == 200:
		info_voucher = api.json()
		info_voucher['name1'] = info_voucher['name']
		info_voucher['status'] = 'Active' if info_voucher['disabled'] == 'false' else 'Inactive'
		if 'limit-uptime' in info_voucher:
			info_voucher['limit_uptime'] = extract_time(info_voucher['limit-uptime'])
		return info_voucher
	else:
		frappe.throw(_(f"Error: The voucher '{user}' does not exist."))

def insert_voucher(data):
	voucher_exists(data['name1'])
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])
	data = voucher_data(data)
	requests.request("PUT",f"https://{IP}/rest/ip/hotspot/user",auth=(admin,password),verify=False,json=data)

def delete_voucher(name):
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])
	requests.request("DELETE",f"https://{IP}/rest/ip/hotspot/user/{name}",auth=(admin,password),
					verify=False)

def update_voucher(voucher,data):
	voucher_exists(data['name1'],data['name'])
	data = voucher_data(data)
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])
	requests.request("PATCH",f"https://{IP}/rest/ip/hotspot/user/{voucher}",auth=(admin,password),
			verify=False,
			json=data)

def voucher_exists(new_name,old_name=None):
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])
	api = requests.request("GET",f"https://{IP}/rest/ip/hotspot/user",auth=(admin,password),verify=False)
	all_vouchers = api.json()
	vouchers_exists = list(map(lambda x: x['name'], all_vouchers))
	if old_name:
		vouchers_exists.pop(vouchers_exists.index(old_name))
	if new_name in vouchers_exists:
		return frappe.throw(_(f"Error: The voucher '{new_name}' already exists."))
	
def voucher_data(data):
	return {
		"name": data['name1'].replace(' ','_'),
		'disabled': 'false' if data['status'] == 'Active' else 'true',
		'limit-uptime':  '00:00:00' if data['limit_uptime'] == None else data['limit_uptime'],
	}

def extract_time(time_str):
    hours, minutes, seconds, days = 0, 0, 0, 0
    if 'd' in time_str:
        parts = time_str.split('d')
        days = int(parts[0])
        time_str = parts[1]
    if 'h' in time_str:
        parts = time_str.split('h')
        hours = int(parts[0])
        time_str = parts[1]
    if 'm' in time_str:
        parts = time_str.split('m')
        minutes = int(parts[0])
        time_str = parts[1]
    if 's' in time_str:
        seconds = int(time_str.replace('s', ''))
    
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return formatted_time

def get_hotspot_controller():
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	IP_hotspot_controller = hotspot_controller.as_dict()
	return {
		'IP': IP_hotspot_controller['ip'],
		'user': IP_hotspot_controller['user'],
		'password': IP_hotspot_controller['password']
	}

# ##### List View ##### #
@frappe.whitelist()
def delete_inactive_vouchers():
	device_hotspot = get_hotspot_controller()
	IP, admin, password = (device_hotspot['IP'], device_hotspot['user'], device_hotspot['password'])
	api = requests.request("GET",f"https://{IP}/rest/ip/hotspot/user",auth=(admin,password),verify=False)
	all_vouchers = api.json()
	all_vouchers.pop(0)
	inactive_vouchers = list(filter(lambda x: x['disabled'] == 'true', all_vouchers))

	for voucher in inactive_vouchers:
		try:
			requests.request("DELETE",f"https://{IP}/rest/ip/hotspot/user/{voucher['name']}",auth=(admin,password),verify=False)
		except:
			frappe.throw(_(f"Error: The voucher '{voucher['name']}' could not be deleted."))
	frappe.msgprint(_(f"Vouchers deleted successfully."))