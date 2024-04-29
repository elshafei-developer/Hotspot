# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import format_duration
from frappe.utils import cint

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
                return format_duration(vouchers_times.duration)
        frappe.throw(_(f"Error: The name `{name}` is not found."))

    def get_limit_uptime_name(self,duration):
        for vouchers_times in self.vouchers_times:
            if vouchers_times.duration == duration_to_seconde(duration):
                return vouchers_times.name1
        return None

    def get_server_url(self,server):
        for hotspot_servers in self.hotspot_servers:
            if hotspot_servers.server == server:
                return hotspot_servers.url
@frappe.whitelist()
def get_info_table():
    hotspot_controller = frappe.get_single('Hotspot Controller')
    servers = []
    times = []

    for hotspot_servers in hotspot_controller.hotspot_servers:
        servers.append(hotspot_servers.name1)
    for vouchers_times in hotspot_controller.vouchers_times:
        times.append(vouchers_times.name1)
    return {
        "servers":servers,
        "times":times
    }

@frappe.whitelist()
def get_server_details(server):
    hotspot_controller = frappe.get_single('Hotspot Controller')
    if server == 'الكل':
        return 'http://localhost'
    for hotspot_servers in hotspot_controller.hotspot_servers:
        if hotspot_servers.name1 == server:
            return hotspot_servers.url

def duration_to_seconde(duration):
    value = 0
    if "d" in duration:
        val = duration.split("d")
        days = val[0]
        value += cint(days) * 24 * 60 * 60
        duration = val[1]
    if "h" in duration:
        val = duration.split("h")
        hours = val[0]
        value += cint(hours) * 60 * 60
        duration = val[1]
    if "m" in duration:
        val = duration.split("m")
        mins = val[0]
        value += cint(mins) * 60
        duration = val[1]
    if "s" in duration:
        val = duration.split("s")
        secs = val[0]
        value += cint(secs)
    
    return value
