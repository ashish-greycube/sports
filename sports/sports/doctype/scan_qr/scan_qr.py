# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document
from frappe.utils import nowdate,getdate,today

class ScanQR(Document):
	pass

def book_attendance(session_allocation,customer,item_code,total_sessions_allocated):
	doc = frappe.new_doc('Sports Session')
	doc.naming_series='SSC-.YY.MM.DD.-.#'
	doc.session_allocation= session_allocation
	doc.customer=customer
	doc.customer_name= frappe.db.get_value('Customer', customer, 'customer_name')
	doc.item_code=item_code
	doc.session_date=today()
	doc.total_session_allocated=total_sessions_allocated
	doc.session_qty=1
	doc.save(ignore_permissions=True)
	return doc.name

@frappe.whitelist()
def mark_attendance(scan_qrcode,item_code=None):
		if scan_qrcode:
			if frappe.db.exists('Customer',scan_qrcode):
				if item_code:
					condition="AND SA.item_code='%s'"%(item_code)
				else:
					condition='AND 1=1'
				res = frappe.db.sql("""select SA.customer_name,SA.customer,SA.item_code ,SA.name as session_allocation, 
				SA.total_sessions_allocated as total_session, 
				SA.total_sessions_allocated-IFNULL(sum(SS.session_qty),0) as session_available, 
				IFNULL(sum(SS.session_qty),0) as session_consumed
				 from `tabSession Allocation SS` SA left outer join `tabSports Session` SS
		on SA.name =SS.session_allocation 
		where SA.customer=%(scan_qrcode)s
		and IFNULL(SA.session_valid_till,'2099-12-31') >= CURDATE() 
		{condition}
		group by SA.name 
		HAVING session_available>=0
		order by SA.session_start_date ASC """.format(condition=condition,),{"scan_qrcode": scan_qrcode},as_dict=True)	
				if len(res)==1:
					# book attendance
					attendance_id=book_attendance(session_allocation=res[0].session_allocation,customer=res[0].customer,item_code=res[0].item_code,total_sessions_allocated=res[0].total_session)
					msgprint(_("Attendance <a href=sports-session/{0}>{0}</a> is registerd successfully for class {1}.").format(attendance_id,res[0].item_code), raise_exception=False)
				else:
					class_options=[]
					item_to_compare=res[0].item_code
					class_options.append(item_to_compare)
					different_item=False
					for item in res:
						if item.item_code!=item_to_compare:
							different_item=True
							class_options.append(item.item_code)
					if different_item==False:
						#book attendance
						attendance_id=book_attendance(session_allocation=res[0].session_allocation,customer=res[0].customer,item_code=res[0].item_code,total_sessions_allocated=res[0].total_session)
						msgprint(_("Attendance <a href=sports-session/{0}>{0}</a> is registerd successfully for class {1} and session {2}.").format(attendance_id,res[0].item_code,res[0].session_allocation), raise_exception=False)
					else:
						# populate item_code back
						return class_options
			else:
				msgprint(_("Invalid student QR code"))