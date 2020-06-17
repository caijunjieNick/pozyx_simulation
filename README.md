# Simulation-of-uwb
this package can simulate the environment with UWB by using Gazebo. It provides the python srcipts to add noise to the Gazebo and compute the global pose(uwb_pose) of turtlebot3(waffle) without orientation. With the help of package "robot localization", the amcl_pose and uwb_pose can be fused to provide a more robust pose estimation.

## Necessary Packages
The repositories with packages (turtlebot3, turtlebot3_msgs, turtlebot3_simulations, robot_localization) need to be cloned into your catkin_ws. 
Note: please choose the level cjj_turtlebot3, cjj_turtlebot3_simulations. These two packages are the new added branchs for the origin master.

# ROS Pozyx Simulation
This package is to simulate the UWB range measurements in ROS environment. Generated data published to “uwb_data_topic” 

![](https://raw.githubusercontent.com/bekirbostanci/ros_pozyx_simulation/master/docs/1.png)

## UWB Anchors Add
The file that contains the UWB anchor information is in "launch/uwb_anchors_set.launch" file. It is possible to add or remove the UWB anchors as you like. </br>
Note : uwb tag frame name should be as follows uwb_anchor_0, uwb_anchor_1, uwb_anchor_2 ...

![](https://raw.githubusercontent.com/bekirbostanci/ros_pozyx_simulation/master/docs/2.png)


## UWB Tag information
Location of the tag has been taken from the robot position so to use this information "modelstate_index" parameter (for turtlebot3 modelstate_index =2) which is in "launch/uwb_simulation_initializing.launch" file must set correctly depending on the robot model used. It is possible to find your own robot parameter in "gazebo/model_states" topic.


## Initialize
Use the command below in terminal to start it with default settings

roslaunch pozyx_simulation uwb_simulation_initializing.launch


## Publish Topic
Name of the publisher topic is "uwb_data_topic". You can check it by using the command below in terminal

rostopic echo /uwb_data_topic

</br>
Message type consists of 3 different arrays <br>
1. anchors name => int64[] destination_id</br>
2. anchors distance to robot => float64[] distance</br>
3. time stamp => time[] stamp</br>

</br>

## Map and Rviz
If you want to start manually with custom maps. You can change map and map configuration in maps folder and start manually with the codes below.

rosrun map_server map_server map.yaml
rosrun rviz rviz
rosrun pozyx_simulation uwb_simulation.py
Note: in launch file, the node for rviz in the uwb_simulation_initializing.launch has been annotated.

## Noise 
Noise has been added to the every UWB ranging data </br> 

np.random.normal(0, uwb_dist*0.015,1)

## Run with Gazebo
please type the command "roslaunch turtlebot3_gazebo uwb_waffle.launch", it will run the Gazebo and load the turtlebot3_world.world. You can also choose the specific world. It includes the launch file "uwb_simulation_initializing.launch" to simulate the uwb environment.

## Add noise to Gazebo
please type the command "rosrun pozyx_simulation add_noise_Gazebo_odometry.py".
Gazebo provides a perfect world without noise for the odom_frame. Therefore, it's necessary to add nosie manually to simulate the real world.

## Compute the uwb_pose of waffle
please type "rosrun pozyx_simulation sqrrange_leastsqr_localization.py". This python script can subscribe the topic "uwb_data_topic" to get the distances between waffle and uwb anchors. And it can compute the pose of waffle and publish the pose to the topic "uwb_pose". The covariance of uwb_pose has been set as static. You can also modify as dynamic covariance.

## Fuse two global poses from different sources
please type "export TURTLEBOT3_MODEL=waffle" and "roslaunch turtlebot3_navigation waffle_uwb_amcl_localization.launch". This launch file aims at fusing the two global poses (uwb_pose and amcl_pose). The "amcl_waffle.launch" has been added to the launch folder of package "turtlebot3_navigation". The parameter "tf_broadcast" has been set as false.

Note: "fusion.launch" uses "ekf_localization_node" in package "robot_localization" and the yaml.file "ekf_amcl_uwb.yaml" exists in the folder "param" of the package "pozyx_simulation". In this yaml.file, /odom, /amcl_pose and /uwb_pose are added. You can also add imu into this file. The "process_noise_covariance" and "initial_estimate_covariance" can be modified.

