async function loadElement(element, type, file, data = null) {
	if (document.cookie === '' || element === null) {
		return;
	}
	const response = await fetch('/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1]
		},
		body: JSON.stringify({
			'type': type,
			'file': file,
			'data': data
		})
	});
	if (!response.ok) {
		return;
	}
	const content = await response.json();
	element.innerHTML = content.html;
}
function updatePageContent(page = 'index') {
	loadElement(navbar, 'navbar', 'navbar.html', sessionData);
	loadElement(app, 'app', page + '.html', sessionData);
	loadElement(modal, 'modal', 'modal.html', sessionData);
	loadElement(footer, 'footer', 'footer.html', sessionData);
}
