# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import format_duration
from frappe.utils import cint

class HotspotController(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from hotspot.hotspot.doctype.servers_table.servers_table import ServersTable
        from hotspot.hotspot.doctype.times_table.times_table import TimesTable

        hotspot_servers: DF.Table[ServersTable]
        ip: DF.Data
        password: DF.Password
        user: DF.Data
        vouchers_times: DF.Table[TimesTable]
    # end: auto-generated types
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
        frappe.throw(_(f"Error: The name `{name}` is not exit."))

    def get_limit_uptime(self,name):
        for vouchers_times in self.vouchers_times:
            if vouchers_times.name1 == name:
                return format_duration(vouchers_times.duration)
        frappe.throw(_(f"Error: The name `{name}` is not exit."))

    def get_limit_uptime_name(self,duration):
        for vouchers_times in self.vouchers_times:
            if vouchers_times.duration == duration_to_seconde(duration):
                return vouchers_times.name1
        return duration

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
        return 'http://hotspot.amalsharq.net'
    for hotspot_servers in hotspot_controller.hotspot_servers:
        if hotspot_servers.name1 == server:
            return hotspot_servers.url

def duration_to_seconde(duration):
    value = 0
    if "w" in duration:
        val = duration.split("w")
        weeks = val[0]
        value += cint(weeks) * 7 * 24 * 60 * 60
        duration = val[1]
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

@frappe.whitelist()
def check_connection():
    import requests
    try:
        hotspot_controller = frappe.get_single('Hotspot Controller')
        ip = hotspot_controller.ip
        user = hotspot_controller.user
        password = hotspot_controller.get_password()
        response = requests.get(f"http://{ip}/rest/ip/hotspot/user",auth=(user,password))

        if response.status_code == 200:
            return {"status": "true"}
        else:
            return {"status": "ERROR"}
    except Exception as e:
        return False
    