from setuptools import setup, find_packages
import sys

if sys.version_info <= (2, 5):
    error = "ERROR: calamari-alert requires Python Version 2.6 or above...exiting."
    print(error)
    sys.exit(1)

requirements = [
    'paho-mqtt>=1.1',
]

setup(
    name='mqtt-benchmark',
    version='0.1.0',
    packages=find_packages(),
    description='MQTT Benchmark Client',
    author='Kyle Bai',
    author_email='kyle.b@inwinstack.com',
    url='http://www.inwinstack.com/',
    install_requires=requirements,
    license="MIT",
    entry_points={
        'console_scripts': [
            'mqtt-bench = mqtt_benchmark.cli:main',
        ],
    },
)