signOut = async (event) => {
	event.preventDefault();
	if (document.cookie === '') return;
	let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (tmp === null || tmp === '') return;
	let csrftoken = tmp.split('=')[1];
	if (csrftoken === null || csrftoken === '') return;
	const response = await fetch('/user/signout/', {
		method: 'POST',
		headers: { 'X-CSRFToken': csrftoken }
	});
	if (!response.ok) return;
	window.location.href = '/';
};
