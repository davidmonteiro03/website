loadElement = async (app, element, type, file) => {
	let csrftoken = getCookie('csrftoken');
	if (app === null || element === null || type === null || file === null || file === '' || csrftoken === null) return false;
	const response = await fetch(`${app}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			'type': type,
			'file': file
		})
	});
	if (!response.ok) return false;
	const json_data = await response.json();
	element.innerHTML = json_data.html;
	return true;
};

updatePageContent = async (app, page) => {
	if (app === null || page === null || navbar === null || content === null || modal === null || footer === null) return false;
	if (await loadElement(app, navbar, 'navbar', 'navbar') === false) return false;
	if (await loadElement(app, content, 'content', page) === false) return false;
	if (await loadElement(app, modal, 'modal', 'modal') === false) return false;
	if (await loadElement(app, footer, 'footer', 'footer') === false) return false;
	return true;
};
