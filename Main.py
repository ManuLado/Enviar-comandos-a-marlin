#!/usr/bin/env python
# coding: utf-8


import serial
import time
from datetime import date
import datetime
import os
import sys
import RPi.GPIO as gpio
#import thread as thread

#///////////////////////////////// puerto 12!!!
gpio.setmode(gpio.BOARD)
gpio.setup(12,gpio.OUT)
gpio.setwarnings(False)
#def ledblinker(port,frec):
#    gpio.setmode(gpio.BOARD)
#    gpio.setup(port,gpio.OUT)
#    gpio.output(port,True)
#    time.sleep(frec)
#    gpio.output(port,False)
#    time.sleep(frec)

#/////////////////////////////////
if not os.path.exists('logdir.txt'):
    with open('logdir.txt','w') as f:
        f.write('0')
with open('logdir.txt','r') as f:
    st = int(f.read())
    st+=1 
with open('logdir.txt','w') as f:
    f.write(str(st))
#////////////////////////////////
#dirname="run_"+str(datetime.datetime.now())
dirname="date_"+str(date.today())+"_run_"+str(st)
print("creating folder "+ dirname +" ...")
os.system("mkdir "+dirname)
samplename=input("Nombre de muestra:>>>")
#................................................................................................
arduino = serial.Serial("/dev/ttyACM0",250000)   #NOMBRE DEL PUERTO Y BOUDRATE
time.sleep(2)
#arduino.write(b"M1005\n")               #set units in mm
#arduino.flush()
arduino.write(b"G21\n")                 #set units in mm
arduino.flush()
arduino.write(b"G91\n")                 #G90 absolute posit; G91 relative position
arduino.flush()
arduino.write(b"M121\n")                #M121 disable endstops; M120 to enable
arduino.flush()
arduino.write(b"M92 X70.63 Y50\n")      #steps per mm
arduino.flush()
arduino.write(b"M203 X50 Y300 \n")      #set max feedrate
arduino.flush()
arduino.write(b"G92 X0 Y0\n")          #set current position as 00 (calibrar en el origen del plano)
arduino.flush()
#................................................................................................
#definicion de variables e input
#gcode=str(input("<<<<ingrese codigo g>>>>:"))
#arduino.write(bytes(gcode,'utf-8'))

inp=input("<<<<CONTINUAR. presione cualquier tecla("'exit'" para salir)>>>>>")
if inp=="exit" or inp=="EXIT":
    sys.exit()
    

xrange=float(input("<<<<ingrese ancho x de muestreo [mm]>>>>"))#200
yrange=float(input("<<<<ingrese largo y de muestreo[mm]>>>>"))#50
pasos=float(input("<<<<ingrese pasos de muestreo (numero de imagenes)>>>>:"))#10


noitt=1 #numberofimagestotake

xstep=int(xrange/pasos)
ystep=int(yrange/pasos)
movx='G0 X'+str(xstep) + " \\" +'n'
movy="G0 Y"+str(ystep) + " \\" +'n'
rnx='G0 X'+str(int(xrange)) + " \\" +'n'
rny='G0 X0 Y'+str(int(yrange)) + " \\" +'n'
#print(movx)

arduino.flush()
#arduino.write(bytes(movy,'utf-8'))
arduino.write(b"G0 X200 Y-50\n")
arduino.flush()
a=arduino.readline()
print("arduino dice:",a)


#................................................................................................
#bucles while, zigzag
i=0
arduino.write(b"G0 X-300 Y50\n")

time.sleep(10)
arduino.flush()
while i<xstep:
    j=0
    i+=1
    while j<ystep:
        j+=1
        #arduino.write(bytes(movx,'utf-8'))
        arduino.write(b"G0 X20 \n")
        a=arduino.readline()
        print("arduino dice:",a)
        arduino.flush()
        arduino.write(b" M114 \n")
        arduino.flush()
        arduino.write(b" M400 \n")
        arduino.flush()
#arduino.write(b" M280 \n")    #Set or get the position of a servo.
#arduino.flush()
##


