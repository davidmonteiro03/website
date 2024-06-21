let navbar = null;
let content = null;
let modal = null;
let footer = null;

getCookie = (name) => {
	let cookie = document.cookie.split('; ').find(row => row.startsWith(name));
	if (cookie === undefined || cookie === null || cookie === '') return '';
	return cookie.split('=')[1];
};

document.addEventListener('DOMContentLoaded', async (event) => {
	event.preventDefault();
	navbar = document.getElementById('navbar');
	content = document.getElementById('content');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');

	let currentApp = '/';
	let currentPage = 'index';

	currentApp = getCookie('token') === '' ? '/' : '/user/';

	changePage = async (event, app, page, replace) => {
		event.preventDefault();
		if (await updatePageContent(app, page) === false) return history.replaceState({ app: '/', page: 'index' }, null, '/');
		if (currentApp === app && currentPage === page) return;
		currentApp = app;
		currentPage = page;
		if (currentPage === 'index') {
			if (replace === true) return history.replaceState({ app: currentApp, page: currentPage }, null, currentApp);
			return history.pushState({ app: currentApp, page: currentPage }, null, currentApp);
		}
		if (replace === true) return history.replaceState({ app: currentApp, page: currentPage }, null, `${currentApp}${currentPage}/`);
		return history.pushState({ app: currentApp, page: currentPage }, null, `${currentApp}${currentPage}/`);
	};

	window.onpopstate = async (event) => {
		event.preventDefault();
		if (event.state === null) return changePage(event, currentApp, 'index', true);
		if (event.state.page === '/' || event.state.page === 'index') return changePage(event, event.state.app, 'index', true);
		return changePage(event, event.state.app, event.state.page, true);
	};

	await updatePageContent(currentApp, currentPage);
	history.replaceState({ app: currentApp, page: currentPage }, null, currentApp);
});
