'use strict';

//#region ***  DOM references ***
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showCategoriesSeeded = function (data) {
	console.log(data.categories);

	let newInnerHTML = '';

	for (const category of data.categories) {
		if (category._slug === 'fan') {		
			newInnerHTML += 
			`<div class="o-layout__item u-mt-lg u-flex-first">
				<div class="c-card c-card--clickable u-text-center u-bg-theme-gradient js-category" data-category-id='${category._id}'>
					<h3 class="c-card__title u-mb-sm">${category._name}</h3>
					<div class="o-layout u-mb-sm">`;
		
			for (const fan of category._devices) {
				newInnerHTML += 
				`<div class="o-layout__item u-1-of-${category._devices.length}">
					<span class="c-card__icon material-icons">air</span>
					<p class="u-mb-clear"><span class="js-value" data-device-id="${fan._id}">---</span> %</p>
				</div>`;
			}
						
			newInnerHTML += `</div>
				</div>
			</div>`;
		} else {
			newInnerHTML += `
			<div class="o-layout__item u-1-of-2-xxs u-mt-md">
				<div class="c-card u-text-center js-category" data-category-id='${category._id}'>
					<h3 class="c-card__title u-mb-sm">${category._name}</h3>
					<span class="c-card__icon material-icons">${category._icon}</span>`;

			newInnerHTML += `<p class="u-mb-clear">`;

			if (category._output) {
				if (category._devices.length > 1) {
					newInnerHTML += `<span class="js-value">--</span>`;
				} else {
					newInnerHTML += `<span class="js-value" data-device-id='${category._devices[0]._id}'>--</span>`;
				}
			} else if (category._input) {
				for (const [i, device] of category._devices.entries()) {
					newInnerHTML += `
					<span class="js-value" data-device-id='${device._id}'>--</span> ${device._unit} `;

					if (i < category._devices.length - 1) {
						newInnerHTML += ' - ';
					}
				}				
			}
			
			newInnerHTML += `
					</p>
				</div>
			</div>`;
		}
	}

	document.querySelector('.js-components').innerHTML = newInnerHTML;

	listenToClickCard();
};
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
//#endregion

//#region ***  Data Access - get___ ***
const getSeededCategories = function() {
	const url = backend + '/categories/seeded';
	handleData(url, showCategoriesSeeded, showError);
};
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToClickCard = function() {
	for (const card of document.querySelectorAll('.c-card--clickable')) {
		card.addEventListener('click', function() {
			const id = card.getAttribute('data-category-id');

			window.location.href = `control.html?id=${id}`;
		});
	}
};
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const initPage = function () {
	console.log('index.js page init');

	getSeededCategories();
};
//#endregion

document.addEventListener('DOMContentLoaded', initPage);