#ser_bytes = str(arduino.readline())
        string1="b'echo:busy: processing" + "\\" + "n'"
        string2="b'ok" + "\\" + "n'"
        arduino.flushInput()
        s = string1 #string estado de arduino

        while True:
            s=str(arduino.readline())
            #print("s",s)
            #ser_bytes =
            arduino.flushInput()
            arduino.flushOutput()
            time.sleep(5)
            if s==string2:
                gpio.output(12,True)
                print('\x1b[6;30;43m'+"!!!WARNING: X-RAYs ON!!!"+'\x1b[0m')
                print('\x1b[3;33;47m'+"Blindar y mantener distancia del dispositivo"+'\x1b[0m')
                print("saving image...")
                filename=dirname+ "/x" +str(j) +"y" +str(i)+".fits"
                
                #ledblinker(12,0.5)

                
                os.system("sudo python take_images.py "+dirname+ "/x" +str(j) +"y" +str(i)+" "+str(noitt))
                
                time.sleep(5)
                gpio.output(12,False)
                print('\x1b[6;37;42m'+"X-RAYs OFF"+'\x1b[0m')
                while True:
                    print("checking file existance...",filename)
                    if os.path.isfile(filename)==True:
                        print("checked!")
                        
                        break    
                break
        print("--------Numero de imagenes tomadas hasta ahora:", j*i)
    arduino.flush()    
    #arduino.write(b"G28 X \n") #regresa a x=0
    arduino.write(b"G0 X-200 \n")
    #arduino.write(bytes(movx,'utf-8'))
    arduino.flush()
    time.sleep(10)
    #arduino.write(bytes(movy,'utf-8'))
    arduino.write(b"G0 Y-5 \n")

print("Escaneo completado")
##
#output=arduino.read(5)
#print(str(output,'utf8'))


time.sleep(10)
#arduino.write(b"G28 X Y \n")             #auto home
#time.sleep(10)
home='G0 X-'+str(xstep) + " Y-" +str(ystep) + " \\" +'n'
arduino.write(bytes(home,'utf-8'))             #
#arduino.write(b"G0 X200 Y20 \n")

time.sleep(15)
arduino.close()
arduino.open()
arduino.close()


# In[17]:


arduino.close()


# In[1]:


#string="b'ok" + "\\" + "n'"
#print(ser_bytes)
#print(string)


c=len(os.listdir(dirname))
print("===============================================================")
print("converting .fits to .jpeg ...........")
print("===============================================================")
import fits2jpeg
fits2jpeg.directory_name(dirname)


# ----------------------------------------------------write logfile

tkimgs=open('take_images.py')


content = tkimgs.readlines()

ct86=content[86]
ct86=ct86.replace(", # Shutter Width 0x0419 (max: 0x3FFF)"," pp")
ct86=ct86.replace("0x09"," **")
ct86=ct86.lstrip("[ **, ")
ct86=ct86.replace("] pp","")

ct97=content[97]
ct97=ct97.replace(", # Global Gain 0x0008 (max: 0x0067)"," pp")
ct97=ct97.replace("0x35"," **")
ct97=ct97.lstrip("[ **, ")
ct97=ct97.replace("] pp","")

itt=open('integrationtime.txt')
content2 = itt.readlines()

with open(str(dirname)+'/log.txt','w') as f:
    f.write('Directorio: '+str(dirname)+"\n")
    f.write('Fecha: '+str(date.today())+"\n")
    f.write('Nombre de muestra: '+str(samplename)+"\n")
    f.write('Numero de imagenes tomadas: '+str(c)+"\n")
    f.write('----------Parametros de camara------------- '+"\n")
    f.write('Distancia focal: 2 cm'+"\n")
    
    f.write('Ancho del sensor: '+str(content[43])+"\n")
    f.write('Alto del sensor: '+str(content[44])+"\n")
    f.write('Ancho del obturador: '+str(int(ct86, 16))+"\n")
    f.write('Ganancia global: '+str(int(ct97, 16))+"\n")
    f.write('Tiempo de integracion [ms]: '+str(content2[0])+"\n")
    
    f.write('----------Parametros de muestreo------------- '+"\n")
    f.write('ancho x de muestreo [mm]: '+str(xrange)+"\n")
    f.write('alto y de muestreo [mm]: '+str(yrange)+"\n")
    f.write('pasos: '+str(pasos)+"\n")
    f.write('cantidad de imagenes promediadas por posicion: '+str(noitt)+"\n")
print("log file saved as log.txt")    