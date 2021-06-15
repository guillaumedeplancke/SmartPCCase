'use strict';

const backend_IP = `http://${window.location.hostname}:5000`;
const backend = backend_IP + '/api/v1';
const socketio = io(backend_IP)

//#region ***  DOM references ***
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showError = function () {
	toastr.error("Something went wrong while fetching data from the API.");
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
//#endregion

//#region ***  Data Access - get___ ***
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToSockets = function () {
	socketio.on('connect', function (msg) {
		console.log('Connected to sockets.');
	});

	socketio.on('connect_error', ()=>{
		toastr.error('Socket connection lost!');
	});

	socketio.on('B2F_new_data', function (data) {
		console.log(data);

		for (const category of data) {
			if (document.querySelector('.js-page-index')) { // index page
				let card, valuePlaceholder;
				
				for (const device of category.devices) {
					card = document.querySelector(`.js-category[data-category-id='${category.id}']`);

					if (card) {
						valuePlaceholder = card.querySelector(`.js-value[data-device-id='${device.id}']`);

						if (valuePlaceholder) { // card found with placeholder for the device's value
							if (category.output == true && device.is_pwm == false) {
								valuePlaceholder.innerHTML = device.value ? 'Aan' : 'Uit';
							} else {
								valuePlaceholder.innerHTML = device.value;
							}
						} 
					}
				}

				if (card && !valuePlaceholder) { // card found but no placeholder for the device's value => we have to put a summary of the outputs states
					valuePlaceholder = card.querySelector('.js-value');

					if (valuePlaceholder) {
						let values = category.devices.map(value => value.value);
	
						const areEqualValues = values.every(function (element) {
							return element === values[0];
						});
		
						if (areEqualValues && values[0] > 0) {
							card.querySelector('.js-value').innerHTML = 'Aan';
						} else if (areEqualValues && values[0] == 0) {
							card.querySelector('.js-value').innerHTML = 'Uit';
						} else {
							card.querySelector('.js-value').innerHTML = 'Gedeeltelijk aan';
						}
					}
				}
			}
			
			if (document.querySelector('.js-page-control')) { // control page
				for (const device of category.devices) {
					if (category.output == true) { // we only need to show outputs on the control page
						let card = document.querySelector(`.js-component[data-id='${device.id}']`);
						
						if (card) {
							const toggle = card.querySelector('.js-toggle');
							const slider = card.querySelector('.js-slider');
		
							if (toggle) {
								if (device.value > 0) {
									card.classList.add('u-bg-theme-gradient');
								} else {
									card.classList.remove('u-bg-theme-gradient');
								}
					
								toggle.querySelector('input').checked = device.value;
							}
					
							if (slider) {
								slider.value = device.value;
							}
						}
					}
				}
			}

			if (document.querySelector('.js-page-component')) {
				for (const device of category.devices) {
					const urlParams = new URLSearchParams(window.location.search);
					const deviceId = urlParams.get('id');

					if (category.output == true && device.id == deviceId) {
						if (device.is_pwm == true) {
							const slider = document.querySelector('.js-slider');

							document.querySelector('.js-component-value').innerHTML = device.value + ' %';
							
							if (slider) {
								slider.value = device.value

								if (document.querySelector('.js-slider-value')) {
									document.querySelector('.js-slider-value').innerHTML = device.value;		
								}			
							}
						} else {
							document.querySelector('.js-component-value').innerHTML = device.value ? 'Aan' : 'Uit';
						}
					} else if (device.unit == '°C') {
						document.querySelector('.js-temperature').innerHTML = device.value;
					}
				}
			}
		}
	});

	socketio.on('B2F_output_changed', function (data) {
		const card = document.querySelector(`.js-component[data-id='${data.output._id}']`);

		if (card) {
			const toggle = card.querySelector('.js-toggle');
			const slider = card.querySelector('.js-slider');
			const componentValuePlaceholder = document.querySelector('.js-component-value')

			if (componentValuePlaceholder) {
				componentValuePlaceholder.innerHTML = data.output._latest_value + ' %';
			}

			if (toggle) {
				if (data.output._latest_value > 0) {
					card.classList.add('u-bg-theme-gradient');
				} else {
					card.classList.remove('u-bg-theme-gradient');
				}
	
				toggle.querySelector('input').checked = data.output._latest_value;
			}
	
			if (slider) {
				slider.value = data.output._latest_value;

				const sliderValuePlaceholder = card.querySelector('.js-slider-value');

				if (sliderValuePlaceholder) {
					sliderValuePlaceholder.innerHTML = data.output._latest_value;
				}
			}
		} else {
			const valuePlaceholder = document.querySelector(`.js-value[data-device-id='${data.output._id}']`)

			if (valuePlaceholder) {
				valuePlaceholder.innerHTML = data.output._latest_value;

				if (data.output._is_pwm == false) {
					valuePlaceholder.innerHTML = data.output._latest_value ? 'Aan' : 'Uit';
				}
			}
		}
	});

	socketio.on('B2F_alert', function (data) {
		toastr.success(data.message);
	});
};

const listenToClickNavToggle = function () {
	for (const toggle of document.querySelectorAll('.js-toggle-nav')) {
		toggle.addEventListener('click', function () {
			document.querySelector("body").classList.toggle("has-mobile-nav");
		});
	}
};
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const init = function () {
	console.log('app.js init');

	toastr.options = {
		"closeButton": true,
		"progressBar": true,
		"preventDuplicates": true,
		"positionClass": "toast-bottom-right",
		"showDuration": "500",
  		"hideDuration": "2000",
	};

	listenToSockets();
	listenToClickNavToggle();
};
//#endregion

document.addEventListener('DOMContentLoaded', init);
