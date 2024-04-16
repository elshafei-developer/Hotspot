# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import get_time


class HotspotController(Document):
    def get_name(self,server):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.server == server:
                return hotspot_servers.name1
        return None

    def get_server(self,name):
        if name == 'الكل':
            return 'all'
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.name1 == name:
                return hotspot_servers.server
        frappe.throw(_(f"Error: The name `{name}` is not found."))

    def get_limit_uptime(self,name):
        for vouchers_times in self.vouchers_times:
            if vouchers_times.name1 == name:
                return vouchers_times.time
        frappe.throw(_(f"Error: The name `{name}` is not found."))

    def get_limit_uptime_name(self,time):
        time =  get_time(time)
        for vouchers_times in self.vouchers_times:
            if get_time(vouchers_times.time) == time:
                return vouchers_times.name1
        return None

    def get_server_url(self,server):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.server == server:
                return hotspot_servers.url
@frappe.whitelist()
def get_info_table():
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    servers = []
    times = []

    for hotspot_servers in hotspot_controller.hotspot_servers:
        servers.append(hotspot_servers.name1)
    for vouchers_times in hotspot_controller.vouchers_times:
        times.append(vouchers_times.name1)
    obj = {
        "servers":servers,
        "times":times
    }
    return obj

@frappe.whitelist()
def get_server_details(server):
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    if server == 'الكل':
        return 'http://localhost'
    for hotspot_servers in hotspot_controller.hotspot_servers:
        if hotspot_servers.name1 == server:
            return hotspot_servers.url
