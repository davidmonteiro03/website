async function signOut(event) {
	event.preventDefault();
	if (csrftoken === null || sessiontoken === undefined) {
		return;
	}
	const response = await fetch('/backend/signout/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({ 'sessiontoken': sessiontoken })
	});
	if (!response.ok) {
		return;
	}
	const content = await response.json();
	sessiontoken = null;
	sessionData = {};
	updatePageContent();
	changePage(event, 'index');
}
