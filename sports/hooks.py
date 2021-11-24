from . import __version__ as app_version

app_name = "sports"
app_title = "Sports"
app_publisher = "GreyCube Technologies"
app_description = "Sports studio management"
app_icon = "octicon octicon-iterations"
app_color = "blue"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sports/css/sports.css"
# app_include_js = "/assets/sports/js/sports.js"

# include js, css files in header of web template
# web_include_css = "/assets/sports/css/sports.css"
web_include_js = "/assets/frappe/js/lib/jSignature.min.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sports/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Sales Invoice" : "public/js/sales_invoice.js",
	"Customer" : "public/js/customer.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"


website_redirects = [
    {"source": "/orders", "target": "/sports_class_detail"},
]

# website user home page (by Role)
role_home_page = {
	"Customer" : "sports_class_detail",
	"Parent SS": "sports_class_detail"
}
portal_menu_items = [
    {"title": "Waiver Sign", "route": "/agree", "role": "Customer"},
		{"title": "My Assessments", "route": "/assessments", "role": "Customer"},
		{"title": "My Class Summary", "route": "/sports_class_detail", "role": "Customer"},
]
# Generators
# ----------

# automatically create page for each record of this doctype
website_generators = ["Sports Assessment"]

# Installation
# ------------

# before_install = "sports.install.before_install"
# after_install = "sports.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sports.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Customer": {
		"validate": "sports.customer_contoller.validate_and_create_qrcode"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sports.tasks.all"
# 	],
# 	"daily": [
# 		"sports.tasks.daily"
# 	],
# 	"hourly": [
# 		"sports.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sports.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sports.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sports.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sports.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sports.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]
website_route_rules = [
	{"from_route": "/assessments", "to_route": "Sports Assessment"}
]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sports.auth.validate"
# ]

