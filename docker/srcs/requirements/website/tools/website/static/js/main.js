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

	let currentPage = 'index';
	let serverData = await getServerData();
	let components = serverData.components;
	let currentApp = serverData.selected;

	changePage = async (event, app, page) => {
		event.preventDefault();
		if (components[app].includes(page) === false) {
			currentApp = '/';
			currentPage = 'index';
			document.title = 'AWESOME WEBSITE';
			return history.replaceState({ app: '/', page: 'index' }, null, '/');
		}
		if (currentApp === app && currentPage === page) return;
		if (await updatePageContent(app, page) === false) {
			currentApp = '/';
			currentPage = 'index';
			document.title = 'AWESOME WEBSITE';
			return history.replaceState({ app: '/', page: 'index' }, null, '/');
		}
		currentApp = app;
		currentPage = page;
		if (currentPage === 'index') return history.pushState({ app: currentApp, page: currentPage }, null, currentApp);
		return history.pushState({ app: currentApp, page: currentPage }, null, `${currentApp}${currentPage}/`);
	};

	window.onpopstate = async (event) => {
		event.preventDefault();
		if (event.state === null) {
			if (components[currentApp].includes('index') === false) {
				currentApp = '/';
				currentPage = 'index';
				document.title = 'AWESOME WEBSITE';
				return history.replaceState({ app: '/', page: 'index' }, null, '/');
			}
			if (currentPage === 'index') return;
			if (await updatePageContent(currentApp, 'index') === false) {
				currentApp = '/';
				currentPage = 'index';
				document.title = 'AWESOME WEBSITE';
				return history.replaceState({ app: '/', page: 'index' }, null, '/');
			}
			currentPage = 'index';
			return history.replaceState({ app: currentApp, page: 'index' }, null, currentApp);
		}
		if (event.state.page === '/' || event.state.page === 'index') {
			if (components[event.state.app].includes('index') === false) {
				currentApp = '/';
				currentPage = 'index';
				document.title = 'AWESOME WEBSITE';
				return history.replaceState({ app: '/', page: 'index' }, null, '/');
			}
			if (currentApp === event.state.app && currentPage === 'index') return;
			if (await updatePageContent(event.state.app, 'index') === false) {
				currentApp = '/';
				currentPage = 'index';
				document.title = 'AWESOME WEBSITE';
				return history.replaceState({ app: '/', page: 'index' }, null, '/');
			}
			currentApp = event.state.app;
			currentPage = 'index';
			return history.replaceState({ app: currentApp, page: 'index' }, null, currentApp);
		}
		if (components[event.state.app].includes(event.state.page) === false) {
			currentApp = '/';
			currentPage = 'index';
			document.title = 'AWESOME WEBSITE';
			return history.replaceState({ app: '/', page: 'index' }, null, '/');
		}
		if (currentApp === event.state.app && currentPage === event.state.page) return;
		if (await updatePageContent(event.state.app, event.state.page) === false) {
			currentApp = '/';
			currentPage = 'index';
			document.title = 'AWESOME WEBSITE';
			return history.replaceState({ app: '/', page: 'index' }, null, '/');
		}
		currentApp = event.state.app;
		currentPage = event.state.page;
		return history.replaceState({ app: currentApp, page: currentPage }, null, `${currentApp}${currentPage}/`);
	};

	await updatePageContent(currentApp, currentPage);
	history.replaceState({ app: currentApp, page: currentPage }, null, currentApp);
});
