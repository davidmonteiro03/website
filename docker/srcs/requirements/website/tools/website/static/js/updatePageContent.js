loadElement = async (app, element, type, file, data = null) => {
	let csrftoken = getCookie('csrftoken');
	if (app === null || element === null || type === null || file === null || file === '' || csrftoken === null) return false;
	let senddata = {};
	senddata['type'] = type;
	senddata['file'] = file;
	if (data !== null) senddata['data'] = data;
	const response = await fetch(`${app}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify(senddata)
	});
	if (!response.ok) return false;
	const json_data = await response.json();
	element.innerHTML = json_data.html;
	return true;
};

updatePageContent = async (app, page, data = null) => {
	if (app === null || page === null || navbar === null || content === null || modal === null || footer === null) return false;
	if (await loadElement(app, navbar, 'navbar', 'navbar', data) === false) return false;
	if (await loadElement(app, content, 'content', page, data) === false) return false;
	if (await loadElement(app, modal, 'modal', 'modal', data) === false) return false;
	if (await loadElement(app, footer, 'footer', 'footer', data) === false) return false;
	return true;
};
