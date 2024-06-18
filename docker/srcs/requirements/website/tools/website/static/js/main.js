let navbar = null;
let app = null;
let modal = null;
let footer = null;
let apiData = null;

document.addEventListener('DOMContentLoaded', (event) => {
	event.preventDefault();
	navbar = document.getElementById('navbar');
	app = document.getElementById('app');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');

	let currentPage = 'index';

	function changePage(page = 'index') {
		updatePageContent(page);
		if (currentPage === page) return;
		currentPage = page;
		if (currentPage === 'index') {
			history.pushState({ page: currentPage }, null, '/');
		} else {
			history.pushState({ page: currentPage }, null, '/' + currentPage + '/');
		}
	}

	window.changePage = (event, page = 'index') => {
		event.preventDefault();
		changePage(page);
	};

	window.onpopstate = (event) => {
		if (event.state === null) {
			currentPage = 'index';
			history.replaceState({ page: currentPage }, null, '/');
			updatePageContent();
		} else {
			if (event.state.page === '/' || event.state.page === 'index') {
				currentPage = 'index';
				history.replaceState({ page: currentPage }, null, '/');
				updatePageContent();
			} else {
				if (event.state.page === currentPage) return;
				currentPage = event.state.page;
				history.replaceState({ page: currentPage }, null, '/' + currentPage + '/');
				updatePageContent(currentPage);
			}
		}
	};

	updatePageContent();
});
