import frappe
from frappe import _
from .rest_api_hotspot import connect_hotspot
import json
from frappe.utils import random_string

### ACTION ###

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
                "limit_uptime": voucher['limit_uptime'],
			})
		doc.insert()
		return doc.name

@frappe.whitelist()
def delete_inactive_vouchers_background():
    frappe.enqueue(delete_inactive_vouchers)
def delete_inactive_vouchers():
    frappe.publish_realtime("realtime_vouchers", {
        "message": f"Will delete all inactive vouchers...",
        "indicator": "blue",
        "title": "Deleting Inactive Vouchers",
    })
    all_vouchers = connect_hotspot("GET")
    inactive_vouchers = list(filter(lambda x: x['disabled'] == 'true', all_vouchers))
    if len(inactive_vouchers) == 0:
        frappe.publish_realtime("realtime_vouchers", {
            "message": f"No Inactive Vouchers Found",
            "indicator": "green",
            "title": "No Inactive Vouchers",
        })
        return False
    for voucher in inactive_vouchers:
        connect_hotspot("DELETE",voucher['name'])
    frappe.publish_realtime("realtime_vouchers", {
        "message": f"Successfully Deleted All Inactive Vouchers",
        "indicator": "green",
        "title": "Deleted Inactive Vouchers",
    })

@frappe.whitelist()
def crete_vouchers_background(number_vouchers,server,limit_uptime,create_print):
    if create_print == 'true':
        frappe.enqueue(create_vouchers_with_print,number_vouchers=number_vouchers,server=server,limit_uptime=limit_uptime)
    else:
        frappe.enqueue(create_vouchers,number_vouchers=number_vouchers,server=server,limit_uptime=limit_uptime)
def create_vouchers(number_vouchers,server,limit_uptime):
    frappe.publish_realtime("realtime_vouchers", {
		"message": f"Creating {number_vouchers} Vouchers for {server} server...",
		"indicator": "blue",
		"title": "Creating Vouchers",
    })
    vouchers = []
    for voucher in range(int(number_vouchers)):
        data = {
            "name1": server + random_string(3),
            'status': 'Active' ,
            'server':  server,
            'limit_uptime':  limit_uptime,
        }
        insert_voucher(data)
        vouchers.append(data)
    frappe.publish_realtime("realtime_vouchers", {
        "message": f"Successfully Created {number_vouchers} Vouchers.",
        "indicator": "green",
        "title": "Created Vouchers",
    })
    return vouchers
def create_vouchers_with_print(number_vouchers,server,limit_uptime):
    frappe.publish_realtime("realtime_vouchers", {
		"message": f"Creating {number_vouchers} Vouchers for {server} server...",
		"indicator": "blue",
		"title": "Creating Vouchers",
    })
    vouchers = []
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    for voucher in range(int(number_vouchers)):
        data = {
            "name1": server + random_string(3),
            'status': 'Active' ,
            'server':  server,
            'limit_uptime':  limit_uptime,
        }
        vouchers.append(data)
        insert_voucher(data)
    doc = frappe.new_doc('Vouchers Printer')
    for v in list(vouchers):
            name = v['name1'].replace(' ','_')    
            server = hotspot_controller.get_server(v['server'])
            server_name = v['server']
            url = hotspot_controller.get_server_url(server)
            doc.append('vouchers_table', {
                'voucher': name,
                'server':server_name,
                'url':url,
                "limit_uptime": limit_uptime,
            })
    doc.insert()
    frappe.publish_realtime("realtime_vouchers", {
        "message": f'<a href=" vouchers-printer/{doc.name}"> Successfully Created {number_vouchers} Vouchers for {server_name} server With Vouchers Printer  {doc.name} <b>Click for View</b></a>',
        "indicator": "green",
        "title": "Created Vouchers",
		"name_doc":  doc.name,
    })
    return vouchers

@frappe.whitelist()
def clear_cache():
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    ip = hotspot_controller.ip
    print("CEARE CHACHE")
    frappe.cache.delete_value(f'hotspot{ip}')
    return True

## FUNCTION ##
def voucher_structure(data):
	"""
	structure of voucher that MikroTik Accept
	"""
	hotspot_controller = frappe.get_doc('Hotspot Controller')
	time = hotspot_controller.get_limit_uptime(data['limit_uptime']) if data['limit_uptime'] else '00:00:00'
	comment = {
		"owner": data['owner'] if 'owner' in data else frappe.session.user,
		"creation": data['creation'] if 'creation' in data else frappe.utils.now_datetime().strftime('%Y-%m-%d %H:%M:%S'),
		"modified": data['modified'] if 'modified' in data else frappe.utils.now_datetime().strftime('%Y-%m-%d %H:%M:%S'),
		"modified_by": data['modified_by'] if 'modified_by' in data else frappe.session.user,
    }
	comment = json.dumps(comment)
	return {
		"name": data['name1'].replace(' ','_'),
		'disabled': 'false' if data['status'] == 'Active' else 'true',
		'server': hotspot_controller.get_server(data['server']) if data['server'] != 'الكل' else 'all',
		'limit-uptime':  convert_time_format(time),
		"comment": f"{comment}",
	}
def convert_time_format(time_str):
    parts = str(time_str).split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    
    formatted_time = f"{hours}h{minutes}m{seconds}s"
    return formatted_time
def insert_voucher(data):
    data = voucher_structure(data)  
    connect_hotspot('PUT',data)