Base for monitoring probe
-------------------------

A base for the monitoring probe that takes multiple probes,
runs them once in a selected period of time, collects data
from them and send they to the selected listeners.

How to use
----------
1. Install
2. Create a probe function(s) that returns a collection of (metric, value, timestamp) triplets
3. Pass those function(s) to the AppBuilder
4. Add any additional command-line options via add_option method
5. Get an App object from AppBuilder with create() method
6. Invoke a launch() method of the App object. It will automatically detect any command-line options
and run an application in daemonized or interactive mode.