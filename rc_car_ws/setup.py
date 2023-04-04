from setuptools import setup

package_name = 'rc_car_ws'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='son',
    maintainer_email='son@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_pub = rc_car_ws.camera_pub2:main',
            'camera_sub = rc_car_ws.camera_sub2:main',
            'wheel_ros = rc_car_ws.wheel_ros2:main',
            'steer_ros = rc_car_ws.steer_ros2:main',
        ],
    },
)
