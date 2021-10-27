// Copyright (c) 2016, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Class Enrolment Detail"] = {
	"filters": [
		{
			"fieldname": "customer",
			"fieldtype": "Link",
			"label": "Student",
			"mandatory": 0,
			"options": "Customer",
			"wildcard_filter": 0
		 }
	]
};
