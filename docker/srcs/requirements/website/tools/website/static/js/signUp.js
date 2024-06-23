signUpFormHelper = async (input) => {
	let id = input.id;
	let name = input.name;
	let value = input.value;
	let error = null;

	updateSignUpForm = () => {
		if (value === '') {
			input.classList.remove('is-valid');
			input.classList.remove('is-invalid');
			document.getElementById(id + '_feedback').innerHTML = '';
			return;
		}
		if (error === null) {
			input.classList.remove('is-invalid');
			input.classList.add('is-valid');
			document.getElementById(id + '_feedback').innerHTML = '';
			return;
		}
		input.classList.remove('is-valid');
		input.classList.add('is-invalid');
		document.getElementById(id + '_feedback').innerHTML = error;
	};

	searchClient = async () => {
		if (document.cookie === '') return;
		let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
		if (tmp === null || tmp === '') return;
		let csrftoken = tmp.split('=')[1];
		if (csrftoken === null || csrftoken === '') return;
		const data = {};
		data[name] = value;
		const response = await fetch('/user/getuser/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify(data)
		});
		if (response.ok) return;
		error = `${name.charAt(0).toUpperCase() + name.slice(1)} already exists.`;
	};

	namesHelper = () => {
		if (value.length < 3) return error = "Name must be at least 3 characters long.";
		if (value.length > 32) return error = "Name must be at most 32 characters long.";
		if (!value.match(/^[^\p{P}\p{S}\p{N}\p{C}\p{Z}]+$/gu)) return error = "Name must contain only letters.";
	};

	usernameHelper = async () => {
		if (value.length < 3) return error = "Username must be at least 3 characters long.";
		if (value.length > 32) return error = "Username must be at most 32 characters long.";
		if (!value.match(/^[a-z0-9_.-]+$/)) return error = "Username must contain only lowercase letters, numbers, and the characters '.', '_', and '-'.";
		if (!value[0].match(/[a-z]/)) return error = "Username must start with a lowercase letter.";
		await searchClient();
	};

	emailHelper = async () => {
		if (value.length < 5) return error = "Email must be at least 5 characters long.";
		if (value.length > 97) return error = "Email must be at most 97 characters long.";
		let main_values = ft_split(value, '@');
		let at_count = ft_strcntchr(value, '@');
		let main_count = main_values.length;
		if (at_count !== 1) return error = "Email must contain exactly one '@'.";
		if (main_count !== 2) return error = "Email must contain a username and a domain.";
		if (main_values[0].length < 3) return error = "Email must contain a username of at least 3 characters long.";
		if (main_values[0].length > 32) return error = "Email must contain a username of at most 32 characters long.";
		if (!main_values[0].match(/^[a-z0-9_.-]+$/)) return error = "Email must contain a username with only lowercase letters, numbers, and the characters '.', '_', and '-'.";
		if (!main_values[0][0].match(/[a-z]/)) return error = "Email must contain a username that starts with a lowercase letter.";
		let domain_values = ft_split(main_values[1], '.');
		let dot_count = ft_strcntchr(main_values[1], '.');
		let domain_count = domain_values.length;
		if (domain_count < 2) return error = "Email must contain at least one '.' in the domain.";
		if (dot_count !== domain_count - 1) return error = "Email must contain only one '.' between each domain.";
		if (main_values[1].length < 2) return error = "Email must contain a domain of at least 2 characters long.";
		if (main_values[1].length > 64) return error = "Email must contain a domain of at most 64 characters long.";
		for (let i = 0; i < domain_count; i++) if (!domain_values[i].match(/^[a-z0-9]+$/)) return error = "Email must contain a domain with only lowercase letters and numbers.";
		await searchClient();
	};

	passwordHelper = () => {
		if (value.length < 8) return error = "Password must be at least 8 characters long.";
		if (value.length > 32) return error = "Password must be at most 32 characters long.";
		if (ft_strschchr(value, " \t\n\r\v\f")) return error = "Password must not contain any whitespace characters.";
		if (!ft_strschchr(value, "0123456789")) return error = "Password must contain at least one digit.";
		if (!ft_strschchr(value, "abcdefghijklmnopqrstuvwxyz")) return error = "Password must contain at least one lowercase letter.";
		if (!ft_strschchr(value, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")) return error = "Password must contain at least one uppercase letter.";
		if (!ft_strschchr(value, "!@#$%^&*()_+-=[]{}|;:,.<>?/")) return error = "Password must contain at least one special character.";
	};

	profilephotoHelper = () => {
		let file = input.files[0];
		if (file.type.split('/')[0] !== 'image') {
			if (document.getElementById("show-foto").hasChildNodes())
				document.getElementById("show-foto").removeChild(document.getElementById("show-foto").firstChild);
			document.getElementById('show-foto').removeAttribute('style');
			document.getElementById('show-foto').removeAttribute('class');
			return error = "Profile photo must be an image.";
		}
		const filein = new FileReader();
		filein.onload = (value) => {
			if (document.getElementById("show-foto").hasChildNodes())
				document.getElementById("show-foto").removeChild(document.getElementById("show-foto").firstChild);
			const image = document.createElement('img');
			image.src = value.target.result;
			image.className = "img-fluid object-fit-cover rounded-circle";
			document.getElementById('show-foto').classList.add('ratio', 'ratio-1x1', 'mb-3');
			document.getElementById('show-foto').style.minWidth = '75px';
			document.getElementById('show-foto').style.minHeight = '75px';
			document.getElementById('show-foto').style.maxWidth = '250px';
			document.getElementById('show-foto').style.maxHeight = '250px';
			document.getElementById('show-foto').appendChild(image);
		}
		filein.readAsDataURL(file);
	};

	switch (name) {
		case 'fname':
		case 'lname':
			namesHelper();
			break;
		case 'username':
			await usernameHelper();
			break;
		case 'email':
			await emailHelper();
			break;
		case 'password':
			passwordHelper();
			break;
		case 'profilephoto':
			profilephotoHelper();
			break;
		default:
			break;
	}

	updateSignUpForm();
};

signUp = async (event) => {
	event.preventDefault();
	if (document.cookie === '') return;
	let tmp = document.cookie.split('; ').find(row => row.startsWith('csrftoken'));
	if (tmp === null || tmp === '') return;
	let csrftoken = tmp.split('=')[1];
	if (csrftoken === null || csrftoken === '') return;
	const form_data = new FormData(event.target);
	const response = await fetch('/user/signup/', {
		method: 'POST',
		headers: { 'X-CSRFToken': csrftoken },
		body: form_data
	});
	if (!response.ok) return;
	$('#signupFormModal').modal('hide');
	window.location.href = '/';
};
