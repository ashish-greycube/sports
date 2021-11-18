import frappe
from frappe import _
from frappe.utils.user import is_website_user




def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True	
	return context

@frappe.whitelist(allow_guest=True)
def set_signature_of_customer(singature_data):	
	user = frappe.session.user
	contact = frappe.db.get_value("Contact", {"user": user}, "name")
	customer = None
	if contact:
		contact_doc = frappe.get_doc("Contact", contact)
		customer = contact_doc.get_link_for("Customer")
		print(is_website_user())
		if customer:
			customer_doc = frappe.get_doc("Customer", customer)
			customer_doc.student_signature_cf=None
			customer_doc.student_signature_cf=singature_data
			customer_doc.save(ignore_permissions = True)		
			return customer_doc.name	
