# Copyright (c) 2024, hassan elsahfei and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ServersTable(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		name1: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		server: DF.Data
		url: DF.Data
	# end: auto-generated types
	pass
