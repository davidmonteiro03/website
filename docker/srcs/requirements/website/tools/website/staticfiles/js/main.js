document.addEventListener('DOMContentLoaded', function () {
	// Change Page
	const app = document.getElementById('app');
	const index = document.getElementById('index');
	if (!app || !index) {
		return console.error('No app or element found.');
	}
	const loadTemplate = async (url, element) => {
		try {
			if (element === null) {
				throw new Error('Element not found.');
			}
			const response = await fetch(url);
			if (!response.ok) {
				throw new Error('Failed to load template.');
			}
			const template = await response.json();
			element.innerHTML = template.html;
		}
		catch (error) {
			console.error("Error:", error);
		}
	};
	index.addEventListener('click', (event) => {
		event.preventDefault();
		loadTemplate('/index/', app);
	});
	loadTemplate('/index/', app);

	// Signup
	const signupForm = document.getElementById('signupForm');
	signupForm.addEventListener('submit', async (event) => {
		event.preventDefault();
		try {
			const formData = new FormData(signupForm);
			const data = {};
			formData.forEach((value, key) => data[key] = value);
			const response = await fetch('/auth/signup/', {
				method: 'POST',
				body: JSON.stringify(data),
			});
			const json = await response.json();
			console.log(json);
		}
		catch (error) {
			console.error("Error:", error);
		}
	});

});
