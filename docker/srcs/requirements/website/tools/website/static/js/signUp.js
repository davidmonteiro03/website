/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   signUp.js                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/06/05 12:40:59 by dcaetano          #+#    #+#             */
/*   Updated: 2024/06/05 12:41:01 by dcaetano         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

async function signUp(event) {
	event.preventDefault();
	const formData = new FormData(event.target);
	const data = {};
	for (const [key, value] of formData.entries()) {
		data[key] = value;
	}
	if (document.cookie === '') {
		return ;
	}
	const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
	const options = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken
		},
		body: JSON.stringify(data)
	};
	const response = await fetch('/auth/signup/', options);
	if (!response.ok) {
		return;
	}
	$('.modal').modal('hide');
	const content = await response.json();
	sessionStorage.setItem('user_data', JSON.stringify(content));
	sessionData = { 'user_data': JSON.parse(sessionStorage.getItem('user_data')) };
	navbar.updateData({ 'user_data': content });
	modal.updateData({ 'user_data': content });
	navbar.loadContent();
	modal.loadContent();
	indexPage.updateData({ 'user_data': content });
	changePage(event, '/index/');
}
