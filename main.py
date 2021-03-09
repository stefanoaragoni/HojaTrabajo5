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

promedio = 0
totalTime = 0.0 #Total time for program execution
currentTime = [] #Time that each process takes, for standard deviation

def simulacion(process, ram, cantMemoria, numInstruc, speed, environment, time):

    global currentTime
    global totalTime

    #--------------------New Process
    yield environment.timeout(time)
    
    #Prints amount of RAM needed to complete the process

    print (process + ':\t requiere ' + str(cantMemoria) + ' de memoria RAM') 

    realTime = environment.now

    #--------------------Ready Process
    yield ram.get(cantMemoria) #retrieves the ram

      
    print (process + ':\t se le cede ' + str(cantMemoria) + ' de memoria RAM')

    #--------------------Running Process

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

        if (choice == 1) and (currTerm<numInstruc):
            with wait.request() as r1:
                yield r1
                yield environment.timeout(1)
                print (process + ':\t El proceso está esperando y ejecutando operaciones I/O')

    #--------------------Process Terminated
    yield ram.put(cantMemoria)
    print (process + ':\t Se regresa del CPU ' + str(cantMemoria)  + ' de RAM ')
    totalTime += (environment.now - realTime)
    currentTime.append(environment.now - realTime)

################################################

#Creates simpy environment and other things    
environment = simpy.Environment() #Creates environment
ram = simpy.Container(environment, capacity=amnRam, init=amnRam) #Creates ram and CPU container
cpu = simpy.Resource(environment, capacity = 1)
wait = simpy.Resource(environment, capacity = 2) #creates resource for waiting process

#sends instructions to function
random.seed(10000)

#Creates the different processes, sends them to the simulation
for j in range(numProces):
    time = random.expovariate(1.0 /amountInst)
    numInstruc = random.randint(1,10)
    cantMemoria = random.randint(1,10) 

    #Sends process to simulation
    environment.process(simulacion('Proceso #'+str(j+1), ram, cantMemoria, numInstruc, speed, environment, time))
#Process is finished

environment.run()

################################################

#Mean
promedio = (totalTime/numProces)
print ('\n\nEl promedio de los procesos es: ' + str(promedio) + ' segundos')

#Standard deviation

print('\nLa desviacion estandar del time promedio de los procesos es: ' + str((statistics.stdev(currentTime))) + ' segundos')
