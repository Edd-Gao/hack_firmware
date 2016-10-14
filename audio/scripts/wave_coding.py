#!/usr/bin/env python
import audio.wave
import rospy

from audio_common_msgs.msg import AudioData

def audioCallBack(data):
    print data.data

def audioListener():
    rospy.init_node('VoiceUploader', anonymous=True)

    rospy.Subscriber("/audio", AudioData, audioCallBack)

    # spin() simply keeps python from exiting until this node is stopped

    rospy.spin()

if __name__ == '__main__':
    audioListener()

