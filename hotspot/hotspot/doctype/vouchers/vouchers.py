import requests
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import json
from frappe.model.mapper import get_mapped_doc


class Vouchers(Document):

	# @frappe.whitelist()
	# def GETT():
	# 	frappe.throw(_(f"Error: The voucher could not be created Empty."))

	def db_insert(self, *args, **kwargs):
		insert_voucher(self.as_dict())
		self.print_templates = 'voucher'

	def db_update(self, *args, **kwargs):
		update_voucher(self.name, self.as_dict())
		self.modified = False

	def update(self, *args, **kwargs):
		return super().update(*args)
	def delete(args):
		delete_voucher(args.name)

	def load_from_db(self):
		self.modified = False
		voucher = get_voucher(self.name)
		super(Document, self).__init__(voucher)
	
	@staticmethod
	def get_list(self, *args, **kwargs):
		vouchers = get_vouchers()
		return vouchers

	@staticmethod
	def get_count(args):
		pass	
	@staticmethod
	def get_stats(args):
		pass

	def print(args):
		frappe.throw(_(f"Error: The voucher could not be printed."))

# FUNCTIONS
@frappe.whitelist()
def get_vouchers():
	vouchers = connect_hotspot('GET')
	if vouchers == False:
		frappe.throw(_(f"Error: The hotspot controller is disconnected."))
	else:
		vouchers.pop(0)
		data_map = lambda v: {'name': v['name'],
							'status': 'Active' if v['disabled'] == 'false' else 'Inactive',
							'uptime': v['uptime'],
							'limit_uptime': extract_time(v['limit-uptime']) if 'limit-uptime' in v else None,
							}
		vouchers_map = list(map(data_map, vouchers))
	return vouchers_map

def get_voucher(voucher):
	response  = connect_hotspot('GET',voucher)
	info_voucher = response
	info_voucher['name1'] = info_voucher['name']
	info_voucher['status'] = 'Active' if info_voucher['disabled'] == 'false' else 'Inactive'
	if 'limit-uptime' in info_voucher:
		info_voucher['limit_uptime'] = extract_time(info_voucher['limit-uptime'])
	return info_voucher
	
def insert_voucher(data):
	data = voucher_structure(data)
	connect_hotspot('PUT',data)

def update_voucher(voucher,data):
	data = voucher_structure(data)
	connect_hotspot('PATCH',data,voucher)

def delete_voucher(voucher):
	connect_hotspot('DELETE',voucher)



def voucher_exists(new_name,old_name=None):
	vouchers = connect_hotspot('GET')
	vouchers_exists = list(map(lambda x: x['name'], vouchers))
	if old_name:
		vouchers_exists.pop(vouchers_exists.index(old_name))
	if new_name in vouchers_exists:
		frappe.throw(_(f"Error: The voucher '{new_name}' already exists."))

# structure of voucher that MikroTik Accept
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

# REST API
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
	
def GET(ip,admin,password,name):
	if name:
		try:
			api = requests.request("GET",f"https://{ip}/rest/ip/hotspot/user/{name}",auth=(admin,password),verify=False)
			if api.status_code == 200:
				return api.json()
			else:
				frappe.throw(_(f"Error: {api.status_code} Not Found"))
				return False
		except requests.exceptions.RequestException as e:
			frappe.throw(_(f"Error: => {e}"))
			return False
	else:
		try:
			api = requests.request("GET",f"https://{ip}/rest/ip/hotspot/user",auth=(admin,password),verify=False)
			if api.status_code == 200:
				return api.json()
			else:
				frappe.throw(_(f"Error: {api.status_code}"))
				return False
		except requests.exceptions.RequestException as e:
			frappe.throw(_(f"Error: => Hotspot Controller is disconnected."))
			return False

def PUT(ip,admin,password,data):
	if data == None:
		frappe.throw(_(f"Error: The voucher could not be created Empty."))
	voucher_exists(data['name'])
	try:
		api = requests.request("PUT",f"https://{ip}/rest/ip/hotspot/user",auth=(admin,password),json=data,verify=False)
		if api.status_code == 201:
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False

def DELETE(ip,admin,password,voucher):
	if voucher == None:
		frappe.throw(_(f"Error: A name Voucher must be given to delete the Voucher"))
	try:
		api = requests.request("DELETE",f"https://{ip}/rest/ip/hotspot/user/{voucher}",auth=(admin,password),verify=False)
		if api.status_code == 204:
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False
	
def PATCH(ip,admin,password,data,voucher):
	if voucher == None:
		frappe.throw(_(f"Error: A name must be given to Update the Voucher"))
	voucher_exists(data['name'],voucher)
	try:
		api = requests.request("PATCH",f"https://{ip}/rest/ip/hotspot/user/{voucher}",auth=(admin,password),verify=False,json=data)
		if api.status_code == 200:
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False



# ## ACTION ## #
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


@frappe.whitelist()
def create_printer_voucher(vouchers):
	doc = frappe.new_doc('Vouchers Printer')
	vouchers = json.loads(vouchers)
	if vouchers == []:
		frappe.throw(_(f"Error: The printer could not be created Empty."))
		return False
	else:
		for voucher in list(vouchers):
			doc.append('vouchers_table', {
				'voucher': voucher,
			})
		doc.insert()

		# frappe.local.response['type'] = 'redirect'
		# frappe.local.response['location'] = f'/desk#Form/vouchers-printer/{doc.name}' # Redirect to the form with the created DocType
		return doc.name


def make_B_from_A(source_name, target_doc=None):
   doclist = get_mapped_doc("Vouchers", source_name, {
      "Vouchers": {
         "doctype": "Vouchers Printer",
         "field_map": {
            "name1": "link_to_A_Document"
         }
      }
   }, target_doc)

   return doclist