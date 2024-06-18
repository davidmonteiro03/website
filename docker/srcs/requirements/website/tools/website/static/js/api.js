async function loadApiData(event, page) {
	event.preventDefault();
	const response = await fetch(`/api/${page}/`);
	if (!response.ok) return;
	const content = await response.json();
	apiData = content[page];
	changePage(event, page);
}
