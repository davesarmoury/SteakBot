#!/usr/bin/env python3

import rtde_control
import time
import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

BBQ_FRAME = [0,0,0,0,0,0]
FRIDGE_FRAME = [0,0,0,0,0,0]

HOME = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

STEAK = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

FRONT_POUNCE = [-0.1, 0.0, -0.005, 0.0, 0.0, 0.0]
FRONT_POUNCE_UP = [-0.1, 0.0, 0.025, 0.0, 0.0, 0.0]
UNDER = [0.0, 0.0, -0.005, 0.0, 0.0, 0.0]
UP = [0.0, 0.0, 0.025, 0.0, 0.0, 0.0]
TURN_UP = [0.0, 0.025, 0.025, 0.0, 1.4, 1.5707]
TURN = [0.0, 0.0, 0.01, 0.0, 0.0, 1.5707]
RIGHT = [0.0, 0.01, 0.01, -1.0, 0.0, 0.0]
FLIP = [0.0, 0.0, 0.025, -1.5707, 0.0, 0.0]

FORCE = 110.0
FORCE_SPEED = 0.5

TASK_FRAME = [0, 0, 0, 0, 0, 0]
FORCE_TYPE = 2

FORCE_WRENCH = [0, 0, FORCE, 0, 0, 0]  # Set force here
FORCE_VECTOR = [0, 0, -1, 0, 0, 0]
FORCE_LIMITS = [1.0, FORCE_SPEED, 1.0, 1.0, 1.0, 1.0]  # Set Speed Here

def measureThickness(rtde_c, rtde_r):
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)

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

    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)

    zero_height = rtde_c.poseTrans(BBQ_FRAME, STEAK)
    thickness = current_pose[2] - zero_height[2]

    return thickness

def getSteak():
    global rtde_c
    rtde_c.moveJ(HOME)

def placeSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE_UP), 0.25)
    rtde_c.moveJ(HOME)

def turnSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE_UP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, TURN), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, TURN_UP), 0.25)
    rtde_c.moveJ(HOME)

def flipSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE_UP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, RIGHT), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FLIP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, RIGHT), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)
    rtde_c.moveJ(HOME)

def finishSteak():
    global rtde_c
    rtde_c.moveJ(HOME)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE_UP), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, FRONT_POUNCE), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UNDER), 0.25)
    rtde_c.moveL(rtde_c.poseTrans(BBQ_FRAME, UP), 0.25)
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

    return first_time, second_time

def getNextSteak():
    if path.exists("steak.yaml"):
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
    print("Starting Control...")
    global rtde_c
    rtde_c = rtde_control.RTDEControlInterface("192.168.2.66")
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.2.66")
    rtde_c.setTcp([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    rtde_c.setPayload(0.5, [0,0,0])

    while(True):
        cook, meat = getNextSteak()

        if cook != None and meat != None:
            getSteak(meat)

            place_time = time.time()
            placeSteak()
            delta_time = time.time() - place_time

            thickness = measureThickness()
            first_time, second_time = getCookTimes(thickness, cook)

            turn1 = threading.Timer(first_time/2.0 - delta_time, turnSteak)
            turn1.start()
            flip = threading.Timer(first_time - delta_time, flipSteak)
            flip.start()
            turn2 = threading.Timer(first_time + second_time/2.0 - delta_time, turnSteak)
            turn2.start()
            finish = threading.Timer(first_time + second_time - delta_time, finishSteak)
            finish.start()

            while(True):
                if turn1.is_alive() or turn2.is_alive() or finish.is_alive() or flip.is_alive():
                    print(str( place_time + first_time + second_time - time.time() ) )
                    time.sleep(1)
                else:
                    break

        os.remove("steak.yaml")

main()
