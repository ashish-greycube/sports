from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt, has_common
from frappe.utils.user import is_website_user


no_cache = 1

def get_context(context):
	# try:
	# 	program = frappe.form_dict['program']
	# except KeyError:
	# 	frappe.local.flags.redirect_location = '/me'
	# 	raise frappe.Redirect
	context.student_list=get_current_student()
	context.courses = get_data(get_current_student())


def get_current_student():
	"""Returns current student from frappe.session.user

	Returns:
		object: Student Document
	"""
	email = frappe.session.user
	if email in ('Administrator', 'Guest'):
		return None
	# try:
	# 	# check role
	# 	parent_role = frappe.user.has_role('Parent SS')
	# 	customer_role=frappe.user.has_role('Customer')
	# 	print('-'*100)
	# 	print('parent_role,customer_role')
	# 	print(parent_role,customer_role)
	# 	if parent_role:
	# 		pass
	# 	elif customer_role:
	# 		pass
	# 	else:
	# 		return None

	# 	student_id = frappe.get_all("Student", {"student_email_id": email}, ["name"])[0].name
	# 	return frappe.get_doc("Student", student_id)
	# except (IndexError, frappe.DoesNotExistError):
	# 	return None	

	customers = []
	user = frappe.session.user
	if (user != 'Guest' and is_website_user()):
		print('frappe.get_roles(user)',frappe.get_roles(user))
		if has_common(["Parent SS"], frappe.get_roles(user)):
			childrens = frappe.db.sql("""
SELECT  PC.customer 
from `tabParent SS` P inner join `tabParent Children SS` PC 
on P.name=PC.parent
where P.user=%s
				""", user, as_dict=1)			
			for child in childrens:
				customers.append(child.customer)
		elif has_common(["Customer"], frappe.get_roles(user)):
			contacts = frappe.db.sql("""
				select
					`tabContact`.email_id,
					`tabDynamic Link`.link_doctype,
					`tabDynamic Link`.link_name
				from
					`tabContact`, `tabDynamic Link`
				where
					`tabContact`.name=`tabDynamic Link`.parent and `tabContact`.email_id =%s
				""", user, as_dict=1)
			customers = [c.link_name for c in contacts if c.link_doctype == 'Customer']
			# customer_list = frappe.get_all("Customer")
			# customers = [customer.name for customer in customer_list]
		print(customers)
		return customers if customers else None


def get_data(customers):
	data = []
	data = frappe.db.sql("""select SA.customer_name,SA.customer,SA.item_code ,SA.name as session_allocation, 
	SA.total_sessions_allocated as total_session, 
	SA.total_sessions_allocated-IFNULL(sum(SS.session_qty),0) as session_available, 
	IFNULL(sum(SS.session_qty),0) as session_consumed,
	SA.session_valid_till as valid_till
		from `tabSession Allocation SS` SA left outer join `tabSports Session` SS
on SA.name =SS.session_allocation 
where IFNULL(SA.session_valid_till,'2099-12-31') >= CURDATE() 
AND SA.customer in (%s)
group by SA.name 
HAVING session_available>=0
order by SA.session_start_date ASC """ % (','.join(['%s'] * len(customers))), tuple(customers), as_dict=1)	
	return data			