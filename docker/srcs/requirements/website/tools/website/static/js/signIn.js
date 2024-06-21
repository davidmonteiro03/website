signIn = async (event) => {
	event.preventDefault();
	if (document.cookie === '') return;
	let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (tmp === null || tmp === '') return;
	let csrftoken = tmp.split('=')[1];
	if (csrftoken === null || csrftoken === '') return;
	const form_data = new FormData(event.target);
	const json_data = {};
	form_data.forEach((value, key) => { json_data[key] = value; });
	const response = await fetch('/user/signin/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify(json_data)
	});
	if (!response.ok) return;
	$('#signinFormModal').modal('hide');
	changePage(event, '/user/', 'index', true);
};
