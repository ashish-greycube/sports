from __future__ import unicode_literals

import frappe
from frappe import _, msgprint, throw
from frappe.model.mapper import get_mapped_doc
from frappe.utils import add_days

@frappe.whitelist()
def make_session_allocation_SS(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.session_start_date=source.posting_date
		items=source.get('items')
		target.item_code=items[0].item_code
		target.description=items[0].description
		target.total_sessions_allocated=frappe.db.get_value('Item', target.item_code, 'no_of_sessions_cf')
		target.mobile_no=frappe.db.get_value('Customer', source.customer, 'mobile_no')
		target.student_email=frappe.db.get_value('Customer', source.customer, 'email_id')
		period_in_days_cf=frappe.db.get_value('Item', target.item_code, 'period_in_days_cf')
		if period_in_days_cf!=0:
			target.session_valid_till=add_days(source.posting_date,period_in_days_cf)

	doclist = get_mapped_doc("Sales Invoice", source_name, 	{
		"Sales Invoice": {
			"doctype": "Session Allocation SS",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"customer": "customer",
				"customer_name": "customer_name",
				"invoice_reference": "name",
				"session_start_date": "posting_date"
			},			
		},

	}, target_doc,set_missing_values)
	return doclist