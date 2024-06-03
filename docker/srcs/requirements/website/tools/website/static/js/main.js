let navbar = null;
let modal = null;
let indexPage = null;
let profilePage = null;
let sessionData = null;

document.addEventListener('DOMContentLoaded', function () {
	// localStorage.clear();

	if (localStorage.getItem('user_data'))
		sessionData = { 'user_data': JSON.parse(localStorage.getItem('user_data')) };

	navbar = new ContentLoader('navbar', '/navbar/', sessionData);
	modal = new ContentLoader('modal', '/modal/', sessionData);
	indexPage = new ContentLoader('app', '/index/', sessionData);
	profilePage = new ContentLoader('app', '/profilepage/', sessionData);

	const pages = {
		'/index/': indexPage,
		'/profilepage/': profilePage
	}

	navbar.loadContent();
	indexPage.loadContent();
	modal.loadContent();

	function changePage(page) {
		if (!page)
			return;
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
			page.loadContent();
		}
		else {
			history.replaceState({ url: '/index/' }, '', '/index/');
			const page = indexPage;
			if (!page)
				return;
			page.loadContent();
		}
	});

	window.signUp = async function (event) {
		event.preventDefault();
		const formData = new FormData(event.target);
		const data = {};
		for (const [key, value] of formData.entries()) {
			data[key] = value;
		}
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		};
		const response = await fetch('/auth/signup/', options);
		if (!response.ok) {
			return;
		}
		$('.modal').modal('hide');
		const content = await response.json();
		localStorage.setItem('user_data', JSON.stringify(content));
		navbar.updateData({ 'user_data': content });
		modal.updateData({ 'user_data': content });
		navbar.loadContent();
		modal.loadContent();
		indexPage.updateData({ 'user_data': content });
		changePage(indexPage);
	}

	window.signOut = async function (event) {
		event.preventDefault();
		const target = sessionData['user_data']['username'];
		console.log(target);
	}

	window.updateData = async function (event) {
		event.preventDefault();
		const formData = new FormData(event.target);
		const data = {};
		for (const [key, value] of formData.entries()) {
			data[key] = value;
		}
		data['username'] = sessionData['user_data']['username'];
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		};
		const response = await fetch('/auth/update/', options);
		if (!response.ok) {
			return;
		}
		const content = await response.json();
		localStorage.setItem('user_data', JSON.stringify(content));
		navbar.updateData({ 'user_data': content });
		modal.updateData({ 'user_data': content });
		navbar.loadContent();
		modal.loadContent();
		currentPage.updateData({ 'user_data': content });
		currentPage.loadContent();
	}

});
