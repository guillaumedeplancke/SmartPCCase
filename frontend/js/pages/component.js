'use strict';

//#region ***  Variables ***
let output;
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showOutput = function (data) {
	output = data.output;

	document.querySelector('.js-component-name').innerHTML = output._name;
	document.querySelector('.js-component').setAttribute('data-id', output._id);

	if (output._is_pwm) {
		document.querySelector('.js-control').innerHTML = `
		<div class="c-component__description">
			<p class="c-description__title">Value</p>
			<p class="c-description__value u-float-right"><span class="js-slider-value">--</span> %</p>
		</div>
		<input class="js-slider c-slider c-slider--lg" type="range" min="0" max="100" value="0" data-id=${output._id}>
		`;

		listenToChangeSlider();
	} else {
		document.querySelector('.js-control').innerHTML = `
		<div class="c-control-group">
			<p class="u-mb-clear">${output._name}</p>
			<label class="c-toggle js-toggle" data-id=${output._id}>
				<input class="c-toggle__input" type="checkbox">
				<span class="c-toggle__slider"></span>
			</label>
		</div>
		`;

		listenToChangeToggle();
	}
}

const showHistory = function (data) {
	let timelineInnerHTML = ``;
	let cardsInnerHTML = ``;
	let i = 0;

	for (const historyItem of data.history) {
		timelineInnerHTML += `<div class="c-timeline__dot">`;

		if (i !== data.history.length - 1) {
			timelineInnerHTML += `</div><div class="c-timeline__line"></div>`;
		}

		cardsInnerHTML += `
		<div class="c-card c-history__card">
			<h4 class="u-mb-xs">Value changed to: ${historyItem.value}</h4>
			<p class="u-mb-clear">${historyItem.date}, ${historyItem.time}</p>
		</div>`;

		i++;
	}

	const history = document.querySelector('.js-history');
	history.querySelector('.js-timeline').innerHTML = timelineInnerHTML;
	history.querySelector('.js-cards').innerHTML = cardsInnerHTML;
}

const showChart = function (data) {
	let converted_labels = []
	let converted_data = []

	for (const entry of data.history) {
		let data = [
			new Date(entry.datetime).getTime(),
			entry.value
		]

		converted_data.push(data);
	}

	let options = {
		chart: {
			id: 'chart',
			height: 380,
			width: '100%',
			type: 'line',
			animations: {
			  initialAnimation: {
				enabled: false
			  }
			},
			toolbar: {
				autoSelected: 'pan',
			}
		  },
		  stroke: {
			curve: 'smooth',
		  },
		  series: [
			{
			  name: "Series 1",
			  data: converted_data
			}
		  ],
		  xaxis: {
			type: 'datetime'
		  }
	}

	/*if (output['_is_pwm'] !== undefined) {
		if (output._is_pwm == false) {
			options['stroke']['curve'] = 'stepline';
		}
	}*/

	let chart = new ApexCharts(document.querySelector('.js-chart'), options);
	chart.render();
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
//#endregion

//#region ***  Data Access - get___ ***
const getOutput = function (outputId) {
	const url = backend + `/output/${outputId}`;
	handleData(url, showOutput, showError);
}

const getHistoryToday = function (outputId) {
	const url = backend + `/output/${outputId}/history/today`;
	handleData(url, showChart, showError);
}

const getLatestHistory = function (outputId) {
	const url = backend + `/output/${outputId}/history/latest`;
	handleData(url, showHistory, showError);
}
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToChangeSlider = function () {
	document.querySelector('.js-slider').addEventListener('change', function () {
		const output_id = this.getAttribute('data-id');
		
		socketio.emit('F2B_change_output', { output_id: output_id, change_to: this.value });
	});
	
	document.querySelector('.js-slider').addEventListener('input', function () {
		document.querySelector('.js-slider-value').innerHTML = document.querySelector('.js-slider').value
	});
};

const listenToChangeToggle = function () {
	for (const toggle of document.querySelectorAll('.js-toggle')) {
		toggle.addEventListener('change', function () {
			let change_to_value;
			const checkbox = this.querySelector('input[type=checkbox]');

			if (checkbox.checked) {
				change_to_value = 1;
			} else {
				change_to_value = 0;
			}

			socketio.emit('F2B_change_output', { output_id: this.getAttribute('data-id'), change_to: change_to_value });
		});
	}
};
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const initPage = function () {
	console.log('component.js page init');

	const urlParams = new URLSearchParams(window.location.search);

	if (urlParams.get('id')) {
		const id = urlParams.get('id');

		getOutput(id);
		getHistoryToday(id);
		getLatestHistory(id);
	} else {
		window.location.href = `control.html`;
	}
};
//#endregion

document.addEventListener('DOMContentLoaded', initPage);
