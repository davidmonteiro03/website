document.addEventListener('DOMContentLoaded', function () {
	const app = document.getElementById('app');
	const index = document.getElementById('index');
	if (!app || !index) {
		console.error('No app or element found.');
		return;
	}
	const loadTemplate = async (url) => {
		try {
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error('Failed to load template.');
			}
			const template = await response.json();
			app.innerHTML = template.html;
		}
		catch (error) {
			console.error("Error:", error);
		}
	};
	index.addEventListener('click', (event) => {
		event.preventDefault();
		loadTemplate('/index/');
	});
	loadTemplate('/index/');

});
