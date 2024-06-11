async function signOut(event) {
	event.preventDefault();
	if (csrftoken === null) return;
	const response = await fetch('/backend/signout/', {
		method: 'POST',
		headers: { 'X-CSRFToken': csrftoken }
	});
	if (!response.ok) return;
	changePage(event);
	document.title = "AWESOME WEBSITE";
}
