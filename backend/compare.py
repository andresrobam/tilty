import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyval as value
import numpy as np

from common import Calibration, fit, x, y

calibration = Calibration()

plt.figure(1)
plt.plot(x(calibration.temperaturePoints), y(calibration.temperaturePoints), "ro")
newXRange = np.linspace(15, 30)
plt.plot(newXRange, value(newXRange, calibration.thermometerCurve))
plt.xlabel("Measured temperature")
plt.ylabel("Actual temperature")
plt.title("Temperature")

for i in range(10):
    plt.figure(i + 2)
    plt.plot(x(calibration.gravityPoints), y(calibration.gravityPoints), "ro")
    newXRange = np.linspace(x(calibration.gravityPoints)[0], x(calibration.gravityPoints)[-1])
    degrees = i + 1
    plt.plot(newXRange, value(newXRange, fit(calibration.gravityPoints, degrees)))
    plt.xlabel("Angle")
    plt.ylabel("Specific gravity")
    plt.title("Gravity with degrees: {}".format(degrees))
    
plt.show()
