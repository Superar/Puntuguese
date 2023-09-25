const submit_button = document.querySelector('#submit_button');
const reset_button = document.querySelector('#reset_button');
const add_sign_button = document.querySelector('#add_sign_button');
const remove_sign_button = document.querySelector('#remove_sign_button');
const copy_button = document.querySelector('#copy_button');
const sign_repeating_field = document.querySelector('#sign_repeater');
const file_input = document.querySelector('#input_corpus');
const download_button = document.querySelector('#download_button');
const pun_repeater = document.querySelector('#pun_repeater');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const pun_pagination = document.querySelector('#pun_pagination');

let data = [];
let number_signs = 0;
let current_page = 0;
const puns_per_page = 10;

/*
 * FORM
 */

function reset_form() {
	for (const input of document.querySelectorAll('input')) {
		if (input.id != 'source_id') {
			if (input.type == 'text') {
				input.value = '';
			} else if (input.type == 'checkbox') {
				input.checked = false;
			}
		}
	}

	for (const textarea of document.querySelectorAll('textarea')) {
		textarea.value = '';
	}

	while (sign_repeating_field.childElementCount > 1) {
		sign_repeating_field.lastChild.remove();
		number_signs = 0;
	}
}

add_sign_button.addEventListener('click', () => {
	new_field = document.createElement('div');
	new_field.className = sign_repeating_field.children[0].className;
	new_field.innerHTML = sign_repeating_field.children[0].innerHTML.replace(/\[0]/g, '[' + ++number_signs + ']');
	sign_repeating_field.append(new_field);
});

remove_sign_button.addEventListener('click', () => {
	if (sign_repeating_field.childElementCount > 1) {
		sign_repeating_field.lastChild.remove();
		number_signs--;
	}
});

submit_button.addEventListener('click', () => {
	source_id = document.querySelector('#source_id').value;
	pun_id = 1;
	for (const pun of data) {
		if (pun.id.startsWith(source_id) && pun.id.split('.')[1] >= pun_id) {
			console.log(source_id, pun_id, pun.id);
			pun_id++;
		}
	}

	id = source_id + '.' + pun_id;

	text = document.querySelector('#pun_text').value;

	signs = [];
	sign_fields = document.querySelector('#sign_repeater').children;
	for (const field of sign_fields) {
		signs.push({homograph: field.querySelector('.homograph').checked,
			homophone: field.querySelector('.homophone').checked,
			'pun sign': field.querySelector('.pun_sign').value,
			'alternative sign': field.querySelector('textarea').value.split('\n')});
	}

	data.push({id, text, signs});
	reset_form();
	render_puns();
	render_json();
});

reset_button.addEventListener('click', reset_form);

/*
 * DATA VISUALIZATION
 */
function reset_puns() {
	while (pun_repeater.children.length > 2) {
		pun_repeater.lastChild.remove();
	}

	while (pun_pagination.children.length > 0) {
		pun_pagination.lastChild.remove();
	}
}

previous.addEventListener('click', () => {
	if (current_page > 0) {
		current_page--;
	}

	render_puns();
});

next.addEventListener('click', () => {
	const max_pages = Math.ceil(data.length / puns_per_page);
	if (current_page < max_pages - 1) {
		current_page++;
	}

	render_puns();
});

function render_puns() {
	const max_pages = Math.ceil(data.length / puns_per_page);
	const min_index = Math.min(current_page * puns_per_page, data.length);
	const max_index = Math.min(min_index + puns_per_page, data.length);

	reset_puns();
	for (let i = min_index; i < max_index; i++) {
		const pun = data[i];
		render_pun(pun);
	}

	// Add pagination
	if (max_pages <= 5) {
		for (let i = 0; i < max_pages; i++) {
			const item = document.createElement('li');
			const page_link = document.createElement('a');
			page_link.classList.add('pagination-link');
			page_link.textContent = i + 1;
			if (i == current_page) {
				page_link.classList.add('is-current');
			}
            page_link.addEventListener('click', () => {
                current_page = i;
                render_puns();
            });

			item.append(page_link);
			pun_pagination.append(item);
		}
	} else if (max_pages > 5) {
	    const first_page = document.createElement('li');
		const first_page_link = document.createElement('a');
		first_page_link.classList.add('pagination-link');
		first_page_link.textContent = 1;
		first_page_link.addEventListener('click', () => {
			current_page = 0;
			render_puns();
		});

		const first_ellipsis = document.createElement('span');
		first_ellipsis.classList.add('pagination-ellipsis');
		first_ellipsis.textContent = '...';

	    const current_item = document.createElement('li');
		const current_page_link = document.createElement('a');
		current_page_link.classList.add('pagination-link', 'is-current');
		current_page_link.textContent = current_page + 1;

		const second_ellipsis = document.createElement('span');
		second_ellipsis.classList.add('pagination-ellipsis');
		second_ellipsis.textContent = '...';

	    const last_page = document.createElement('li');
		const last_page_link = document.createElement('a');
		last_page_link.classList.add('pagination-link');
		last_page_link.textContent = max_pages;
		last_page_link.addEventListener('click', () => {
			current_page = max_pages - 1;
			render_puns();
		});

		first_page.append(first_page_link);
		current_item.append(current_page_link);
		last_page.append(last_page_link);
		pun_pagination.append(first_page);
		pun_pagination.append(first_ellipsis);
		pun_pagination.append(current_item);
		pun_pagination.append(second_ellipsis);
		pun_pagination.append(last_page);
	}
}

function delete_pun(event) {
	const id = event.target.id;

	let index = 0;
	while (data[index].id != id) {
		index++;
	}

	data.splice(index, 1);

	render_puns();
	render_json();
}

function render_pun(pun) {
	const block = document.createElement('div');
	block.classList.add('block');
	block.id = 'block_id_' + pun.id;
	const card = document.createElement('div');
	card.classList.add('card');
	const header = document.createElement('header');
	header.classList.add('card-header');
	const title = document.createElement('p');
	title.classList.add('card-header-title');
	title.textContent = pun.id;
	const card_content = document.createElement('div');
	card_content.classList.add('card-content');
	const content = document.createElement('div');
	content.classList.add('content');
	content.textContent = pun.text;
	const footer = document.createElement('footer');
	footer.classList.add('card-footer');
	const del_button = document.createElement('a');
	del_button.classList.add('card-footer-item');
	del_button.textContent = 'Apagar';
	del_button.id = pun.id;
	del_button.addEventListener('click', delete_pun);

	header.append(title);
	card.append(header);
	card_content.append(content);
	card.append(card_content);
	footer.append(del_button);
	card.append(footer);
	block.append(card);
	pun_repeater.append(block);
}

/*
 * JSON
 */

function load_json(event) {
	const file = event.target.files[0];
	if (file) {
		const reader = new FileReader();

		reader.addEventListener('load', e => {
			const contents = e.target.result;
			data = JSON.parse(contents);

			// For (const pun of data) {
			// 	render_pun(pun);
			// }
			render_puns();

			render_json();
		});
		reader.readAsText(file);
	}
}

file_input.addEventListener('change', load_json);

function render_json() {
	document.querySelector('pre').innerHTML = JSON.stringify(data, null, 4);
}

function export_json(event) {
	const data_uri = 'text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(data, null, 4));
	event.target.setAttribute('href', 'data:' + data_uri);
	event.target.setAttribute('download', 'data.json');
}

download_button.addEventListener('click', export_json);

copy_button.addEventListener('click', () => {
	navigator.clipboard.writeText(JSON.stringify(data, null, 4));
});
