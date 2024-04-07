# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HotspotController(Document):
    def get_name(self,server):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.server == server:
                return hotspot_servers.name1
    def get_server(self,name):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.name1 == name:
                return hotspot_servers.server
    def get_server_url(self,server):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.server == server:
                return hotspot_servers.url

@frappe.whitelist()
def get_servers():
    hotspot_controller = frappe.get_doc('Hotspot Controller')
    servers = ['الكل']
    for hotspot_servers in hotspot_controller.hotspot_servers:
        servers.append(hotspot_servers.name1)
    return servers
