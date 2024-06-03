let navbar = null;
let modal = null;
let indexPage = null;
let profilePage = null;

document.addEventListener('DOMContentLoaded', function () {
	localStorage.clear();
	navbar = new ContentLoader('navbar', '/navbar/');
	modal = new ContentLoader('modal', '/modal/');
	indexPage = new ContentLoader('app', '/index/');
	profilePage = new ContentLoader('app', '/profilepage/');

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
			if (localStorage.getItem('ft_token') === null)
				history.replaceState({ url: '/index/' }, '', '/index/');
			else
				history.replaceState({ url: '/profilepage/' }, '', '/profilepage/');
			const page = localStorage.getItem('ft_token') === null ? indexPage : profilePage;
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
		if (!response.ok)
			return;
		const result = await response.json();
		if (result['error']) {
			// console.log(result['error']);
			return;
		}
		localStorage.setItem('ft_token', result['token']);
		$('.modal').modal('hide');
		navbar.updateData({ 'ft_token': 'true' });
		modal.updateData({ 'ft_token': 'true' });
		navbar.loadContent();
		modal.loadContent();
		changePage(profilePage);
	}
});
