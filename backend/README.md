# Tilty backend
Python based backend for Tilty. \
Includes a server and a module for finding the best fit for the calibration data. \
Listens on port 5000 by default.

## Custom calibration 
Custom calibration settings can be provided by defining a file `settings/settings.json`. Look at `settings.json` (which is the default settings file) to see the format.

## Environment variables
`FIT_DEGREES` - number of degrees to use for fitting function \
`DELAY` - number of seconds to tell the Arduino to sleep for after each request \
`URL` - URL of the request to Brewfather