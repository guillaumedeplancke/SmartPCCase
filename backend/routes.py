from __main__ import endpoint, app, config
from flask import jsonify, request
from utils import serialize, serialize_simple
import sys
import os

# Repositories
from repositories.DataRepository import DataRepository
from repositories.SensorRepository import SensorRepository
from repositories.SensorHistoryRepository import SensorHistoryRepository
from repositories.OutputRepository import OutputRepository
from repositories.OutputHistoryRepository import OutputHistoryRepository
from repositories.CategoryRepository import CategoryRepository


# Routes: Config

@app.route(endpoint + '/config', methods=['GET', 'POST'])
def get_config():
    if request.method == 'GET':
        return jsonify(config=serialize_simple(config)['data'])
    elif request.method == 'POST':
        data = DataRepository.json_or_formdata(request)

        for key, value in data.items():
            config[key] = value
        
        config.save()

        return jsonify(status='success'), 202


# Model: Sensor

@app.route(endpoint + '/sensors')
def sensors():
    sensors = SensorRepository.all()

    if sensors is not None:
        return jsonify(sensors=serialize(sensors))
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/sensor/<sensor_id>')
def sensor(sensor_id):
    sensor = SensorRepository.find(sensor_id)

    if sensor is not None:
        return jsonify(sensor=serialize(sensor))
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/sensor/<sensor_id>/history')
def sensor_history(sensor_id):
    history = SensorHistoryRepository.get(sensor_id)

    if history is not None:
        return jsonify(history=history)
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/sensor/<sensor_id>/history/<date>')
def sensor_history_for_date(sensor_id, date):
    history = SensorHistoryRepository.get_for_date(sensor_id, date)

    if history is not None:
        return jsonify(history=history)
    else:
        return jsonify(status='error', message='not found'), 404


# Model: Output

@app.route(endpoint + '/outputs')
def outputs():
    outputs = OutputRepository.all()

    if outputs is not None:
        return jsonify(outputs=serialize(outputs))
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/output/<output_id>')
def output(output_id):
    output = OutputRepository.find(output_id)

    if output is not None:
        return jsonify(output=serialize(output))
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/output/<output_id>/history/today')
def output_history(output_id):
    history = OutputHistoryRepository.get(output_id)

    if history is not None:
        return jsonify(history=history)
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/output/<output_id>/history/latest')
def output_history_latest(output_id):
    history = OutputHistoryRepository.get_latest_10(output_id)

    if history is not None:
        return jsonify(history=history)
    else:
        return jsonify(status='error', message='not found'), 404


# Model: Category


@app.route(endpoint + '/categories')
def categories():
    categories = CategoryRepository.all()

    if categories is not None:
        return jsonify(categories=serialize(categories))
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/categories/seeded')
def categories_seeded():
    data = CategoryRepository.all_seeded()

    if data is not None:
        return jsonify(categories=serialize(data))
    else:
        return jsonify(status='error', message='not found')


@app.route(endpoint + '/category/<category_id>')
def category(category_id):
    category = CategoryRepository.find(category_id)

    if category is not None:
        return jsonify(category=serialize(category))
    else:
        return jsonify(status='error', message='not found'), 404


@app.route(endpoint + '/category/<category_id>/devices')
def category_devices(category_id):
    devices = CategoryRepository.devices(category_id)

    if devices is not None:
        return jsonify(serialize(devices))
    else:
        return jsonify(status='error', message='not found'), 404
