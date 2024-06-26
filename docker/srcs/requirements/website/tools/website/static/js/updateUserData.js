updateUserData = async (event) => {
	event.preventDefault();
	if (document.cookie === '') return;
	let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (tmp === null || tmp === '') return;
	let csrftoken = tmp.split('=')[1];
	if (csrftoken === null || csrftoken === '') return;
	const form_data = new FormData(event.target);
	const response = await fetch('/user/update/', {
		method: 'POST',
		headers: { 'X-CSRFToken': csrftoken },
		body: form_data
	});
	if (!response.ok) return;
	updatePageContent('/user/', 'profilepage');
};
