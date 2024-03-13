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
		voucher['name1'] = voucher['name']
		voucher['status'] = 'Active' if voucher['disabled'] == 'false' else 'Inactive'
		if 'limit-uptime' in voucher:
			voucher['limit_uptime'] = extract_time(voucher['limit-uptime'])
		super(Document, self).__init__(voucher)
	
	@staticmethod
	def get_list(self, *args):
		all_vouchers = get_all_voucher()

		return all_vouchers

	@staticmethod
	def get_count(args):
		pass	

	@staticmethod
	def get_stats(args):
		pass

# FUNCTIONS
def get_all_voucher():
	frappe.db.commit()
	IP = get_IP_hotspot_controller()
	try:
		api = requests.request("GET",f"https://{IP.ip}/rest/ip/hotspot/user",auth=(IP.user,IP.password),verify=False)
		all_vouchers = api.json()
		all_vouchers.pop(0)
		map_lambda = lambda x: {'name': x['name'],
								'status': 'Active' if x['disabled'] == 'false' else 'Inactive',
								'uptime': x['uptime']}
		all_vouchers_map = list(map(map_lambda, all_vouchers))
		return all_vouchers_map
	except:
		frappe.throw(_(f"Error: hotspot is not reachable. Please check the connection and try again."))

def get_info_voucher(user):
	IP = get_IP_hotspot_controller()
	api = requests.request("GET",f"https://{IP.ip}/rest/ip/hotspot/user/{user}",auth=(IP.user,IP.password),verify=False)
	if api.status_code == 200:
		return api.json()

def insert_voucher(data):
	voucher_exists(data['name1'])
	IP = get_IP_hotspot_controller()
	data = {
			"name": data['name'].replace(' ', '_'),
			'disabled':'false' if  data['status'] == 'Active' else 'true',
			'limit-uptime':  '00:00:00' if data['limit_uptime'] == None else data['limit_uptime'],
			}
	requests.request("PUT",f"https://{IP.ip}/rest/ip/hotspot/user",auth=(IP.user,IP.password),verify=False,json=data)

def delete_voucher(name):
	IP = get_IP_hotspot_controller()
	requests.request("DELETE",f"https://{IP.ip}/rest/ip/hotspot/user/{name}",auth=(IP.user,IP.password),
			verify=False)

def update_voucher(voucher,data):
	voucher_exists(data['name1'],data['name'])
	data = {
		"name": data['name1'].replace(' ','_'),
		'disabled': 'false' if data['status'] == 'Active' else 'true',
		'limit-uptime':  '00:00:00' if data['limit_uptime'] == None else data['limit_uptime'],
		}
	IP = get_IP_hotspot_controller()
	requests.request("PATCH",f"https://{IP.ip}/rest/ip/hotspot/user/{voucher}",auth=(IP.user,IP.password),
			verify=False,
			json=data)

def voucher_exists(new_name,old_name=None):
	IP = get_IP_hotspot_controller()
	api = requests.request("GET",f"https://{IP.ip}/rest/ip/hotspot/user",auth=(IP.user,IP.password),verify=False)
	all_vouchers = api.json()
	vouchers_exists = list(map(lambda x: x['name'], all_vouchers))
	if old_name:
		vouchers_exists.pop(vouchers_exists.index(old_name))
	if new_name in vouchers_exists:
		return frappe.throw(_(f"Error: The voucher '{new_name}' already exists."))

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

def get_IP_hotspot_controller():
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	IP_hotspot_controller = hotspot_controller.as_dict()
	return IP_hotspot_controller