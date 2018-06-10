# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hr_bahrain"
app_title = "Hr Bahrain"
app_publisher = "Hiba Solutions"
app_description = "Hr changes for bahrain"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hafeesk@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hr_bahrain/css/hr_bahrain.css"
# app_include_js = "/assets/hr_bahrain/js/hr_bahrain.js"

# include js, css files in header of web template
# web_include_css = "/assets/hr_bahrain/css/hr_bahrain.css"
# web_include_js = "/assets/hr_bahrain/js/hr_bahrain.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hr_bahrain.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hr_bahrain.install.before_install"
# after_install = "hr_bahrain.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hr_bahrain.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

#doc_events = {
#	"Sales Invoice": {
#		"on_cancel": "hr_bahrain.hr_bahrain.hr_controllers.allocate_annual_leave_monthly"
#	}
#}

doc_events = {
       "Sales Invoice": {
               "on_submit": "hr_bahrain.hr_bahrain.hr_controllers.allocate_annual_leave_monthly"
       }
}


# Scheduled Tasks
# ---------------

scheduler_events = {
 	"hourly": [
 		"hr_bahrain.hr_bahrain.hr_controllers.calculate_gratuity"
	],
}

# Testing
# -------

# before_tests = "hr_bahrain.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hr_bahrain.event.get_events"
# }

fixtures = [ {"dt":"Custom Field", "filters": ["dt", "in", ("HR Settings","Employee")] }] 
