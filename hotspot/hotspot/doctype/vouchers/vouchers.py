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
	def get_list(self, *args, **kwargs):
		vouchers = get_vouchers()
		return vouchers

	@staticmethod
	def get_count(args):
		pass	
	def get_stats(args):
		pass

# FUNCTIONS
def get_vouchers():
	all_vouchers = []
	vouchers = connect_hotspot('GET')
	if vouchers == False:
		frappe.throw(_(f"Error: The hotspot controller is disconnected."))
	else:
		vouchers.pop(0)
		data_map = lambda x: {'name': x['name'],
							'status': 'Active' if x['disabled'] == 'false' else 'Inactive',
							'uptime': x['uptime'],
							'limit_uptime': extract_time(x['limit-uptime']) if 'limit-uptime' in x else None,
							}
		vouchers_map = list(map(data_map, vouchers))
		all_vouchers += vouchers_map
	return all_vouchers

def get_info_voucher(voucher):
	response  = connect_hotspot('GET',voucher)
	if response == False:
		frappe.throw(_(f"Error: The hotspot controller is disconnected."))
	else:
		info_voucher = response
		info_voucher['name1'] = info_voucher['name']
		info_voucher['status'] = 'Active' if info_voucher['disabled'] == 'false' else 'Inactive'
		if 'limit-uptime' in info_voucher:
			info_voucher['limit_uptime'] = extract_time(info_voucher['limit-uptime'])
		return info_voucher
	

def insert_voucher(data):
	# voucher_exists(data['name1'])
	data = voucher_structure(data)
	connect_hotspot('PUT',data)

def update_voucher(voucher,data):
	# voucher_exists(data['name1'],data['name'])
	data = voucher_structure(data)
	connect_hotspot('PATCH',data,voucher)

def delete_voucher(name):
	connect_hotspot('DELETE',name)



def voucher_exists(new_name,old_name=None):
	vouchers = connect_hotspot('GET')
	vouchers_exists = list(map(lambda x: x['name'], vouchers))
	if old_name:
		vouchers_exists.pop(vouchers_exists.index(old_name))
	if new_name in vouchers_exists:
		frappe.throw(_(f"Error: The voucher '{new_name}' already exists."))
	
def voucher_structure(data):
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

def connect_hotspot(method,data=None,voucher=None):
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	ip = hotspot_controller.ip
	admin = hotspot_controller.user
	password = hotspot_controller.password

	if method == 'GET':
		return GET(ip,admin,password,data)
	if method == 'PUT':
		return PUT(ip,admin,password,data)
	if method == 'DELETE':
		return DELETE(ip,admin,password,data)
	if method == 'PATCH':
		return PATCH(ip,admin,password,data,voucher)

# ##### List View ##### #
@frappe.whitelist()
def delete_inactive_vouchers():
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	IP = hotspot_controller.ip
	admin = hotspot_controller.user
	password = hotspot_controller.password
	api = requests.request("GET",f"https://{IP}/rest/ip/hotspot/user",auth=(admin,password),verify=False)
	all_vouchers = api.json()
	all_vouchers.pop(0)
	inactive_vouchers = list(filter(lambda x: x['disabled'] == 'true', all_vouchers))

	for voucher in inactive_vouchers:
		try:
			requests.request("DELETE",f"https://{IP}/rest/ip/hotspot/user/{voucher['name']}",auth=(admin,password),verify=False)
		except:
			frappe.throw(_(f"Error: The voucher '{voucher['name']}' could not be deleted."))
	frappe.msgprint(_(f"Vouchers Inactive deleted successfully."))


def GET(ip,admin,password,voucher):
	if voucher:
		try:
			api = requests.request("GET",f"https://{ip}/rest/ip/hotspot/user/{voucher}",auth=(admin,password),verify=False)
			if api.status_code == 200:
				return api.json()
			else:
				return False
		except requests.exceptions.RequestException as e:
			return False
	else:
		try:
			api = requests.request("GET",f"https://{ip}/rest/ip/hotspot/user",auth=(admin,password),verify=False)
			if api.status_code == 200:
				return api.json()
			else:
				return False
		except requests.exceptions.RequestException as e:
			return False

def PUT(ip,admin,password,data):
	voucher_exists(data['name'])
	if data == None:
		frappe.throw(_(f"Error: The voucher could not be created Empty."))
	try:
		api = requests.request("PUT",f"https://{ip}/rest/ip/hotspot/user",auth=(admin,password),json=data,verify=False)
		if api.status_code == 201:
			return True
		else:
			frappe.throw(_(f"Error: The voucher could not be created."))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False

def DELETE(ip,admin,password,name):
	if name == None:
		frappe.throw(_(f"Error: A name must be given to delete the Voucher"))
	try:
		api = requests.request("DELETE",f"https://{ip}/rest/ip/hotspot/user/{name}",auth=(admin,password),verify=False)
		if api.status_code == 204:
			return True
		else:
			frappe.throw(_(f"Error: The voucher could not be Delete"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False
def PATCH(ip,admin,password,data,voucher):
	voucher_exists(data['name'],voucher)
	if voucher == None:
		frappe.throw(_(f"Error: A name must be given to Update the Voucher"))
	try:
		api = requests.request("PATCH",f"https://{ip}/rest/ip/hotspot/user/{voucher}",auth=(admin,password),verify=False,json=data)
		if api.status_code == 200:
			return True
		else:
			frappe.throw(_(f"Error: The voucher could not be Update."))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False
