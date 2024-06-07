async function signIn(event) {
	event.preventDefault();
	if (csrftoken === null || sessiontoken !== null) {
		return;
	}
	const form_data = new FormData(event.target);
	const json_data = {};
	for (const [key, value] of form_data.entries()) {
		json_data[key] = value;
	}
	const response = await fetch('/backend/signin/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(json_data)
	});
	if (!response.ok) {
		return;
	}
	const content = await response.json();
	sessionData['sessiontoken'] = content.sessiontoken;
	sessionData['publicdata'] = content.publicdata;
	sessiontoken = content.sessiontoken;
	$('#signinFormModal').modal('hide');
	updatePageContent();
	changePage(event, 'index');
}
