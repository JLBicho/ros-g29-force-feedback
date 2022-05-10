import os

from matplotlib.pyplot import eventplot
from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import  DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def find_handlers():
    stream = os.popen("cat /proc/bus/input/devices")
    stream = stream.read().split('\n')
    found_name = False
    for line in stream:
        if('N: Name="Logitech G29 Driving Force Racing Wheel"' in line or found_name):
            if(not found_name):
                idx = stream.index(line)
            else:
                idx = idx+1
            #print(f"{idx}: {line}")
            found_name = True
            if(line == ""):
                found_name = False
            if("H: Handlers" in line):
                handlers = line.split("=")[1].split(" ")
                for h in handlers:
                    if h.startswith("event"):
                        print("--> Found handler at /dev/input/"+h)
                        return(h)

def generate_launch_description():

    event = find_handlers()
    
    params_file = "g29.yaml" 
    params = os.path.join(
        get_package_share_directory('ros_g29_force_feedback'),
        "config",
        params_file)
        
    g29_ff = Node(
            package="ros_g29_force_feedback",
            executable="g29_force_feedback",
            name="g29_force_feedback",
            namespace=LaunchConfiguration("namespace"),
            output="screen",
            parameters=[params, {"device_name":"/dev/input/"+event}])

    return LaunchDescription([
        DeclareLaunchArgument("namespace",
            default_value="",
            description="Namespace for the node"),
        g29_ff
    ])