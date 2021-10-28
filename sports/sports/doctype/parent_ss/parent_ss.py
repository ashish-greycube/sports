# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

class ParentSS(Document):
	@frappe.whitelist()
	def create_parent_user(self):
		user = frappe.get_doc({
			'doctype': 'User',
			'send_welcome_email': 0,
			'email': self.parent_email,
			'first_name': self.parent_name,
			'user_type': 'Website User',
		})
		user.append('roles', {
			'role': 'Parent SS'
		})		
		user.save(ignore_permissions=True)
		update_password_link = user.reset_password()
		self.user=user.name
		print('update_password_link',update_password_link)
		msgprint(_("password reset link {0}").format(update_password_link))
		# https://github.com/frappe/erpnext/blob/develop/erpnext/buying/doctype/request_for_quotation/request_for_quotation.py#L164
		return 