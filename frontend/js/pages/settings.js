'use strict';

//#region ***  Variables ***
let selectFilterId;
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showConfigValues = function (data) {
	Object.keys(data.config).forEach(function(key) {
		console.log('Key : ' + key + ', Value : ' + data.config[key])

		const slider = document.querySelector(`.js-setting[data-name='${key}']`);

		if (slider) {
			slider.querySelector('input').checked = data.config[key];
		}
	});

	listenToClickSaveSettings();
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
//#endregion

//#region ***  Data Access - get___ ***
const getConfigValues = function () {
	const url = backend + '/config';
	handleData(url, showConfigValues, showError);
};
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToClickSaveSettings = function () {
	document.querySelector('.js-save-settings').addEventListener('click', function () {
		const url = backend + '/config';
		const body = {};

		for (const setting of document.querySelectorAll('.js-setting')) {
			body[setting.getAttribute('data-name')] = setting.querySelector('input').checked;
		}

		handleData(url, function () {
			toastr.success('Config settings saved successfully!');
		}, showError, 'POST', JSON.stringify(body));
	});
};
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const initPage = function () {
	console.log('settings.js page init');

	getConfigValues();
};
//#endregion

document.addEventListener('DOMContentLoaded', initPage);
