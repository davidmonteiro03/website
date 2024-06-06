let navbar = null;
let app = null;
let modal = null;
let footer = null;
let sessionData = {};
let csrftoken = null;

document.addEventListener('DOMContentLoaded', function () {
	navbar = document.getElementById('navbar');
	app = document.getElementById('app');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');

	if (!(document.cookie === '')) {
		csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
	}

	window.updatePageContent = updatePageContent;
	window.signUp = signUp;

	updatePageContent();
});
