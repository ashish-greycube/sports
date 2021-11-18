from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils import cstr
import pyqrcode 
import io

def validate_and_create_qrcode(self,method):
		if not self.qr_code_cf and self.customer_name:
			url = pyqrcode.create(self.customer_name)
			buffer = io.BytesIO()
			url.svg(buffer)
			_file = frappe.get_doc({
				"doctype": "File",
				"file_name": "%s.svg" % frappe.generate_hash()[:8],
				"attached_to_doctype": self.doctype,
				"attached_to_name": self.name,
				"content": buffer.getvalue()
			})
			_file.save()
			self.qr_code_cf=_file.file_url			
		elif self.customer_name :
			file_exists=frappe.db.get_all('File', filters={'file_url': ['=', cstr(self.qr_code_cf)]})
			if len(file_exists)==0:			
				url = pyqrcode.create(self.customer_name)
				buffer = io.BytesIO()
				url.svg(buffer)
				_file = frappe.get_doc({
					"doctype": "File",
					"file_name": "%s.svg" % frappe.generate_hash()[:8],
					"attached_to_doctype": self.doctype,
					"attached_to_name": self.name,
					"content": buffer.getvalue()
				})
				_file.save()
				self.qr_code_cf=_file.file_url	