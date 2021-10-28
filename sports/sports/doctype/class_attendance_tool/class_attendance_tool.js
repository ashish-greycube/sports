// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Class Attendance Tool', {
	refresh: function(frm) {
		frm.disable_save();
		$("span:contains('Not Saved')").hide()
	},
	session_date: function(frm) {
		erpnext.class_attendance_tool.load_students(frm);
	},

	item_code: function(frm) {
		debugger
		erpnext.class_attendance_tool.load_students(frm);
	}	
});

erpnext.class_attendance_tool = {
	load_students: function(frm) {
		if(frm.doc.session_date && frm.doc.item_code) {
			frappe.call({
				
				method: "sports.sports.doctype.class_attendance_tool.class_attendance_tool.get_students",
				args: {
					date: frm.doc.session_date,
					item_code: frm.doc.item_code,
				},
				callback: function(r) {
					if(r.message['unmarked'].length > 0) {
						unhide_field('unmarked_attendance_section')
						if(!frm.employee_area) {
							frm.employee_area = $('<div>')
							.appendTo(frm.fields_dict.students_html.wrapper);
						}
						frm.EmployeeSelector = new erpnext.EmployeeSelector(frm, frm.employee_area, r.message['unmarked'])
					}
					else{
						hide_field('unmarked_attendance_section')
					}

					if(r.message['marked'].length > 0) {
						unhide_field('marked_attendance_section')
						if(!frm.marked_employee_area) {
							frm.marked_employee_area = $('<div>')
								.appendTo(frm.fields_dict.marked_attendance_html.wrapper);
						}
						frm.marked_employee = new erpnext.MarkedEmployee(frm, frm.marked_employee_area, r.message['marked'])
					}
					else{
						hide_field('marked_attendance_section')
					}
				}
			});
		}
	}
}


erpnext.MarkedEmployee = Class.extend({
	init: function(frm, wrapper, customer) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.make(frm, customer);
	},
	make: function(frm, customer) {
		var me = this;
		$(this.wrapper).empty();

		var row;
		$.each(customer, function(i, m) {
			var attendance_icon = "fa fa-check";
			var color_class = "";
			if(m.status == "Absent") {
				attendance_icon = "fa fa-check-empty"
				color_class = "text-muted";
			}
			else if(m.status == "Half Day") {
				attendance_icon = "fa fa-check-minus"
			}

			if (i===0 || i % 4===0) {
				row = $('<div class="row"></div>').appendTo(me.wrapper);
			}

			$(repl('<div class="col-sm-3 %(color_class)s">\
				<label class="marked-student-label"><span class="%(icon)s"></span>\
				%(customer)s</label>\
				</div>', {
					customer: m.customer,
					icon: attendance_icon,
					color_class: color_class
				})).appendTo(row);
		});
	}
});


erpnext.EmployeeSelector = Class.extend({
	init: function(frm, wrapper, customer) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.make(frm, customer);
	},
	make: function(frm, customer) {
		var me = this;

		$(this.wrapper).empty();
		var employee_toolbar = $('<div class="col-sm-12 top-toolbar">\
			<button class="btn btn-default btn-add btn-xs"></button>\
			<button class="btn btn-xs btn-default btn-remove"></button>\
			</div><br>').appendTo($(this.wrapper));

		var mark_employee_toolbar = $('<br><div class="col-sm-12 bottom-toolbar">\
			<button class="btn btn-primary btn-mark-present btn-xs"></button>\
			</div>');

		employee_toolbar.find(".btn-add")
			.html(__('Check all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if(!$(check).is(":checked")) {
						check.checked = true;
					}
				});
			});

		employee_toolbar.find(".btn-remove")
			.html(__('Uncheck all'))
			.on("click", function() {
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						check.checked = false;
					}
				});
			});

		mark_employee_toolbar.find(".btn-mark-present")
			.html(__('Mark Present'))
			.on("click", function() {
				var employee_present = [];
				$(me.wrapper).find('input[type="checkbox"]').each(function(i, check) {
					if($(check).is(":checked")) {
						employee_present.push(customer[i]);
					}
				});
				frappe.call({
					method: "sports.sports.doctype.class_attendance_tool.class_attendance_tool.mark_student_attendance",
					args:{
						"student_list":employee_present,
						"item_code":frm.doc.item_code,
						"session_date":frm.doc.session_date,
					},

					callback: function(r) {
						erpnext.class_attendance_tool.load_students(frm);

					}
				});
			});

		var row;
		$.each(customer, function(i, m) {
			if (i===0 || (i % 4) === 0) {
				row = $('<div class="row"></div>').appendTo(me.wrapper);
				console.log(m)
			}

			$(repl('<div class="col-sm-3 unmarked-student-checkbox">\
				<div class="checkbox">\
				<label><input type="checkbox" class="student-check" title="%(customer)s" customer="%(customer)s"/>\
				%(label_customer)s</label>\
				</div></div>', {customer: m.customer_name,label_customer: m.customer})).appendTo(row);
		});

		mark_employee_toolbar.appendTo($(this.wrapper));
	}
});
