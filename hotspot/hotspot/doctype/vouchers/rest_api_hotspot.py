import frappe
from frappe import _
import requests

def connect_hotspot(method,data=None,voucher=None):
	hotspot_controller = frappe.get_single('Hotspot Controller')
	ip = hotspot_controller.ip

	if method == 'GET':
		return GET(ip,data)
	if method == 'PUT':
		return PUT(ip,data)
	if method == 'DELETE':
		return DELETE(ip,data)
	if method == 'PATCH':
		return PATCH(ip,data,voucher)

def url(method,url,data=None):
    hotspot_controller = frappe.get_single('Hotspot Controller')
    ip = hotspot_controller.ip
    admin = hotspot_controller.user
    password = hotspot_controller.get_password()
    if data:
        return requests.request(method,f"http://{ip}/rest/ip/hotspot/{url}",auth=(admin,password),json=data,verify=False)
    return requests.request(method,f"http://{ip}/rest/ip/hotspot/{url}",auth=(admin,password),verify=False)

def GET(ip,name=None):
	if name:
		try:
			api = url("GET",f"user/{name}")
			if api.status_code == 200:
				return api.json()
			else:
				frappe.throw(_(f"Error: this voucher '{name}' does not exist in hotspot."))
				return False
		except requests.exceptions.RequestException as e:
			frappe.throw(_(f"Error: => {e}"))
			return False
	else:
		try:
			api = url("GET","user")
			if api.status_code == 200:
				filtered_data = [item for item in api.json() if item.get('dynamic') == 'false' and item.get('name') != 'default-trial']
				frappe.cache.set_value(f'hotspot{ip}', filtered_data, expires_in_sec=3600)
				return filtered_data
			else:
				return "ERROR"
		except requests.exceptions.RequestException as e:
			frappe.cache.delete_value(f'hotspot{ip}')
			return False

def PUT(ip,data):
	if data == None:
		frappe.throw(_(f"Error: The voucher could not be created Empty."))
	voucher_exists(data['name'])
	try:
		api = url("PUT","user",data)
		if api.status_code == 201:
			frappe.cache.delete_value(f'hotspot{ip}')
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code} could not create the voucher "))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False

def DELETE(ip,voucher):
	if voucher == None:
		frappe.throw(_(f"Error: A name Voucher must be given to delete the Voucher"))
	try:
		api = url("DELETE",f"user/{voucher}")
		if api.status_code == 204:
			frappe.cache.delete_value(f'hotspot{ip}')
			frappe.publish_realtime("realtime_vouchers",{"message":"delete"})
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code} could not delete this voucher '{voucher}'."))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False

def PATCH(ip,data,voucher):
	if voucher == None:
		frappe.throw(_(f"Error: A name must be given to Update the Voucher"))
	voucher_exists(data['name'],voucher)
	try:
		api = url("PATCH",f"user/{voucher}",data)
		if api.status_code == 200:
			frappe.cache.delete_value(f'hotspot{ip}')
			return True
		else:
			frappe.throw(_(f"Error: {api.status_code} could not update this voucher '{voucher}'."))
			return False
	except requests.exceptions.RequestException as e:
		frappe.throw(_(f"Error: => {e}"))
		return False

## FUNCTION ##
def voucher_exists(new_name,old_name=None):
	vouchers = connect_hotspot('GET')
	vouchers_exists = list(map(lambda x: x['name'], vouchers))
	if old_name:
		vouchers_exists.pop(vouchers_exists.index(old_name))
	if new_name in vouchers_exists:
		frappe.throw(_(f"Error: The voucher '{new_name}' already exists."))
		

