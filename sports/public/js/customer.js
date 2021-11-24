// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer', {
	refresh: function (frm) {
		if (frm.doc.waiver_terms_cf == undefined) {
			frappe.db.get_single_value('Sports Settings', 'default_waiver_terms')
				.then(default_waiver_terms => {
					if (default_waiver_terms) {
						let template_name = default_waiver_terms
						frappe.db.get_value('Terms and Conditions', default_waiver_terms, 'terms')
						.then(r => {
								console.log(r.message.terms) // Open
								let terms=r.message.terms
								if (terms) {
									frm.set_value('waiver_terms_cf', terms);
								}
						})						
					}
				})
	}
}
});