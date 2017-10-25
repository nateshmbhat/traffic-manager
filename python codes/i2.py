import mraa
import time
atrigpin = 22
aechopin = 23

btrigpin = 24
bechopin = 25

ctrigpin = 26
cechopin = 27

aredpin =mraa.Gpio(21)
bredpin =mraa.Gpio(0)
credpin = mraa.Gpio(20)
dredpin = mraa.Gpio(14)

aredpin.dir(mraa.DIR_OUT)
bredpin.dir(mraa.DIR_OUT)
credpin.dir(mraa.DIR_OUT)
dredpin.dir(mraa.DIR_OUT)

ayellowpin = mraa.Gpio(36)
byellowpin = mraa.Gpio(48)
cyellowpin = mraa.Gpio(47)
dyellowpin = mraa.Gpio(33)

ayellowpin.dir(mraa.DIR_OUT)
byellowpin.dir(mraa.DIR_OUT)
cyellowpin.dir(mraa.DIR_OUT)
dyellowpin.dir(mraa.DIR_OUT)

agreenpin = mraa.Gpio(46)
bgreenpin = mraa.Gpio(32)
cgreenpin = mraa.Gpio(45)
dgreenpin = mraa.Gpio(31)

agreenpin.dir(mraa.DIR_OUT)
bgreenpin.dir(mraa.DIR_OUT)
cgreenpin.dir(mraa.DIR_OUT)
dgreenpin.dir(mraa.DIR_OUT)

"""
acamerapin = A0
bcamerapin = A1
ccamerapin = A2
dcamerapin = A3"""

mailsendornot = 0

atraffic = 1
btraffic = 1
ctraffic = 1
dtraffic = 1
numbypass = 0
acount = 0
bcount = 0
ccount = 0
dcount = 0

g = 1



def sensorvalue(trigpin, echopin):
    trigpin.write(0)
    sleepMicroseconds(2)
    trigpin.write(1)
    sleepMicroseconds(10)
    trigpin.write(0)
    return pulseIn(echopinIGH) / 58


def command(gs):
    es
    time.sleep(.1000)


def decisionmake(atraffic, btraffic, ctraffic, dtraffic):
    if (atraffic == 0 and btraffic == 0 and ctraffic == 0 and dtraffic == 0):
        agreenpin.write( 0)
        aredpin.write(0)
        bgreenpin.write( 0)
        bredpin.write(0)
        cgreenpin.write( 0)
        credpin.write(0)
        dgreenpin.write( 0)
        dredpin.write(0)
        ayellowpin.write(1)
        byellowpin.write(1)
        cyellowpin.write(1)
        dyellowpin.write(1)

    elif (atraffic == 0 and btraffic == 0 and dtraffic == 0 and ctraffic != 0):
        cgreenpin.write( 0)
        credpin.write(0)
        cyellowpin.write(1)
    elif (btraffic == 0 and ctraffic == 0 and dtraffic == 0 and atraffic != 0):
        agreenpin.write( 0)
        aredpin.write(0)
        ayellowpin.write(1)
    elif (ctraffic == 0 and atraffic == 0 and dtraffic == 0 and btraffic != 0):
        bgreenpin.write( 0)
        bredpin.write(0)
        byellowpin.write(1)
    elif (ctraffic == 0 and atraffic == 0 and btraffic == 0 and dtraffic != 0):
        dgreenpin.write( 0)
        dredpin.write(0)
        dyellowpin.write(1)


def turngreen(pin):
    aredpin.write(1)
    bredpin.write(1)
    credpin.write(1)
    dredpin.write(1)
    agreenpin.write( 0)
    bgreenpin.write( 0)
    cgreenpin.write( 0)
    dgreenpin.write( 0)
    if (pin == agreenpin):
        aredpin.write(0)
        agreenpin.write( 1)
    if (pin == bgreenpin):
        bredpin.write(0)
        bgreenpin.write( 1)
    if (pin == cgreenpin):
        credpin.write(0)
        cgreenpin.write( 1)
    if (pin == dgreenpin):
        dredpin.write(0)
        dgreenpin.write( 1)

    if (ayellowpin.read() == 1):
        aredpin.write(0)
        agreenpin.write( 0)
    if (byellowpin.read() == 1):
        bredpin.write(0)
        bgreenpin.write( 0)

    if (cyellowpin.read() == 1):
        credpin.write(0)
        cgreenpin.write( 0)
    if (dyellowpin.read() == 1):
        dredpin.write(0)
        dgreenpin.write( 0)


