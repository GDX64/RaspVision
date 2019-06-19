import RPi.GPIO as gpio
import time


# Disable warnings
gpio.setwarnings(False)

#Configuring GPIO
gpio.setmode(gpio.BCM) # gpio.setmode(gpio.BOARD) 
gpio.setup(17, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(19, gpio.OUT) 


#Configure the pwm objects and initialize its value
pwmE = gpio.PWM(16,1000)
pwmE.start(0)   
pwmD = gpio.PWM(19,1000)
pwmD.start(0)

#Velocidade maxima que o robo pode atingir
vMax = 100 # em m/s

# Inicializa as variaveis de duty cycle
MTA = 0
MTB = 0

gpio.output(17, False)
gpio.output(27, False)
gpio.output(22, False)
gpio.output(23, False)



def motor(vD, vE):
    #Create the dutycycle variables
    try:
        MTA = (vD/vMax)*100
        if abs(MTA) > 70:
            MTA = 70
            
        MTB = (vE/vMax)*100
        if abs(MTB) > 70:
            MTB = 70
            
        MTB=int(abs(MTB))+10
        MTA=int(abs(MTA))+10
        print(MTA, MTB)


        # Envia os valores de PWM para os motores
        pwmE.ChangeDutyCycle(MTA)
        pwmD.ChangeDutyCycle(MTB)    

        # Define os sentidos de giro das rodas
        if vD > 0:
            gpio.output(17, True)
            gpio.output(27, False)
        elif vD <= 0:
            vD = abs(vD)
            gpio.output(17, False)
            gpio.output(27, True)

        if vE > 0:
            gpio.output(22, False)
            gpio.output(23, True)
        elif vE <= 0:
            vE = abs(vE)
            gpio.output(22, True)
            gpio.output(23, False)

    except:
        print("problema no motor")


motor(0,0)
    

