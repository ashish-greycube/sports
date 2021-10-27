# Copyright (c) 2013, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	if not filters: filters = {}
	columns, data = [], []
	columns=get_columns()
	data = get_data(filters)
	return columns, data
def get_columns():
	return [
  {
   "fieldname": "customer",
   "fieldtype": "Link",
   "label": "Student",
   "options": "Customer",
   "width": 150
  },
  {
   "fieldname": "item_code",
   "fieldtype": "Link",
   "label": "Class",
   "options": "Item",
   "width": 250
  },
  {
   "fieldname": "total_session",
   "fieldtype": "Int",
   "label": "Total Sessions",
   "width": 150
  },
  {
   "fieldname": "session_consumed",
   "fieldtype": "Int",
   "label": "Consumed Sessions",
   "width": 150
  },
  {
   "fieldname": "session_available",
   "fieldtype": "Int",
   "label": "Available Sessions",
   "width": 150
  },
  {
   "fieldname": "valid_till",
   "fieldtype": "Date",
   "label": "Valid Till",
   "width": 100
  }
		]

def get_data(filters):
	if filters.get("customer"):
		condition="AND SA.customer='%s'"%(filters.get("customer"))
	else:
		condition='AND 1=1'


	data = []
	data = frappe.db.sql("""select SA.customer_name,SA.customer,SA.item_code ,SA.name as session_allocation, 
	SA.total_sessions_allocated as total_session, 
	SA.total_sessions_allocated-IFNULL(sum(SS.session_qty),0) as session_available, 
	IFNULL(sum(SS.session_qty),0) as session_consumed,
	SA.session_valid_till as valid_till
		from `tabSession Allocation SS` SA left outer join `tabSports Session` SS
on SA.name =SS.session_allocation 
where IFNULL(SA.session_valid_till,'2099-12-31') >= CURDATE() 
{condition}
group by SA.name 
HAVING session_available>=0
order by SA.session_start_date ASC """.format(condition=condition,),as_dict=True)		
	return data	