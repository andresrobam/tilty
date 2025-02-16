from pathlib import Path
from numpy.polynomial.polynomial import polyfit
from os import getenv
import json

def getTemperatureCorrectedGravity(measuredGravity, currentTemperatureCelsius, calibrationTemperatureCelsius):
    if currentTemperatureCelsius == calibrationTemperatureCelsius:
        return measuredGravity
    
    def fahrenheit(celsius):
        return celsius * 1.8 + 32
    
    a = 1.00130346
    b = 0.000134722124
    c = 0.00000204052596
    d = 0.00000000232820948

    t = fahrenheit(currentTemperatureCelsius)
    ct = fahrenheit(calibrationTemperatureCelsius)

    return measuredGravity * ((a - t*(b - c*t + d*t*t )) / (a - ct*(b - c*ct + d*ct*ct)))

def x(values):
    return values[::2]
                
def y(values):
    return values[1::2]

def fit(points, degrees = 1):
    return polyfit(x(points), y(points), degrees)

def loadSettings(calibration, file):
    settings = json.load(file)
    calibration.hydrometerCalibrationTemperature = settings["hydrometerCalibrationTemperature"]
    calibration.calibrationLiquidTemperature = settings["calibrationLiquidTemperature"]
    calibration.temperaturePoints = settings["temperaturePoints"]
    calibration.gravityPoints = settings["gravityPoints"]

class Calibration:
    def __init__(self):

        customSettingsPath = "settings/settings.json"
        filePath = customSettingsPath if Path(customSettingsPath).is_file() else "settings.json"

        with open(filePath, "r") as file:
            print("Loading settings from "+filePath)
            loadSettings(self, file)

        for i in range(1, len(self.gravityPoints), 2):
            measured = self.gravityPoints[i]
            corrected = getTemperatureCorrectedGravity(measured, self.calibrationLiquidTemperature, self.hydrometerCalibrationTemperature)
            self.gravityPoints[i] = corrected
            print("Corrected initial SG measurement of {:.3f} to {:.3f}".format(measured, corrected))

        fitDegrees = int(getenv("FIT_DEGREES", "7"))

        print(f"Using {fitDegrees} degrees for the fit function.")

        self.thermometerCurve = fit(self.temperaturePoints)
        self.gravityCurve = fit(self.gravityPoints, fitDegrees)
