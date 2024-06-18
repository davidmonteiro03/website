async function loadElement(element, type, url = 'index', data = null) {
	if (csrftoken === null || element === null) return;
	const response = await fetch('/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({
			'type': type,
			'file': url + '.html',
			'data': data
		})
	});
	if (!response.ok) return;
	const content = await response.json();
	element.innerHTML = content.html;
}
function updatePageContent(page = 'index', data = null) {
	loadElement(navbar, 'navbar', 'navbar', data);
	loadElement(app, 'app', page, data);
	loadElement(modal, 'modal', 'modal', data);
	loadElement(footer, 'footer', 'footer', data);
}
