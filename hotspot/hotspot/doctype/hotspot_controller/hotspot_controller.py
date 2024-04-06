# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HotspotController(Document):
    def get_company(self,server):
        for hotspot_table in self.hotspot_table:
            if hotspot_table.server == server:
                return hotspot_table.name1
    def get_server(self,company):
        for hotspot_table in self.hotspot_table:
            if hotspot_table.name1 == company:
                return hotspot_table.server
