from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def convert_length(value, from_unit, to_unit):
    to_meter = {
        'millimeter': 0.001, 'centimeter': 0.01, 'meter': 1,
        'kilometer': 1000, 'inch': 0.0254, 'foot': 0.3048,
        'yard': 0.9144, 'mile': 1609.344
    }
    return value * to_meter[from_unit] / to_meter[to_unit]


def convert_weight(value, from_unit, to_unit):
    to_kg = {
        'milligram': 0.000001, 'gram': 0.001, 'kilogram': 1,
        'ounce': 0.0283495, 'pound': 0.453592
    }
    return value * to_kg[from_unit] / to_kg[to_unit]


def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'Celsius':
        celsius = value
    elif from_unit == 'Fahrenheit':
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    if to_unit == 'Celsius':
        return celsius
    elif to_unit == 'Fahrenheit':
        return celsius * 9 / 5 + 32
    else:
        return celsius + 273.15


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    category = data.get('category')
    value = float(data.get('value'))
    from_unit = data.get('from_unit')
    to_unit = data.get('to_unit')

    try:
        if category == 'Length':
            result = convert_length(value, from_unit, to_unit)
        elif category == 'Weight':
            result = convert_weight(value, from_unit, to_unit)
        elif category == 'Temperature':
            result = convert_temperature(value, from_unit, to_unit)
        else:
            return jsonify({'error': 'Unknown category'}), 400

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
