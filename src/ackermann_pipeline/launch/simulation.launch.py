from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_path = get_package_share_directory('ackermann_pipeline')

    world_path = os.path.join(pkg_path, 'worlds', 'shapes.sdf')
    urdf_path = os.path.join(pkg_path, 'urdf', 'robot.urdf')
    bridge_config = os.path.join(pkg_path, 'config', 'bridge.yaml')

    gz = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    spawn = TimerAction(period=3.0, actions=[
        ExecuteProcess(
            cmd=['ros2', 'run', 'ros_gz_sim', 'create',
                 '-file', urdf_path,
                 '-name', 'ackerman_2',
                 '-x', '1.0', '-y', '0.0', '-z', '0.15'],
            output='screen'
        )
    ])

    bridge = TimerAction(period=5.0, actions=[
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['--ros-args', '-p',
                       f'config_file:={bridge_config}'],
            output='screen',
            emulate_tty=True
        )
    ])

    perception = TimerAction(period=7.0, actions=[
        Node(
            package='ackermann_pipeline',
            executable='perception_node',
            output='screen',
            emulate_tty=True
        )
    ])

    control = TimerAction(period=7.0, actions=[
        Node(
            package='ackermann_pipeline',
            executable='control_node',
            output='screen',
            emulate_tty=True
        )
    ])

    return LaunchDescription([
        gz,
        spawn,
        bridge,
        perception,
        control
    ])