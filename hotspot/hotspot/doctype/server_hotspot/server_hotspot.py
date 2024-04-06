    # Copyright (c) 2024, hassan elsahfei and contributors
    # For license information, please see license.txt

import frappe
from frappe import _
import requests
from frappe.model.document import Document

class ServerHotspot(Document):

    def db_insert(self, *args, **kwargs):
        insert_server(self.as_dict())
		
    def db_update(self, *args, **kwargs):
        update_server(self.name, self.as_dict())
        self.modified = False
			
    def delete(args):
        delete_server(args.name)
	
    def load_from_db(self):
        self.modified = False
        server = get_server(self.name)
        super(Document, self).__init__(server)

    @staticmethod
    def get_list(args):
        servers = get_servers()
        if args.get('as_list'):
            return [tuple(server.values()) for server in servers]
        return servers
    @staticmethod
    def get_count(args):
        return len(get_servers())

    @staticmethod
    def get_stats(args):
        pass


# ### FUNCTION ###
def get_servers():
	servers = connect_hotspot('GET')
	if servers == False:
		frappe.throw(_(f"Error: The hotspot controller is disconnected."))
	else:
		data_map = lambda s: {
                            'name': s['name'],
                            'status': 'Active' if s['disabled'] == 'false' else 'Inactive',
                            'interface': s['interface'],
                            }
		servers_map = list(map(data_map, servers))
	return servers_map

def get_server(server):
    response  = connect_hotspot('GET',server)
    info_server = response
    info_server['name1'] = info_server['name']
    info_server['status'] = 'Active' if info_server['disabled'] == 'false' else 'Inactive'
    return info_server

def insert_server(data):
	data = server_structure(data)
	connect_hotspot('PUT',data)
	
def update_server(server,data):
	data = server_structure(data)
	connect_hotspot('PATCH',data,server)

def delete_server(server):
	connect_hotspot("DELETE",server)

# structure of server that MikroTik Accept
def server_structure(data):
	return {
		"name": data['name1'].replace(' ','_'),
		'disabled': 'false' if data['status'] == 'Active' else 'true',
		'interface': data['interface'],
	}

### REST API ###
def connect_hotspot(method,data=None,server=None):
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
		return PATCH(ip,admin,password,data,server)
	
def GET(ip,admin,password,name=None):
	if name:
		try:
			api = requests.request("GET",f"https://{ip}/rest/ip/hotspot/{name}",auth=(admin,password),verify=False)
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
			api = requests.request("GET",f"https://{ip}/rest/ip/hotspot",auth=(admin,password),verify=False)
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
		frappe.throw(_(f"Error: The Server could not be created Empty."))
	# server_exists(data['name'])
	try:
		api = requests.request("PUT",f"https://{ip}/rest/ip/hotspot",auth=(admin,password),json=data,verify=False)
		if api.status_code == 201:
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False

def DELETE(ip,admin,password,server):
	if server == None:
		frappe.throw(_(f"Error: A name server must be given to delete the server"))
	try:
		api = requests.request("DELETE",f"https://{ip}/rest/ip/hotspot/{server}",auth=(admin,password),verify=False)
		if api.status_code == 204:
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False
	
def PATCH(ip,admin,password,data,server):
	if server == None:
		frappe.throw(_(f"Error: A name must be given to Update the Voucher"))
	# server_exists(data['name'],voucher)
	try:
		api = requests.request("PATCH",f"https://{ip}/rest/ip/hotspot/{server}",auth=(admin,password),verify=False,json=data)
		if api.status_code == 200:
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code}"))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False
