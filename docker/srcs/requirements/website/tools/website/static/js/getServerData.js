getServerData = async () => {
	let csrftoken = getCookie('csrftoken');
	if (csrftoken === null) return false;
	const response = await fetch('/server-data/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
	});
	if (!response.ok) return null;
	const data = await response.json();
	return data;
};
