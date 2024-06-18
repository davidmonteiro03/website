async function loadApiData(event, page = 'ligaportugal') {
	event.preventDefault();
	if (csrftoken === null) return;
	const response = await fetch(`/api/${page}/`, {
		method: 'GET',
		headers: { 'X-CSRFToken': csrftoken },
	});
	if (!response.ok) return;
	const content = await response.json();
	apiData = content[page];
	changePage(event, page);
}
