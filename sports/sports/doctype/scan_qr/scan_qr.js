// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scan QR', {
	refresh: function (frm) {
		frm.disable_save()
		$("span:contains('Not Saved')").hide()
	},
	clear_qr_code: function (frm) {
		frm.doc.scan_qrcode = ''
		frm.refresh_field('scan_qrcode')
	},
	scan_qrcode: function (frm) {
		if (frm.doc.scan_qrcode) {
			return frappe.call({
				args: {
					'scan_qrcode': frm.doc.scan_qrcode,
					'item_code': '',
				},
				method: 'sports.sports.doctype.scan_qr.scan_qr.mark_attendance',
				callback: function (r) {
					if (r._server_messages) {
						frm.doc.scan_qrcode = ''
						frm.refresh_field('scan_qrcode')
					} else {
						let class_options = r.message
						frappe.prompt({
							label: __("Select Class"),
							fieldname: 'item_code',
							fieldtype: 'Select',
							options: class_options,
							reqd: 1
						}, (values) => {
							return frappe.call({
								args: {
									'scan_qrcode': frm.doc.scan_qrcode,
									'item_code': values.item_code,
								},
								method: 'sports.sports.doctype.scan_qr.scan_qr.mark_attendance',
								callback: function (r) {
									if (r._server_messages) {
										frm.doc.scan_qrcode = ''
										frm.refresh_field('scan_qrcode')
									}
								}
							})
						})
					}
				}
			});
		}

	}
});