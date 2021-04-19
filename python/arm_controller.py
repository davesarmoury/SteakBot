#!/usr/bin/env python3

import rtde_control
import rtde_receive
import time
import os
import threading
from scipy.spatial.transform import Rotation as R

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

BBQ_FRAME = [-0.454, -0.0733, -0.06943, 0.036, 0.054, 3.14159]
FRIDGE_FRAME = [0,0,0,0,0,0]
TCP_FRAME = [-0.125, 0.125, 0.05, 1.76, -0.729, 1.76]
HOME = [1.5707, -2.0944, 2.0944, 0.0, 1.5707, 2.35619]

STEAK = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

FRONT_POUNCE = [-0.1, 0.0, -0.005, 0.0, 30.0, 0.0]
FRONT_POUNCE_UP = [-0.1, 0.0, 0.05, 0.0, 30.0, 0.0]
UNDER = [0.0, 0.0, -0.005, 0.0, 0.0, 0.0]
UP = [0.0, 0.0, 0.05, 0.0, 0.0, 0.0]
TURN = [0.0, 0.0, 0.05, 0.0, 45.0, 90.0]
TURN_UP = [0.0, 0.0, 0.09, 0.0, 90, 90.0]
RIGHT = [0.0, -0.15, 0.1, -40.0, 0.0, 0.0]
FLIP = [0.0, -0.08, 0.15, -80.0, 0.0, 0.0]

FORCE = 25.0
FORCE_SPEED = 0.2

TASK_FRAME = [0, 0, 0, 3.14159, 0, 0]
FORCE_TYPE = 2

FORCE_WRENCH = [0, 0, FORCE, 0, 0, 0]  # Set force here
FORCE_VECTOR = [0, 0, 1, 0, 0, 0]
FORCE_LIMITS = [1.0, FORCE_SPEED, 1.0, 1.0, 1.0, 1.0]  # Set Speed Here

def measureThickness(rtde_c, rtde_r):
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UP), 0.25)

    dt = 1.0/100
    for i in range(200):
        start = time.time()

        rtde_c.forceMode(TASK_FRAME, FORCE_VECTOR, FORCE_WRENCH, FORCE_TYPE, FORCE_LIMITS)

        end = time.time()
        duration = end - start

        if duration < dt:
            time.sleep(dt - duration)

    rtde_c.forceModeStop()

    current_pose = rtde_r.getActualTCPPose()

    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UP), 0.25)

    zero_height = getPose(rtde_c, BBQ_FRAME, STEAK)
    thickness = ( current_pose[2] - zero_height[2] ) * 1000

    return thickness

def getSteak(meat):
    global rtde_c
    rtde_c.moveJ(HOME)

def getAxisAngle(pose):
    r = R.from_euler('ZYX', [pose[5], pose[4], pose[3]], degrees=True)
    rv = r.as_rotvec()
    return [pose[0], pose[1], pose[2], rv[0], rv[1], rv[2]]

def getPose(rtde_c, f1, f2):
    return rtde_c.poseTrans(f1, getAxisAngle(f2))

def placeSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveJ_IK(getPose(rtde_c, BBQ_FRAME, UP))
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE_UP), 0.25)

def turnSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveJ_IK(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE_UP))
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UP), 0.25)
    rtde_c.moveJ_IK(getPose(rtde_c, BBQ_FRAME, TURN))
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, TURN_UP), 0.25)
    rtde_c.moveJ(HOME)

def flipSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveJ_IK(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE_UP))
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UP), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, RIGHT), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, FLIP), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, RIGHT), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UP), 0.25)
    rtde_c.moveJ(HOME)

def finishSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveJ_IK(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE_UP))
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(getPose(rtde_c, BBQ_FRAME, UP), 0.25)
    rtde_c.moveJ(HOME)

def getCookTimes(thickness, cook):
    first_time = -1
    second_time = -1

    if cook == 0:
        first_time = 0.129 * thickness + 1.11
        second_time = 0.114 * thickness + 0.131
    if cook == 1:
        first_time = 0.157 * thickness + 1.0
        second_time = 0.139 * thickness + 0.53
    if cook == 2:
        first_time = 0.15 * thickness + 2.01
        second_time = 0.169 * thickness - 0.0179
    if cook == 3:
        first_time = 0.172 * thickness + 2.45
        second_time = 0.187 * thickness + 0.423
    if cook == 4:
        first_time = 0.193 * thickness + 2.88
        second_time = 0.204 * thickness + 0.863

    first_time = first_time * 60.0
    second_time = second_time * 60.0

    return first_time, second_time

def getNextSteak():
    if os.path.exists("steak.yaml"):
        try:
            inFile = open("steak.yaml", 'r')
            data = load(inFile, Loader=Loader)
            inFile.close()

            cook = data["cook"]
            meat = data["meat"]
            return cook, meat
        except:
            pass
    else:
        return None, None

def main():
    print("Starting Control... <" + str(os.getpid()) + ">")
    global rtde_c
    rtde_c = rtde_control.RTDEControlInterface("192.168.2.66")
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.2.66")
    rtde_c.setTcp(TCP_FRAME)
    rtde_c.setPayload(0.5, [0,0,0])

    while(True):
        cook, meat = getNextSteak()

        if cook != None and meat != None:
            getSteak(meat)

            place_time = time.time()
            placeSteak()
            delta_time = time.time() - place_time

            thickness = measureThickness(rtde_c, rtde_r)
            print("THICKNESS: " + str(thickness))
            first_time, second_time = getCookTimes(thickness, cook)
            print("TIMES: < " + str(first_time) + ", " + str(second_time) + " >")
            rtde_c.moveJ(HOME)

            if first_time > 0 and second_time > 0:
                turn1 = threading.Timer(first_time/2.0 - delta_time, turnSteak)
                #turn1.start()
                flip = threading.Timer(first_time - delta_time, flipSteak)
                #flip.start()
                turn2 = threading.Timer(first_time + second_time/2.0 - delta_time, turnSteak)
                #turn2.start()
                finish = threading.Timer(first_time + second_time - delta_time, finishSteak)
                finish.start()

                while(True):
                    if turn1.is_alive() or turn2.is_alive() or finish.is_alive() or flip.is_alive():
                        print(str( int( ( time.time() - place_time ) / ( first_time + second_time ) * 100 ) )  + " %" )
                        time.sleep(1)
                    else:
                        print("MmmmMmMMMMMmmm")
                        break
            else:
                print("Measurement Error")

            os.remove("steak.yaml")

main()
