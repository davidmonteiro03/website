let navbar = null;
let app = null;
let modal = null;
let footer = null;

document.addEventListener('DOMContentLoaded', async (event) => {
	event.preventDefault();
	navbar = document.getElementById('navbar');
	app = document.getElementById('app');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');

	let currentPage = 'index';

	async function changePage(page = 'index', api_data = null) {
		if (await updatePageContent(page, api_data) === false) return;
		if (currentPage === page) return;
		currentPage = page;
		if (currentPage === 'index') {
			history.pushState({ page: currentPage, api_data: api_data }, null, '/');
		} else {
			history.pushState({ page: currentPage, api_data: api_data }, null, `/${currentPage}/`);
		}
	}

	window.changePage = async (event, page = 'index', api_data = null) => {
		event.preventDefault();
		await changePage(page, api_data);
	};

	window.onpopstate = async (event) => {
		if (event.state === null) {
			currentPage = 'index';
			if (await updatePageContent() === false) return;
			history.replaceState({ page: currentPage, api_data: null }, null, '/');
		} else {
			if (event.state.page === '/' || event.state.page === 'index') {
				currentPage = 'index';
				if (await updatePageContent() === false) return;
				history.replaceState({ page: currentPage, api_data: null }, null, '/');
			} else {
				if (event.state.page === currentPage) return;
				currentPage = event.state.page;
				if (await updatePageContent(currentPage, event.state.api_data) === false) return;
				history.replaceState({ page: currentPage, api_data: event.state.api_data }, null, `/${currentPage}/`);
			}
		}
	};

	await updatePageContent();
});
