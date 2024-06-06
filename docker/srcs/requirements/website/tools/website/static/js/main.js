let navbar = null;
let app = null;
let modal = null;
let footer = null;

document.addEventListener('DOMContentLoaded', function () {
	navbar = document.getElementById('navbar');
	app = document.getElementById('app');
	modal = document.getElementById('modal');
	footer = document.getElementById('footer');
	async function loadElement(element, type, file, data = null) {
		if (document.cookie === '' || element === null) {
			return;
		}
		const response = await fetch('/', {
			'method': 'POST',
			'headers': {
				'Content-Type': 'application/json',
				'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1],
			},
			'body': JSON.stringify({
				'type': type,
				'file': file,
				'data': data
			})
		});
		const content = await response.json();
		// console.log(content);
		element.innerHTML = content.html;
	}
	function updateNavbar(data = null) {
		loadElement(navbar, 'navbar', 'navbar.html', data);
	}
	function updateApp(page = 'index', data = null) {
		loadElement(app, 'app', page + '.html', data);
	}
	function updateModal(data = null) {
		loadElement(modal, 'modal',  'modal.html', data);
	}
	function updateFooter(data = null) {
		loadElement(footer, 'footer', 'footer.html', data);
	}
	updateNavbar();
	updateApp();
	updateModal();
	updateFooter({
		'json_fodido': {
			'ola': {
				'adeus': 'ola_adeus'
			},
			'adeus': {
				'ola': 'adeus_ola'
			}
		}
	});
});
