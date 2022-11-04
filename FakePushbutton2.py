#!/usr/bin/env python3

from std_msgs.msg import Int8, Bool
import requests
import rospy
from random import randrange
from datetime import datetime
import sys, select, termios, tty
import asyncio
from clickplc import ClickPLC

async def set():
    async with ClickPLC('169.254.183.12') as plc:
   #async with ClickPLC('10.128..4') as plc:   

        if await plc.get('y001') == (True):
          print('green push button activated')
        else:
          print('green push button not activated')

        if await plc.get('y002') == (True):
          print('red push button activated')
        else:
          print('red push ')
asyncio.run(set())
 
    key_mapping = {
   	 	'1': True,
    	'	2': False
}

    key_mapping_cols = {
    	'1': "\033[92mGREEN\033[0m",
    	'2': "\033[91mRED\033[0m"
}


    class FakePushbutton:
	    def __init__(self):
		     self.pub = rospy.Publisher("/pushbutton_input", Bool, queue_size=10)
		     self.settings = termios.tcgetattr(sys.stdin)

	    def publish_msg(self,data):
		     msg = Bool()
		     msg.data = data
		     self.pub.publish(msg)
		

	    def getKey(self):
		     tty.setraw(sys.stdin.fileno())
		     rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
		     if rlist:
		     	      key = sys.stdin.read(1)
		     else:
		         key = ''

		     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
		     # print(key)
		     return key

	    def log(self, message):
		     with open('/home/administrator/uld-management/ksc-uld-management/src/ksc_uld_manager/scripts/state.log', 'a') as f:
		         f.write(message)
		     f.close()

	    if __name__ == '__main__':

	         try:
                    rospy.init_node('FakePushbutton', anonymous=True)
                    faker = FakePushbutton()
		# rospy.init_node('RS_Processor')
                    print("[NODE] FakePushbutton init")
                    print("[USAGE] '1' = \033[92mGREEN\033[0m Button Push, '2' = \033[91mRED\033[0m Button Push, 'q' = Quit")

		
		# faker.log("[FakePushbutton]:\t{}\t-\tInit\n".format(datetime.now()))
		
                    while not rospy.is_shutdown():

                        key = faker.getKey()
                        if key in ['1', '2']:

		        # faker.log("[FakePushbutton]:\t{}\t-\t'{}' detected. Publishing {}\n".format(datetime.now(), key,key_mapping[key]))
                            print("[FakePushbutton]:\t{}\t-\t'{}' detected. Simulates {} Button Push.  ROS: Publishing {}\n".format(datetime.now(), key,  key_mapping_cols[key], key_mapping[key]))
                            faker.publish_msg(key_mapping[key])
		        
                        elif key == 'q':
		        # faker.log("[FakePushbutton]:\t{}\t-\t'{}' detected. Quitting...\n".format(datetime.now(), key))
                            print("[FakePushbutton]:\t{}\t-\t'{}' detected. Quitting...\n".format(datetime.now(), key))
                            break

		
    #except rospy.ROSInterruptException: pass
