import frappe.realtime
import requests
import frappe
from frappe import _
from frappe.model.document import Document
from frappe import json

class Vouchers(Document):

    def db_insert(self, *args, **kwargs):
        insert_voucher(self.as_dict())
		
    def db_update(self, *args, **kwargs):
        update_voucher(self.name, self.as_dict())
        self.modified = False

    def update(self, *args, **kwargs):
        return super().update(*args)

    def before_rename(self, old, new, merge=False):
        frappe.throw(_(f"Error: Can not Rename From Here."))

    def delete(args):
        delete_voucher(args.name)

    def load_from_db(self):
        self.modified = False
        voucher = get_voucher(self.name)
        super(Document, self).__init__(voucher)

    @staticmethod
    def get_list(args):
        printData(args.filters)
        vouchers = get_vouchers(args.filters)
        if args.get('as_list'):
            return [tuple(voucher.values()) for voucher in vouchers]
        return vouchers

    @staticmethod
    def get_count(args):
        return ''
    @staticmethod
    def get_stats(args):
        return {}

### FUNCTIONS ###
@frappe.whitelist()
def get_vouchers(filters):
	vouchers = connect_hotspot('GET')
	if vouchers == False:
		frappe.throw(_(f"Error: The hotspot controller is disconnected."))
	else:
		vouchers.pop(0)
		hotspot_controller = frappe.get_doc('Hotspot Controller')
		data_map = lambda v: {'name':v['name'],
							'status': 'Active' if v['disabled'] == 'false' else 'Inactive',
							'uptime': v['uptime'],
							'limit_uptime': extract_time(v['limit-uptime']) if 'limit-uptime' in v else None,
                            'server': hotspot_controller.get_name(v['server']) if 'server' in v else 'الكل',
							"server_name": hotspot_controller.get_name(v['server']) if 'server' in v else "الكل",
							'url': hotspot_controller.get_server_url(v['server']) if 'server' in v else 'http://localhost',
							}
		vouchers_map = list(map(data_map, vouchers))
		if filters == []:
			return vouchers_map
		else:
			vouchers_filter = vouchers_map
			for f in filters:
				if 'status' in f:
					print(f'{f[1]} => {f[-1]}')
					status_filter = list(filter(lambda v: v[f[1]] == f[-1], vouchers_map))
					vouchers_filter = status_filter
				if 'limit_uptime' in f:
					limit_uptime_filter = list(filter(lambda v: v[f[1]] == f[-1], vouchers_filter))
					vouchers_filter = limit_uptime_filter
				# if 'server_name' in f:
				# 	server_name = f[-1].replace('%','')
				# 	server_name_filter = list(filter(lambda v: v[f[1]] == server_name, vouchers_filter))
				# 	vouchers_filter = server_name_filter
				if 'server' in f:
					# server = f[-1].replace('%','')
					server_filter = list(filter(lambda v: v[f[1]] == f[-1], vouchers_filter))
					vouchers_filter = server_filter
			return vouchers_filter
def get_voucher(voucher):
	response  = connect_hotspot('GET',voucher) 
	info_voucher = response
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	if 'server' in info_voucher:
		server = hotspot_controller.get_name(info_voucher['server'])
		if server:
			info_voucher['server'] = server
	else:
		info_voucher['server'] = 'الكل'
	info_voucher['url'] = hotspot_controller.get_server_url(info_voucher['server']) if 'server' in info_voucher else 'http://localhost'
	info_voucher['name1'] = info_voucher['name']
	info_voucher['status'] = 'Active' if info_voucher['disabled'] == 'false' else 'Inactive'
	info_voucher['limit_uptime'] = extract_time(info_voucher['limit-uptime']) if 'limit-uptime' in info_voucher else None
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
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	return {
		"name": data['name1'].replace(' ','_'),
		'disabled': 'false' if data['status'] == 'Active' else 'true',
		'server': hotspot_controller.get_server(data['server']) if data['server'] != 'الكل' else 'all',
		'limit-uptime':  data['limit_uptime'] if data['limit_uptime'] else '00:00:00',
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

def convert_time_format(time_str):
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    
    formatted_time = f"{hours}h{minutes}m{seconds}s"
    return formatted_time

from datetime import datetime
def str_to_time(time_str):
    time_format = "%H:%M:%S"
    time_obj = datetime.strptime(time_str, time_format).time()
    
    return time_obj

### REST API ###
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
	
def GET(ip,admin,password,name=None):
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
			if api.status_code == 400:
				frappe.throw(_(f"Error: {api.status_code} the server ''{data['server']}'' is not found in Hotspot."))
				return False
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
			if api.status_code == 400:
				frappe.throw(_(f"Error: {api.status_code} the server ''{data['server']}'' is not found in Hotspot."))
				return False
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False


### ACTION ###
@frappe.whitelist()
def delete_inactive_vouchers():
	all_vouchers = connect_hotspot("GET")
	inactive_vouchers = list(filter(lambda x: x['disabled'] == 'true', all_vouchers))

	for voucher in inactive_vouchers:
		connect_hotspot("DELETE",voucher['name'])
	frappe.msgprint(_(f"Vouchers Inactive deleted successfully."))


@frappe.whitelist()
def create_printer_voucher(vouchers):
	doc = frappe.new_doc('Vouchers Printer')
	vouchers = json.loads(vouchers)
	if type(vouchers) != list:
		frappe.throw(_(f"ERROR => Type Data is Not Array"))
		return False
	else:
		for voucher in list(vouchers):
			doc.append('vouchers_table', {
				'voucher': voucher['name'],
				'server': voucher['server'],
				'url': voucher['url'],
			})
		doc.insert()
		return doc.name
	



def printData(date):
	print('\n')
	print("*"*20)
	print(date)
	print("*"*20)
	print('\n')