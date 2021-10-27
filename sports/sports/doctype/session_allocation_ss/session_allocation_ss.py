# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.utils import get_url_to_form

class SessionAllocationSS(Document):
	def validate(self):
		existing_record=frappe.db.get_list('Session Allocation SS', filters={'invoice_reference': ['=', self.invoice_reference],'item_code': ['=', self.item_code],'name': ['!=', self.name]},fields=['name'])	
		if len(existing_record)	> 0 :
			msg=_('Session Allocation record <a href=session-allocation-ss/{0}>{0}</a> exists for same class and invoice.').format(existing_record[0].name)
			frappe.throw(msg, title=_("Duplicate Entry"))
