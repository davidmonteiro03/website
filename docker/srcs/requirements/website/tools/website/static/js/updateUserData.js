async function updateUserData(event) {
	event.preventDefault();
	if (csrftoken === null) return;
	const form_data = new FormData(event.target);
	const response = await fetch('/backend/update/', {
		method: 'POST',
		headers: { 'X-CSRFToken': csrftoken },
		body: form_data
	});
	if (!response.ok) return;
	updatePageContent('profilepage');
}
