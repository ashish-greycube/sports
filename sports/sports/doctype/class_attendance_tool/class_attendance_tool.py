# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class ClassAttendanceTool(Document):
	pass

@frappe.whitelist()
def get_students(date, item_code):
	attendance_not_marked = []
	attendance_marked = []
	active_students = frappe.db.sql("""select SA.customer,SA.customer_name,SA.total_sessions_allocated-IFNULL(sum(SS.session_qty),0) as session_available				
		from `tabSession Allocation SS` SA left outer join `tabSports Session` SS
		on SA.name =SS.session_allocation 
		where SA.item_code=%(item_code)s
		and IFNULL(SA.session_valid_till,'2099-12-31') >= CURDATE() 
		group by SA.name 
		HAVING session_available>=0
		order by SA.session_start_date ASC """,{"item_code": item_code},as_dict=True)		

	student_attended=	frappe.db.sql("""select customer,customer_name 
from `tabSports Session` SS
where session_date=%(date)s
and item_code =%(item_code)s """,{"date":date,"item_code": item_code},as_dict=True)

	for student in student_attended:
		attendance_marked.append(student)

	for student in active_students:
		student.pop('session_available')
		if (student not in attendance_marked ) and (student not in attendance_not_marked) :
			attendance_not_marked.append(student)	
	return {
		"marked": attendance_marked,
		"unmarked": attendance_not_marked
	}

@frappe.whitelist()
def mark_student_attendance(student_list, item_code, session_date):

	student_list = json.loads(student_list)
	print('student_list',student_list)
	for student in student_list:
		session_allocation_ss=frappe.db.sql("""select name,total_sessions_allocated from `tabSession Allocation SS`
where customer=%(customer)s
and item_code=%(item_code)s
and IFNULL(session_valid_till,'2099-12-31') >= CURDATE()
order by session_start_date ASC limit 1 """,{"customer":student.get('customer'),"item_code": item_code},as_dict=True)
		session_allocation=session_allocation_ss[0].name
		total_session_allocated=session_allocation_ss[0].total_session_allocated
		attendance=frappe.get_doc(dict(
			doctype='Sports Session',
			session_allocation=session_allocation,
			customer=student.get('customer'),
			customer_name=student.get('customer_name'),
			session_date=getdate(session_date),
			item_code=item_code,
			total_session_allocated=total_session_allocated,
			session_qty=1
		))
		attendance.insert()
		# attendance.submit()	