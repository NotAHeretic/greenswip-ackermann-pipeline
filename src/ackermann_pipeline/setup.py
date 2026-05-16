from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ackermann_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/urdf', glob('urdf/*')),
        ('share/' + package_name + '/worlds', glob('worlds/*')),
        ('share/' + package_name + '/config', glob('config/*')),
        ('share/' + package_name + '/launch', glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='weirdtune',
    maintainer_email='abhijitmahadik002@gmail.com',
    description='Greenswip Ackermann perception-to-action pipeline',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'perception_node = ackermann_pipeline.perception_node:main',
            'control_node = ackermann_pipeline.control_node:main',
        ],
    },
)
