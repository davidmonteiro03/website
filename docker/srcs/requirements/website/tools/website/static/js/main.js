let navbar = null;
let app = null;
let modal = null;
let footer = null;
let sessionData = {};
let csrftoken = null;
let sessiontoken = null;

document.addEventListener('DOMContentLoaded', function () {
	navbar = document.getElementById('navbar');
	app = document.getElementById('app');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');

	if (!(document.cookie === '')) {
		let tmp_csrf = document.cookie.split('; ').find(row => row.startsWith('csrftoken')),
			tmp_session = document.cookie.split('; ').find(row => row.startsWith('sessiontoken'))
		if (tmp_csrf !== undefined) {
			csrftoken = tmp_csrf.split('=')[1];
		}
		if (tmp_session !== undefined) {
			sessiontoken = tmp_session.split('=')[1];
			sessionData['sessiontoken'] = sessiontoken;
		}
	}

	window.updatePageContent = updatePageContent;
	window.signUp = signUp;
	window.signOut = signOut;
	window.signIn = signIn;

	updatePageContent();
});
