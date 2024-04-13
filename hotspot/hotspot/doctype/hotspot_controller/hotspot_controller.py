# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


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

    def get_server_url(self,server):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.server == server:
                return hotspot_servers.url
        # frappe.throw(_(f"Error: The server `{server}` is not found."))

@frappe.whitelist()
def get_servers():
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    servers = []
    for hotspot_servers in hotspot_controller.hotspot_servers:
        servers.append(hotspot_servers.name1)
    return servers

@frappe.whitelist()
def get_server_details(server):
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    if server == 'الكل':
        return 'http://localhost'
    for hotspot_servers in hotspot_controller.hotspot_servers:
        if hotspot_servers.name1 == server:
            return hotspot_servers.url