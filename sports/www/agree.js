frappe.ready(function () {
	// Initialize jSignature
	var $sigdiv = $("#signature").jSignature({
		height: 207,
		color: "var(--text-color)",
		width: 616,
		lineWidth: 2,
		"background-color": "var(--control-bg)"
	});
	let button = document.getElementById('click');
	let waiver_signed_by_cf = document.getElementById('waiver_signed_by_cf');
	
	if ($('#existing_sign').val()!='None') {
	$sigdiv.jSignature('setData', $('#existing_sign').val());
	button.disabled = true;
	waiver_signed_by_cf.disabled = true;
	}
	$sigdiv.jSignature("reset")
	$('#click').click(function () {
		// Get response of type image
		var data = $sigdiv.jSignature('getData', 'image');
		var waiver_signed_by_cf=$('[data-fieldname="waiver_signed_by_cf"]').val()
		if( $sigdiv.jSignature('getData', 'native').length == 0) {
			frappe.throw(
{    title: __('Signature is mandatory'),
message: __('Please Enter Signature..'),}				
				)
			// alert('Please Enter Signature..');
			return
	 }		
		button.disabled = true;
		let set_signature_of_student = frappe.call({
			method: 'sports.www.agree.set_signature_of_student',
			args: {
				'waiver_signed_by_cf':waiver_signed_by_cf,
				'singature_data': "data:" + data,
			},
			callback: (response) => {

				customer_doc_message = 'Waiver is submitted successfully for ' + response.message + "'s  document"
				frappe.msgprint(customer_doc_message);
				button.disabled = false;
				setTimeout(() => {
				location.reload();
					
				}, 1500);
			},
			error: (err) => {
				frappe.show_alert("Something went wrong please try again");
				button.disabled = false;
			}
		});
	});
})