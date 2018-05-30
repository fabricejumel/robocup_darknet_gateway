#!/usr/bin/env python  
__author__ ='Raphael Leber'


import rospy 
import actionlib

#from darknet_gateway_srvs.srv import OpenPoseGossip




from darknet_gateway_srvs.srv import ObjectsDetectionGateway_Srv as ODG_Srv

from darknet_ros_msgs.msg import BoundingBox, BoundingBoxes, CheckForObjectsAction



from robocup_msgs.msg import Entity2D, Entity2DList
from sensor_msgs.msg import Image

from process.ObjectsDetectionGateway_process import ObjectsDetectionGateway_process as ODG_process




class ObjectsDetectionGateway_node():

    def __init__(self):

        self.ready = 0

        rospy.init_node('ObjectsDetectionGateway_node', anonymous=False)
        rospy.loginfo("ObjectsDetectionGateway_node init")

        rospy.Subscriber("/pepper_robot/naoqi_driver/camera/front/image_raw", Image, self.img_callback)
        rospy.loginfo("ObjectsDetectionGateway_node topics init")

        #declare ros service 
        self.opg_Srv = rospy.Service('object_detection_gateway_srv', ODG_Srv, self.ODG_SrvCallback)
        rospy.loginfo("ObjectsDetectionGateway_node services init")

        self._actCheckForObjects = actionlib.SimpleActionClient("check_for_objects", CheckForObjectsAction)
        self._actCheckForObjects.wait_for_server(rospy.Duration(10))
        rospy.loginfo("ObjectsDetectionGateway_node actions init")

        self.service_running = 0
        self.ready = 1

        rospy.spin()



    def ODG_SrvCallback(self,req):

        self.service_running = 1

        odg_process = ODG_process()

        #goal = odg_process.CreateGoalFromImage( self.msg_img )

        self._actCheckForObjects.send_goal( self.msg_img )
        self._actCheckForObjects.wait_for_result()

        result = self._actCheckForObjects.get_result()

        e2D = odg_process.BoundingBoxes_to_Entity2DList( result )

        self.service_running = 0

        return e2D

    def img_callback(self, msg_img):
        if self.ready == 1 :
            if self.service_running == 0:
                self.msg_img = msg_img       


def main():
    #""" main function
    #"""
    node = ObjectsDetectionGateway_node()

if __name__ == '__main__':
    main()