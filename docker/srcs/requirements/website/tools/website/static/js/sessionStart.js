async function sessionStart() {
	if (document.cookie === '') {
		return;
	}
	let find_csrf = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (find_csrf === undefined) {
		return;
	}
	csrftoken = find_csrf.split('=')[1];
	let find_session = document.cookie.split('; ').find(row => row.startsWith('sessiontoken'));
	if (find_session === undefined) {
		return;
	}
	sessiontoken = find_session.split('=')[1];
	sessionData['sessiontoken'] = sessiontoken;
	const response = await fetch('/backend/getdata/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({ 'sessiontoken': sessiontoken })
	});
	if (!response.ok) {
		document.cookie = "sessiontoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; secure; samesite=Strict";
		return;
	}
	const content = await response.json();
	sessionData['publicdata'] = content.publicdata;
}
