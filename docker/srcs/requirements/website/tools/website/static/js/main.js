let navbar = null;
let app = null;
let modal = null;
let footer = null;
let sessionData = {};
let csrftoken = null;
let sessiontoken = null;
let currentPage = null;

document.addEventListener('DOMContentLoaded', (event) => {
	event.preventDefault();
	navbar = document.getElementById('navbar');
	app = document.getElementById('app');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');

	window.signUp = signUp;
	window.signOut = signOut;
	window.signIn = signIn;

	currentPage = 'index';

	async function startAndUpdate() {
		await sessionStart();
		updatePageContent();
	}

	function changePage(page = 'index') {
		if (page === currentPage) return;
		currentPage = page;
		updatePageContent(page);
		if (page === 'index') {
			history.pushState({ page: currentPage }, '', '/');
		} else {
			history.pushState({ page: currentPage }, '', '/' + currentPage + '/');
		}
	}

	window.changePage = (event, page) => {
		event.preventDefault();
		changePage(page);
	};

	window.onpopstate = (event) => {
		if (event.state === null) {
			history.replaceState({ page: 'index' }, '', '/');
			updatePageContent();
		} else {
			if (event.state.page === '/' || event.state.page === 'index') {
				history.replaceState({ page: 'index' }, '', '/');
				updatePageContent();
			} else {
				history.replaceState({ page: event.state.page }, '', '/' + event.state.page + '/');
				updatePageContent(event.state.page);
			}
		}
	};

	startAndUpdate();
});
