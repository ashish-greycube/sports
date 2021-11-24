// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sports Assessment', {
	set_sports_assessment_template_detail: function (frm, template_name, child_table_name) {
		frappe.call({
			'method': 'frappe.client.get',
			args: {
				doctype: 'Sports Assessment Template',
				name: template_name
			},
			callback: function (data) {
				frm.set_value(child_table_name, data.message.sports_assessment_template_detail);
			}
		});
	},
	onload: function (frm) {
		if (frm.is_new() == 1) {
			frappe.db.get_single_value('Sports Settings', 'anthropometric_template')
				.then(anthropometric_template => {
					if (anthropometric_template) {
						let template_name = anthropometric_template
						let child_table_name = 'anthroprometric_assessment_detail'
						frm.events.set_sports_assessment_template_detail(frm, template_name, child_table_name);
					}
				})
			frappe.db.get_single_value('Sports Settings', 'physical_fitness_template')
				.then(physical_fitness_template => {
					if (physical_fitness_template) {
						let template_name = physical_fitness_template
						let child_table_name = 'physical_fitness_assessment_detail'
						frm.events.set_sports_assessment_template_detail(frm, template_name, child_table_name);
					}
				})
			frappe.db.get_single_value('Sports Settings', 'technical_fitness_template')
				.then(technical_fitness_template => {
					if (technical_fitness_template) {
						let template_name = technical_fitness_template
						let child_table_name = 'technical_fitness_assessment_detail'
						frm.events.set_sports_assessment_template_detail(frm, template_name, child_table_name);
					}
				})
		}
	}
});