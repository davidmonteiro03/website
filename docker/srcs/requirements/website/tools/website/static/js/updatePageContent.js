async function loadElement(element, type, url = 'index', api_data = null) {
	if (document.cookie === '' || element === null) return;
	let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (tmp === null || tmp === '') return;
	let csrftoken = tmp.split('=')[1];
	if (csrftoken === null || csrftoken === '') return;
	let data = {};
	data['type'] = type;
	data['file'] = url;
	if (api_data !== null) data['api_data'] = api_data;
	const response = await fetch('/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify(data)
	});
	if (!response.ok) return false;
	const content = await response.json();
	element.innerHTML = content.html;
	return true;
}
async function updatePageContent(page = 'index', api_data = null) {
	if (navbar === null || app === null || modal === null || footer === null) return false;
	if (await loadElement(navbar, 'navbar', 'navbar', api_data) === false) return false;
	if (await loadElement(app, 'app', page, api_data) === false) return false;
	if (await loadElement(modal, 'modal', 'modal', api_data) === false) return false;
	if (await loadElement(footer, 'footer', 'footer', api_data) === false) return false;
	return true;
}
