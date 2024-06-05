class ContentLoader {
	constructor(component_id, url, data = null) {
		this.component_id = component_id;
		this.url = url;
		this.data = data;
	}

	rewriteData(data) {
		this.data = data;
	}

	updateData(data) {
		if (!data) {
			return;
		}
		let currentData = this.data;
		if (currentData) {
			for (const key in data) {
				currentData[key] = data[key];
			}
		}
		else {
			currentData = data;
		}
		this.data = currentData;
	}

	async loadContent() {
		this.component = document.getElementById(this.component_id);
		if (!this.component) {
			// console.error('Component not found');
			return false;
		}
		if (document.cookie === '') {
			return false;
		}
		const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
		const options = this.data ? {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify(this.data)
		} : {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			}
		};
		const response = await fetch(this.url, options);
		if (!response.ok) {
			return false;
		}
		const content = await response.json();
		// console.log(content.html);
		this.component.innerHTML = content.html;
	}
}
