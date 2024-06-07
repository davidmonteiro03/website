async function signUp(event) {
	event.preventDefault();
	if (csrftoken === null || sessiontoken !== null) {
		return;
	}
	// console.log(event.target);
	const form_data = new FormData(event.target);
	const response = await fetch('/backend/signup/', {
		method: 'POST',
		headers: {
			'X-CSRFToken': csrftoken
		},
		body: form_data
	});
	if (!response.ok) {
		return;
	}
	const content = await response.json();
	sessionData['sessiontoken'] = content.sessiontoken;
	sessionData['publicdata'] = content.publicdata;
	sessiontoken = content.sessiontoken;
	$('#signupFormModal').modal('hide');
	updatePageContent();
	changePage(event, 'index');
}
