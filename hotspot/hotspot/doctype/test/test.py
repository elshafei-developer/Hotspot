# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

import requests
import frappe
from frappe.model.document import Document



class table(Document):
    pass
	# def before_save(self):
	# 	self.table = []
	# def onload(self):
	# 	self.append("child",{"name1":"sgwrwwrfwrfwwrfw","password": "my remarks"})

#     print("#"*10)
#     print("table")
#     print("#"*10)
#     """This is a virtual doctype controller for demo purposes.

#     - It uses a single JSON file on disk as "backend".
#     - Key is docname and value is the document itself.

#     Example:
#     {
#             "doc1": {"name": "doc1", ...}
#             "doc2": {"name": "doc2", ...}
#     }
#     """
#     DATA_FILE = {
#         'doc1': {"name": "doc1", "name1": "name1"},
#         "doc2": {"name": "doc2", "name1": "name2"}
# 	}
    
#     @staticmethod
#     def get_all_users():
#      api = requests.request("GET","https://192.168.88.1/rest/ip/hotspot/user",auth=('admin','123'),verify=False)
#      return api.json()

    
	
#     @staticmethod
#     def get_current_data() -> dict[str, dict]:
#         """Read data from disk"""
#         if not os.path.exists(table.DATA_FILE):
#             return {}

#         with open(table.DATA_FILE) as f:
#             return json.load(f)

#     @staticmethod
#     def update_data(data: dict[str, dict]) -> None:
#         """Flush updated data to disk"""
#         with open(table.DATA_FILE, "w+") as data_file:
#             json.dump(data, data_file)

#     def db_insert(self, *args, **kwargs):
#         d = self.get_valid_dict(convert_dates_to_str=True)

#         data = self.get_current_data()
#         data[d.name] = d

#         self.update_data(data)

#     def load_from_db(self):
#         data = self.get_current_data()
#         d = data.get(self.name)
#         super(Document, self).__init__(d)

#     def db_update(self, *args, **kwargs):
#         # For this example insert and update are same operation,
#         # it might be  different for you.
#         self.db_insert(*args, **kwargs)

#     def delete(self):
#         data = self.get_current_data()
#         data.pop(self.name, None)
#         self.update_data(data)

#     @staticmethod
#     def get_list(args):
#         api = requests.request("GET","https://192.168.88.1/rest/ip/hotspot/user",auth=('admin','123'),verify=False)
#         # data = table.get_current_data()
#         print(api.json())
#         return api.json()

#     @staticmethod
#     def get_count(args):
#         data = table.get_current_data()
#         return len(data)

#     @staticmethod
#     def get_stats(args):
#         return {}

# 	# @frappe.whitelist()
# @staticmethod
# def get_all_users():
# 	api = requests.request("GET","https://192.168.88.1/rest/ip/hotspot/user",auth=('admin','123'),verify=False)
# 	return api.json()