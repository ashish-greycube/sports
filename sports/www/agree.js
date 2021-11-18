frappe.ready(function () {
	// Initialize jSignature
	var $sigdiv = $("#signature").jSignature({
		height: 207,
		color: "var(--text-color)",
		width: 616,
		lineWidth: 2,
		"background-color": "var(--control-bg)"
	});
	$sigdiv.jSignature("reset")
	$('#click').click(function () {
		// Get response of type image
		var data = $sigdiv.jSignature('getData', 'image');
		let button = document.getElementById('click');
		button.disabled = true;
		let set_signature_of_customer = frappe.call({
			method: 'sports.www.agree.set_signature_of_customer',
			args: {
				'singature_data': "data:" + data,
			},
			callback: (response) => {

				customer_doc_message = 'Signature is attached to ' + response.message + "'s  document"
				frappe.msgprint(customer_doc_message);
				button.disabled = false;
			},
			error: (err) => {
				frappe.show_alert("Something went wrong please try again");
				button.disabled = false;
			}
		});
	});
})