def bypass_and_count_increase(acm, bcm, ccm, dcm):
    global acount, numbypass, bcount, ccount
    if (acm < 6):
        acount += 1
        if (aredpin.read()):
            acamerapin.write(1)
            time.sleep(.250)
            acamerapin.write(0)
            numbypass += 1

    if (bcm < 6):
        bcount += 1
        if (bredpin.read()):
            bcamerapin.write(1)
            time.sleep(.250)
            bcamerapin.write(0)
            numbypass += 1

    if (ccm < 6):
        ccount += 1
        if (credpin.read()):
            ccamerapin.write(1)
            time.sleep(.250)
            ccamerapin.write(0)
            numbypass += 1
    if (dcm < 6):
        ccount += 1
        if (dredpin.read()):
            dcamerapin.write(1)
            time.sleep(.250)
            dcamerapin.write(0)
            numbypass += 1


def loop():
    global atraffic, btraffic, ctraffic, dtraffic
    acm = 10
    bcm = 10
    ccm = 10
    dcm = 10
    acount = 10
    bcount = 10
    ccount = 10
    dcount = 10
    numbypass = 0

    decisionmake(atraffic, btraffic, ctraffic, dtraffic)

    for i in range(3):
        for loopcounter in range(10):

            if (acm == 0 or bcm == 0 or ccm == 0 or dcm == 0):
                continue
            loopcounter += 1

            if not (ctraffic == 0 and btraffic == 0 and dtraffic == 0):
                ayellowpin.write(0)
                turngreen(agreenpin)

            bypass_and_count_increase(acm, bcm, ccm, dcm)
            time.sleep(.500)

        for loopcounter in range(10):

            if (acm == 0 or ccm == 0 or ccm == 0 or dcm == 0):
                continue
            loopcounter += 1

            if not (ctraffic == 0 and atraffic == 0 and dtraffic == 0):
                byellowpin.write(0)
                turngreen(bgreenpin)

            bypass_and_count_increase(acm, bcm, ccm, dcm)

            time.sleep(.500)

        for loopcounter in range(10):

            if (acm == 0 or bcm == 0 or ccm == 0 or dcm == 0):
                continue
            loopcounter += 1

            if not (btraffic == 0 and atraffic == 0 and dtraffic == 0):
                cyellowpin.write(0)
                turngreen(cgreenpin)

            bypass_and_count_increase(acm, bcm, ccm, dcm)

            time.sleep(.500)

        for loopcounter in range(10):
            if (acm == 0 or bcm == 0 or ccm == 0 or dcm == 0):
                continue
            loopcounter += 1

            if not (btraffic == 0 and atraffic == 0 and ctraffic == 0):
                dyellowpin.write(0)
                turngreen(dgreenpin)

            bypass_and_count_increase(acm, bcm, ccm, dcm)

            time.sleep(.500)

    if (acount < 10):
        atraffic = 0
    else:
        atraffic = 1
    if (bcount < 10):
        btraffic = 0
    else:
        btraffic = 1
    if (ccount < 10):
        ctraffic = 0
    else:
        ctraffic = 1
    if (dcount < 10):
        dtraffic = 0
    else:
        dtraffic = 1

    if (atraffic == 1 and btraffic == 1 and dtraffic == 1):
        ctraffic = 1
    elif (btraffic == 1 and ctraffic == 1 and dtraffic == 1):
        atraffic = 1
    elif (ctraffic == 1 and atraffic == 1 and dtraffic == 1):
        btraffic = 1
    elif (btraffic == 1 and atraffic == 1 and ctraffic == 1):
        dtraffic = 1




while(1):
    loop()