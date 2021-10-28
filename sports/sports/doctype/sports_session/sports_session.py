# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.utils import get_url_to_form,cint

class SportsSession(Document):
	def after_insert(self):
		session_consumed = frappe.db.get_value('Session Allocation SS', self.session_allocation, 'session_consumed')
		session_consumed=cint(session_consumed)+cint(self.session_qty)
		doc = frappe.get_doc('Session Allocation SS', self.session_allocation)
		doc.session_consumed =  cint(session_consumed)
		doc.save(ignore_permissions=True)		

	def on_trash(self):
		session_consumed = frappe.db.get_value('Session Allocation SS', self.session_allocation, 'session_consumed')
		session_consumed=cint(session_consumed)-cint(self.session_qty)
		doc = frappe.get_doc('Session Allocation SS', self.session_allocation)
		doc.session_consumed =  cint(session_consumed)
		doc.save(ignore_permissions=True)				

	def validate(self):
			existing_record=frappe.db.get_list('Sports Session', filters={'session_allocation': ['=', self.session_allocation],'session_date': ['=', self.session_date],'name': ['!=', self.name]},fields=['name']) 
			if len(existing_record) > 0 :
					msg=_('Sports Session <a href=sports-session/{0}>{0}</a> exists for same student, class and date.').format(existing_record[0].name)
					frappe.throw(msg, title=_("Duplicate Entry"))
