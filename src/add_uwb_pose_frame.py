#!/usr/bin/env python
import rospy
import tf
import math
from geometry_msgs.msg import Pose


def handle_uwb_pose(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.position.x, msg.position.y, 0),
                     (0.0, 0.0, 0.0, 1.0),
                     rospy.Time.now(),
                     "uwb_base_link",
                     "map")

if __name__ == '__main__':
    rospy.init_node("uwb_pose_tf_broadcaster")

    rospy.Subscriber('localization_data_topic',
                     Pose,
                     handle_uwb_pose)
    rospy.spin()
