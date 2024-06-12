async function signUp(event) {
	event.preventDefault();
	if (csrftoken === null) return;
	const form_data = new FormData(event.target);
	const response = await fetch('/backend/signup/', {
		method: 'POST',
		headers: { 'X-CSRFToken': csrftoken },
		body: form_data
	});
	if (!response.ok) return ;
	$('#signupFormModal').modal('hide');
	changePage(event);
	document.title = "Home";
}
