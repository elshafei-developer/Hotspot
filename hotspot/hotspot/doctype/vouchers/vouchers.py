import requests
import frappe
from frappe import _
from frappe.model.document import Document

class Vouchers(Document):

	def db_insert(self, *args, **kwargs):
		insert_voucher(self.as_dict())

	def db_update(self, *args, **kwargs):
		update_voucher(self.name, self.as_dict())
		self.modified = False
		
	def delete(args):
		delete_voucher(args.name)
	
	def load_from_db(self):
		self.modified = False
		voucher = get_info_voucher(self.name)
		voucher['name1'] = voucher['name']
		if 'limit-uptime' in voucher:
			voucher['limit_uptime'] = extract_time(voucher['limit-uptime'])
		super(Document, self).__init__(voucher)
	
	@staticmethod
	def get_list(self, *args):
		return get_all_voucher()

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
		return api.json()
	except:
		frappe.throw(_(f"Error: hotspot is not reachable. Please check the connection and try again."))

def get_info_voucher(user):
	IP = get_IP_hotspot_controller()
	api = requests.request("GET",f"https://{IP.ip}/rest/ip/hotspot/user/{user}",auth=(IP.user,IP.password),verify=False)
	if api.status_code == 200:
		return api.json()
	return frappe.throw(_(f"Error: hotspot is not reachable. Please check the connection and try again."))

def insert_voucher(data):
	data = {
			"name": data['name'],
			'disabled': data['disabled'],
			'limit-uptime': data['limit_uptime'],
			}
	IP = get_IP_hotspot_controller()
	requests.request("PUT",f"https://{IP.ip}/rest/ip/hotspot/user",auth=(IP.user,IP.password),verify=False,json=data)

def delete_voucher(name):
	IP = get_IP_hotspot_controller()
	requests.request("DELETE",f"https://{IP.ip}/rest/ip/hotspot/user/{name}",auth=(IP.user,IP.password),
			verify=False)

def update_voucher(voucher,data):
	data = {
		"name": data['name1'],
		'disabled': data['disabled'],
		'limit-uptime':  '00:00:00' if data['limit_uptime'] == None else data['limit_uptime'],
		}
	IP = get_IP_hotspot_controller()
	requests.request("PATCH",f"https://{IP.ip}/rest/ip/hotspot/user/{voucher}",auth=(IP.user,IP.password),
			verify=False,
			json=data)
	
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