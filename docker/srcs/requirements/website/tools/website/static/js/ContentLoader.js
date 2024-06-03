class ContentLoader {
	constructor(component_id, url, data = null) {
		this.component_id = component_id;
		this.url = url;
		this.data = data;
	}

	async loadContent() {
		this.component = document.getElementById(this.component_id);
		if (!this.component) {
			// console.error('Component not found');
			return false;
		}
		const options = this.data ? {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(this.data)
		} : {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
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
}
