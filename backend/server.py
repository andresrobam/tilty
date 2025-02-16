from requests import post
from flask import Flask, request
from decimal import Decimal
from os import getenv
from numpy.polynomial.polynomial import polyval as value

from common import Calibration, getTemperatureCorrectedGravity

import warnings
import simplejson as json

app = Flask(__name__)

def sendMeasurement(temperature, gravity):
    global brewfatherUrl
    response = post(brewfatherUrl, json = { "name": "tilty", "temp": temperature, "gravity": gravity })
    print("Brewfather responded with {}: {}".format(response.status_code, response.text))


warnings.filterwarnings("ignore")
delaySeconds = getenv("DELAY", "10800")
brewfatherUrl = getenv("URL")

calibration = Calibration()

@app.route("/measurements")
def receiveMeasurement():
    global calibration
    angle = float(request.args.get("angle"))
    rawTemperature = float(request.args.get("temperature"))
    print("Received temperature {} and angle {}.".format(rawTemperature, angle))
    temperature = value(rawTemperature, calibration.thermometerCurve)
    gravity = getTemperatureCorrectedGravity(value(angle, calibration.gravityCurve), temperature, calibration.hydrometerCalibrationTemperature)
    temperature = Decimal("{:.1f}".format(temperature))
    gravity = Decimal("{:.3f}".format(gravity))
    print("Calculated temperature {} and gravity {}.".format(temperature, gravity))
    sendMeasurement(temperature, gravity)

    return delaySeconds

if __name__ == '__main__':
    app.run(host = "0.0.0.0")
