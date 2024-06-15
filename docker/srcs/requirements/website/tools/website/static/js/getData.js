async function getData(event) {
	event.preventDefault();
	if (csrftoken === null) return;
	const response = await fetch('/backend/getdata/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
	});
	if (!response.ok) return;
}
