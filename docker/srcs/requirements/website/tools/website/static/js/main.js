let navbar = null;
let modal = null;
let indexPage = null;
let profilePage = null;
let sessionData = null;
let pages = null;

document.addEventListener('DOMContentLoaded', function () {
	// sessionStorage.clear();

	if (sessionStorage.getItem('user_data'))
		sessionData = { 'user_data': JSON.parse(sessionStorage.getItem('user_data')) };

	navbar = new ContentLoader('navbar', '/navbar/', sessionData);
	modal = new ContentLoader('modal', '/modal/', sessionData);
	indexPage = new ContentLoader('app', '/index/', sessionData);
	profilePage = new ContentLoader('app', '/profilepage/', sessionData);

	pages = {
		'/index/': indexPage,
		'/profilepage/': profilePage
	}

	navbar.loadContent();
	indexPage.loadContent();
	modal.loadContent();

	function changePage(page) {
		if (!page)
			return;
		page.updateData(sessionData);
		if (page.loadContent()) {
			currentPage = page;
			history.pushState({ url: page.url }, '', page.url);
		}
	}

	window.changePage = function (event, page) {
		event.preventDefault();
		changePage(pages[page]);
	}

	window.addEventListener('popstate', (event) => {
		if (event.state) {
			history.replaceState({ url: event.state.url }, '', event.state.url);
			const page = pages[event.state.url];
			if (!page)
				return;
			page.updateData(sessionData);
			page.loadContent();
		}
		else {
			history.replaceState({ url: '/index/' }, '', '/index/');
			const page = indexPage;
			if (!page)
				return;
			page.updateData(sessionData);
			page.loadContent();
		}
	});

	window.signOut = async function (event) {
		event.preventDefault();
		const target = sessionData['user_data']['username'];
		console.log(target);
	}


	//#region User management
	window.signUp = signUp;
	window.updateData = updateData;
	//#endregion

});
