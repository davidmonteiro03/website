async function updateUserData(event) {
	event.preventDefault();
	if (csrftoken === null) return;
	const form_data = new FormData(event.target);
	const json_data = {};
	form_data.forEach((value, key) => { json_data[key] = value; });
	const response = await fetch('/backend/update/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(json_data)
	});
	if (!response.ok) return;
	updatePageContent('profilepage');
}
