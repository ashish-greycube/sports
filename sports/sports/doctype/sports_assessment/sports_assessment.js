// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sports Assessment', {

	student: function (frm) {
		if (frm.is_new() == 1 && frm.doc.student != undefined) {
			frappe.db.get_single_value('Sports Settings', 'anthropometric_template')
				.then(anthropometric_template => {
					if (anthropometric_template) {
						let template_name = anthropometric_template
						let child_table_name = 'anthroprometric_assessment_detail'
						set_sports_assessment_template_detail(frm, template_name, child_table_name)

					}
				})
			frappe.db.get_single_value('Sports Settings', 'physical_fitness_template')
				.then(physical_fitness_template => {
					if (physical_fitness_template) {
						let template_name = physical_fitness_template
						let child_table_name = 'physical_fitness_assessment_detail'
						set_sports_assessment_template_detail(frm, template_name, child_table_name)
					}
				})
			frappe.db.get_single_value('Sports Settings', 'technical_fitness_template')
				.then(technical_fitness_template => {
					if (technical_fitness_template) {
						let template_name = technical_fitness_template
						let child_table_name = 'technical_fitness_assessment_detail'
						set_sports_assessment_template_detail(frm, template_name, child_table_name)
					}
				})
			frappe.after_ajax().then(
				setTimeout(() => {
					frm.save()
				}, 1000)
			)

		}
	},
});

function set_sports_assessment_template_detail(frm, template_name, child_table_name) {
	frappe.call({
		'method': 'frappe.client.get',
		args: {
			doctype: 'Sports Assessment Template',
			name: template_name
		},
		callback: function (data) {
			let sports_assessment_template_details = data.message.sports_assessment_template_detail
			console.log('sports_assessment_template_details', sports_assessment_template_details)
			for (let index = 0; index < sports_assessment_template_details.length; index++) {
				let row = frm.add_child(child_table_name);

				let d = sports_assessment_template_details[index];
				row.category = d.category
				row.assessment__parameter = d.assessment__parameter
				row.unit_of_measurement = d.unit_of_measurement

			}
			frm.refresh_field(child_table_name)
		}
	});
}