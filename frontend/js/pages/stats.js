'use strict';
let chart;

//#region ***  Variables ***
const date = new Date();
let selectedSensorName;
let selectedSensorId;
//#endregion

//#region ***  Callback-Visualisation - show___ ***
const showFilters = function (data) {
	let newInnerHTML = '';

	for (const sensor of data.sensors) {
		newInnerHTML += `<p class="c-label js-filter" data-sensor-id=${sensor._id}>${sensor._name}</p>`;
	}

	document.querySelector('.js-filters').innerHTML = newInnerHTML;

	listenToClickFilter();
}

const showChart = function (data) {
	let converted_data = []

	if (data.history.length < 1) {
		toastr.warning('No data found for the selected date.');
		return;
	}

	for (const entry of data.history) {
		let data = [
			new Date(entry.datetime).getTime(),
			entry.value
		]

		converted_data.push(data);
	}


	ApexCharts.exec('chart', 'updateOptions', {
		series: [
			{
			  name: selectedSensorName,
			  data: converted_data
			}
		],
	}, false, true);

	toastr.success('Chart updated with new data.');
}

const showDatepickerCurrentDate = function () {
	/* source: https://gomakethings.com/setting-a-date-input-to-todays-date-with-vanilla-js/ */
	const todayDateString = date.getFullYear().toString() + '-' + 
		(date.getMonth() + 1).toString().padStart(2, 0) + '-' + 
		date.getDate().toString().padStart(2, 0);

	document.querySelector('.js-datepicker').value = todayDateString;
	document.querySelector('.js-datepicker').setAttribute('max', todayDateString);	
}
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***
//#endregion

//#region ***  Data Access - get___ ***
const getSensors = function () {
	const url = backend + '/sensors';
	handleData(url, showFilters, showError);
}

const getSensorHistory = function (sensor_id) {
	const url = backend + `/sensor/${sensor_id}/history`;
	handleData(url, showChart, showError);

	showDatepickerCurrentDate();
}

const getSensorHistoryForDate = function (sensor_id, date) {
    const url = backend + `/sensor/${sensor_id}/history/${date}`;
	handleData(url, showChart, showError);
}
//#endregion

//#region ***  Event Listeners - listenTo___ ***
const listenToClickFilter = function () {
	for (const filter of document.querySelectorAll('.js-filter')) {
		filter.addEventListener('click', function () {
			const id = this.getAttribute('data-sensor-id');
			selectedSensorName = this.innerHTML;
			selectedSensorId = id;

			getSensorHistory(id);

			for (const filter of document.querySelectorAll('.js-filter')) {
				if (filter.classList.contains('c-label--active')) {
					filter.classList.remove('c-label--active');
				}
			}

			this.classList.add('c-label--active');

			document.querySelector('.js-datepicker').disabled = false;
		})
	}
}

const listenToChangeDatepicker = function () {
	document.querySelector('.js-datepicker').addEventListener('change', function() {
		console.log('date changed!');
		console.log(document.querySelector('.js-datepicker').value)
		getSensorHistoryForDate(selectedSensorId, document.querySelector('.js-datepicker').value)
	})
}
//#endregion

//#region ***  INIT / DOMContentLoaded  ***
const initPage = function () {
	console.log('stats.js page init');

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
			zoom: {
				autoScaleYaxis: true
			},
			toolbar: {
				autoSelected: 'pan',
			}
		  },
		  stroke: {
			curve: 'smooth',
		  },
		  series: [],
		  xaxis: {
			type: 'datetime'
		  },
		  tooltip: {
			shared: true,
			x: {
			  show: false,
			  formatter(timestamp) {
				return new Date(timestamp)
			  },
			},
		  },
		  toolbar: {
			autoSelected: 'pan' 
		  },
	}

	chart = new ApexCharts(document.querySelector('.js-chart'), options);
	chart.render();

	showDatepickerCurrentDate();

	document.querySelector('.js-datepicker').disabled = true;

	listenToChangeDatepicker();
	getSensors();
};
//#endregion

document.addEventListener('DOMContentLoaded', initPage);
