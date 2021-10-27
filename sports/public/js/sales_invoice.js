frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm){
		
		if (cint(frm.doc.docstatus==1) && cur_frm.page.current_view_name!=="pos" && !frm.doc.is_return) {
			// && flt(frm.doc.outstanding_amount)=0
			frm.add_custom_button(__('Enroll'), function() {
				make_session_allocation_SS(frm);
			});		
			$('[data-label="Enroll"]').removeClass(' btn-default')
			$('[data-label="Enroll"]').addClass('btn-warning')
	}
}
})

var make_session_allocation_SS = function(frm) {
	frappe.model.open_mapped_doc({
		method: "sports.sales_invoice_controller.make_session_allocation_SS",
		frm: cur_frm
	})	
}