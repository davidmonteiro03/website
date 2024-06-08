async function loadElement(element, type, url = 'index') {
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
			'file': url + '.html'
		})
	});
	if (!response.ok) return;
	const content = await response.json();
	element.innerHTML = content.html;
}
function updatePageContent(page = 'index') {
	loadElement(navbar, 'navbar', 'navbar');
	loadElement(app, 'app', page);
	loadElement(modal, 'modal', 'modal');
	loadElement(footer, 'footer', 'footer');
}
