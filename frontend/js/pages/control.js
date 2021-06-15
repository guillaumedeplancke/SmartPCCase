'use strict';

//#region ***  Variables ***
let selectFilterId;
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showOutputs = function (data) {
	let newInnerHTML = '';

	for (const output of data.outputs) {
		if(output._name.toLowerCase().includes('fan')) {
			newInnerHTML += `
			<div class="o-layout__item u-1-of-2-xxs u-mt-md">
				<div class="c-card c-card--clickable js-component" data-id=${output._id}>
					<div class="c-card__header--with-slider">
						<span class="c-card__icon material-icons">${output._icon}</span>
						<input class="c-slider js-slider" type="range" min="0" max="100" value="0" data-id=${output._id}>
					</div>
					<h3 class="c-card__title u-mt-lg u-mb-xs">${output._name}</h3>
					<p class="c-card__value u-mb-clear js-power">${output._description}</p>
				</div>
			</div>`;
		} else {
			newInnerHTML += `
			<div class="o-layout__item u-1-of-2-xxs u-mt-md">
				<div class="c-card c-card--clickable js-component" data-id=${output._id}>
					<div class="c-card__header">
						<span class="c-card__icon material-icons">${output._icon}</span>
						<label class="c-toggle js-toggle" data-id=${output._id} data-is-pwm=${output._is_pwm}>
							<input class="c-toggle__input" type="checkbox">
							<span class="c-toggle__slider"></span>
						</label>
					</div>
					<h3 class="c-card__title u-mt-lg u-mb-xs">${output._name}</h3>
					<p class="c-card__value u-mb-clear js-power">${output._description}</p>
				</div>
			</div>`;
		}
	}

	document.querySelector('.js-components').innerHTML = newInnerHTML;

	listenToChangeSlider();
	listenToChangeToggle();
	listenToClickCard();
};

const showFilters = function (data) {
	let newInnerHTML = `<p class="c-label c-label--active js-filter" data-id=all>Alle</p>`;

	for (const category of data.categories) {
		if (category._output) {
			newInnerHTML += `<p class="c-label js-filter" data-id=${category._id}>${category._name}</p>`;
		}
	}

	document.querySelector('.js-filters').innerHTML = newInnerHTML;
	
	if (selectFilterId) {
		showSelectedFilter(selectFilterId);
	}

	listenToClickFilter();
};

const showSelectedFilter = function (category_id) {
	for (const filter of document.querySelectorAll('.js-filter')) {
		if (filter.classList.contains('c-label--active')) {
			filter.classList.remove('c-label--active');
		}
	}

	document.querySelector(`.js-filter[data-id='${category_id}']`).classList.add('c-label--active');
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
//#endregion

//#region ***  Data Access - get___ ***
const getAllOutputs = function () {
	const url = backend + '/outputs';
	handleData(url, showOutputs, showError);
};

const getCategories = function () {
	const url = backend + '/categories';
	handleData(url, showFilters, showError);
};

const getOutputsForCategory = function (categoryId) {
	const url = backend + `/category/${categoryId}/devices`;
	handleData(url, showOutputs, showError);
}
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToClickFilter = function () {
	for (const filter of document.querySelectorAll('.js-filter')) {
		filter.addEventListener('click', function () {
			const id = this.getAttribute('data-id');

			for (const filter of document.querySelectorAll('.js-filter')) {
				if (filter.classList.contains('c-label--active')) {
					filter.classList.remove('c-label--active');
				}
			}

			this.classList.add('c-label--active');

			if (id === 'all') {
				getAllOutputs();
			} else {
				getOutputsForCategory(id);
			}
		});
	}
};

const listenToChangeSlider = function () {
	for (const slider of document.querySelectorAll('.js-slider')) {
		slider.addEventListener('change', function () {
			const output_id = this.getAttribute('data-id');

			socketio.emit('F2B_change_output', { output_id: output_id, change_to: this.value });
		});
	}
};

const listenToChangeToggle = function () {
	for (const toggle of document.querySelectorAll('.js-toggle')) {
		toggle.addEventListener('change', function () {
			let change_to_value;
			const checkbox = this.querySelector('input[type=checkbox]');

			if (checkbox.checked) {
				change_to_value = 1;
				
				if (this.getAttribute('data-is-pwm') == 'true') {
					change_to_value = 100;
				}
			} else {
				change_to_value = 0;
			}

			socketio.emit('F2B_change_output', { output_id: this.getAttribute('data-id'), change_to: change_to_value });
		});
	}
};

const listenToClickCard = function () {
	for (const card of document.querySelectorAll('.c-card--clickable')) {
		card.addEventListener('click', function(e) {
			const id = card.getAttribute('data-id');

			let element = document.elementFromPoint(e.clientX, e.clientY);

			if (!element.classList.contains('c-toggle__slider') && !element.classList.contains('c-slider')) {
				window.location.href = `component.html?id=${id}`;
			}	
		});
	}
}
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const initPage = function () {
	console.log('control.js page init');

	const urlParams = new URLSearchParams(window.location.search);

	if (urlParams.get('id')) {
		const id = urlParams.get('id');

		selectFilterId = id;

		getCategories();
		getOutputsForCategory(id);
	} else {
		getCategories();
		getAllOutputs();
	}
};
//#endregion

document.addEventListener('DOMContentLoaded', initPage);
