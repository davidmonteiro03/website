async function loadElement(element, type, url = 'index', data = null) {
	if (document.cookie === '' || element === null) return;
	let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (tmp === null || tmp === '') return;
	let csrftoken = tmp.split('=')[1];
	if (csrftoken === null || csrftoken === '') return;
	const response = await fetch('/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({
			'type': type,
			'file': url,
			'data': data
		})
	});
	if (!response.ok) return;
	const content = await response.json();
	element.innerHTML = content.html;
}
function updatePageContent(page = 'index') {
	loadElement(navbar, 'navbar', 'navbar', apiData);
	loadElement(app, 'app', page, apiData);
	loadElement(modal, 'modal', 'modal', apiData);
	loadElement(footer, 'footer', 'footer', apiData);
}
