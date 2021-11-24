# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from erpnext.controllers.website_list_for_contact import get_list_context

class SportsAssessment(WebsiteGenerator):
	_website = frappe._dict(
		template = "sports/doctype/sports_assessment/templates/sports_assessment.html",
		condition_field = "published",
		page_title_field = "title",
	)	


	def autoname(self):
		if not self.title:
			self.title = self.get_title()

	def validate(self):
		if not self.route:		#pylint: disable=E0203
			self.route = "assessments/" + "-".join(self.title.split(" "))


	def get_context(self, context):
		context.read_only = 1
		context.no_cache = 1
		context.show_sidebar = False
		# context.title = self.title
		# context.anthroprometric_assessment_detail=self.anthroprometric_assessment_detail
		context.parents = [{'title': _('Student Account'), 'route': 'student_account' },{'title': _('All My Assessments'), 'route': 'assessments' }]

	def get_title(self):
		return _("Assessment of {0} on {1}").format(self.student,self.assessment_date)


def get_list_context(context=None):
	print('get_list_context'*100)
	# list_context = get_list_context(context)
	# list_context.update({
	# 	'show_sidebar': True,
	# 	'show_search': True,
	# 	'no_breadcrumbs': True,
	# 	'title': _('Student Assessments'),
	# })
	context.update({
		"show_sidebar": False,
		"title": _("Student Assessments"),
		"get_list": get_assessment_list,
		"row_template": "sports/doctype/sports_assessment/templates/sports_assessment_row.html",
		 "parents" :[{'title': _('Student Account'), 'route': 'student_account' }]
	})
def get_assessment_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified"):
	print('get_assessment_list'*100)
	student = get_student()
	print(student)
	return frappe.db.sql('''select name, title, student, modified, location, route,
		assessment_date from `tabSports Assessment` where published=1 and student = %s
		order by assessment_date desc limit {0}, {1}
		'''.format(limit_start, limit_page_length), [student], as_dict=1)	

def get_student():
	return frappe.get_value("Customer",{"email_id": frappe.session.user}, "name")

# def has_website_permission(doc, ptype, user, verbose=False):
# 	if doc.student == get_student():
# 		return True
# 	else:
# 		return False