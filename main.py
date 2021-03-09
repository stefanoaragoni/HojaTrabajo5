import simpy
import random
import statistics

#Algortimos y Estructura de Datos
#Autores: Stefano Aragoni 20261 y Roberto Vallecillos 20441

################################################

##Start of the program

amnRam = 100 #Total amount of ram available
numProces = 25 #Amount of processes to be done
speed = 3.0 #speed
amountInst = 1 #Intervalo

avg = 0
totalTime = 0.0 #Total time for program execution
currentTime = [] #Time that each process takes, for standard deviation


################################################

#Functions

def terminated(process, ram, cantMemoria, numInstruc, speed, environment, time, realTime):
    global totalTime
    #--------------------Process Terminated
    yield ram.put(cantMemoria)
    print (process + ':\t Se regresa del CPU ' + str(cantMemoria)  + ' de RAM ')


    timeTermination = environment.now - realTime

    totalTime += (timeTermination)
    currentTime.append(timeTermination)



def running(process, ram, cantMemoria, numInstruc, speed, environment, time, waitProcess, realTime):

    #--------------------Running Process

    currentTime

    #Varialbe where it shows all of the finished instructions.
    currTerm = 0

    #Loop that resolves the different instructions of each process
    while currTerm < numInstruc:

        toDo = numInstruc - currTerm

        with cpu.request() as cpuRequest:
            yield cpuRequest

            #checks if the iremaining nstructions amount is bigger than the amount of speed
            if (toDo)>= speed:
                realTime = int(speed)
            else:
                realTime = int(toDo)

            #Prints the amount of instructions completed
            print (process + ':\t El CPU ejecutara ' + str(realTime) + ' instrucciones')
            yield environment.timeout(realTime/speed)

            #Updates the amount of instructions completed with this cycle
            currTerm = currTerm + realTime
            print (process + ':\t El CPU ha ejecutado ' + str(currTerm) + ' de ' + str(numInstruc) + ' instrucciones ')
        
        #--------------------Process is waiting

        #Random that determines if simulation is ready or will wait
        choice = random.randint(1,2)

        if (choice == 1) and (currTerm < numInstruc):
            with waitProcess.request() as waiting:
                yield waiting
                yield environment.timeout(1)
                print (process + ':\t El proceso está esperando y ejecutando operaciones I/O')

    environment.process(terminated(process, ram, cantMemoria, numInstruc, speed, environment, time, realTime))
            


def ready(process, ram, cantMemoria, numInstruc, speed, environment, time, waitProcess):

    #--------------------Ready Process

    realTime = environment.now

    yield ram.get(cantMemoria) #retrieves the ram if available. IF NOT, IT SENDS THE REQUEST TO QUEUE AND CONTINUES WITH THE NEXT REQUEST
    print (process + ':\t se le cede ' + str(cantMemoria) + ' de memoria RAM')

    environment.process(running(process, ram, cantMemoria, numInstruc, speed, environment, time, waitProcess, realTime))

    

def new(process, ram, cantMemoria, numInstruc, speed, environment, time, waitProcess):
    
    #--------------------New Process

    #Simulates incoming time for new process
    yield environment.timeout(time)

    #Prints amount of RAM needed to complete the process
    print (process + ':\t requiere ' + str(cantMemoria) + ' de memoria RAM') 

    environment.process(ready(process, ram, cantMemoria, numInstruc, speed, environment, time, waitProcess))
    

################################################

#Creates simpy environment and other things    
environment = simpy.Environment() #Creates environment

cpu = simpy.Resource(environment, capacity = 1)
ram = simpy.Container(environment, capacity=amnRam, init=amnRam) #Creates ram and CPU container

waitProcess = simpy.Resource(environment, capacity = 1)


#creates random seed
random.seed(10000)


################################################

#Creates the different processes, sends them to the simulation
for j in range(numProces):
    time = random.expovariate(1.0 /amountInst)
    numInstruc = random.randint(1,10)
    cantMemoria = random.randint(1,10) 

    #Sends process to simulation
    environment.process(new('Proceso #'+str(j+1), ram, cantMemoria, numInstruc, speed, environment, time, waitProcess))

environment.run()

#Environment ends

################################################

#Mean
avg = (totalTime/numProces)
print ('\n\nEl promedio de los procesos es: ' + str(avg) + ' unidades de tiempo de Simpy')

#Standard deviation

print('\nLa desviacion estandar del time promedio de los procesos es: ' + str((statistics.stdev(currentTime))) + ' unidades de tiempo de Simpy')
