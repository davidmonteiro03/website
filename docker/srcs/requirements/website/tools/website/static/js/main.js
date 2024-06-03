let navbar = null;
let modal = null;
let indexPage = null;
let profilePage = null;

function closeModals() {
	const modals = document.getElementsByClassName('modal');
	for (let i = 0; i < modals.length; i++) {
		modals[i].classList.remove('show');
		modals[i].setAttribute('aria-hidden', 'true');
		modals[i].setAttribute('style', 'display: none');
	}
	const modalsBackdrops = document.getElementsByClassName('modal-backdrop');
	for (let i = 0; i < modalsBackdrops.length; i++) {
		document.body.removeChild(modalsBackdrops[i]);
	}
}

document.addEventListener('DOMContentLoaded', function () {
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
			if (currentPage.url === '/')
				history.pushState({ url: '/' }, '', '/');
			else
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
			history.replaceState({ url: '/' }, '', '/');
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
		if (!response.ok)
			return;
		const result = await response.json();
		if (result['error']) {
			// console.log(result['error']);
			return;
		}
		navbar.updateData({ 'ft_token': 'true' });
		navbar.loadContent();
		profilePage.loadContent();
		closeModals();
	}
});
