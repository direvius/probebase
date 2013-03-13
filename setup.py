from distutils.core import setup

setup(
    name="probebase",
    packages=["probebase"],
    version="0.1.1",
    description="Base for monitoring probe",
    author="Alexey Lavrenuke (load testing)",
    author_email="direvius@yandex-team.ru",
    url="https://github.com/direvius/probebase",
    keywords=["monitoring", "probe", "graphite"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        ],
    install_requires=[
        "lockfile"
    ],
    long_description="""\
Base for monitoring probe
-------------------------

A base for the monitoring probe that takes multiple probes,
runs them once in a selected period of time, collects data
from them and send they to the selected listeners.
"""
)
