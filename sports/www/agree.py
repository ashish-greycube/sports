import frappe
from frappe import _
from frappe.utils.user import is_website_user




def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False	
	context.student = get_student()
	context.waiver_terms=get_default_waiver_terms()
	context.student_signature_cf=get_student_value('student_signature_cf')
	context.waiver_signed_by_cf=get_student_value('waiver_signed_by_cf')
	context.title='Waiver Sign-Off'
	print('waiver_signed_by_cf',context.waiver_signed_by_cf,	context.student_signature_cf)
	context.parents = [{'title': _('Student Account'), 'route': 'student_account' }]
	return context



@frappe.whitelist(allow_guest=True)
def set_signature_of_student(waiver_signed_by_cf,singature_data):	
	user = frappe.session.user
	contact = frappe.db.get_value("Contact", {"user": user}, "name")
	customer = None
	if contact:
		contact_doc = frappe.get_doc("Contact", contact)
		customer = contact_doc.get_link_for("Customer")
		print(is_website_user())
		if customer:
			customer_doc = frappe.get_doc("Customer", customer)
			customer_doc.waiver_signed_by_cf=waiver_signed_by_cf
			customer_doc.student_signature_cf=singature_data
			customer_doc.save(ignore_permissions = True)		
			return customer_doc.name	

def get_student():
	return frappe.get_value("Customer",{"email_id": frappe.session.user}, "name")

def get_default_waiver_terms():
	waiver_terms_name= frappe.db.get_single_value('Sports Settings', 'default_waiver_terms')
	return frappe.db.get_value('Terms and Conditions', waiver_terms_name,'terms')


def get_student_value(field_name):
	user = frappe.session.user
	contact = frappe.db.get_value("Contact", {"user": user}, "name")
	customer = None
	if contact:
		contact_doc = frappe.get_doc("Contact", contact)
		customer = contact_doc.get_link_for("Customer")
		if customer:
			customer_doc = frappe.get_doc("Customer", customer)
			if customer_doc.get(field_name):
				return customer_doc.get(field_name)
			else:
				return None
