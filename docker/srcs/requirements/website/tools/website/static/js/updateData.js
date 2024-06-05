async function updateData(event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const data = {};
	for (const [key, value] of formData.entries()) {
		data[key] = value;
	}
	const all_data = {
		'user_data': sessionData['user_data'],
		'new_data': data
	};
	if (document.cookie === '') {
		return ;
	}
	const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
	const options = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(all_data)
	};
	const response = await fetch('/auth/update/', options);
	if (!response.ok) {
		return;
	}
	const content = await response.json();
	sessionStorage.setItem('user_data', JSON.stringify(content));
	navbar.updateData({ 'user_data': content });
	modal.updateData({ 'user_data': content });
	navbar.loadContent();
	modal.loadContent();
	currentPage.updateData({ 'user_data': content });
	currentPage.loadContent();
}
