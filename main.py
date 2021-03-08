import simpy
import random

#Algortimos y Estructura de Datos
#Autores: Stefano Aragoni 20261 y Roberto Vallecillos 20441


def simulacion(process, ram, cantMemoria, numInstruc, velocidad, environment, tiempo):

    global currentTime
    global totalTime

    #--------------------New Process
    yield environment.timeout(tiempo)
    
    #Prints amount of RAM needed to complete the process

    print (process + ': requiere ' + str(cantMemoria) + ' de memoria RAM') 

    realTime = environment.now

    #--------------------Ready Process
    yield ram.get(cantMemoria) #retrieves the ram

      
    print (process + ': se le cede :' + str(cantMemoria) + 'de memoria RAM')

    #Varialbe where it shows all of the finished instructions.
    currTerm = 0

    #Loop that resolves the different instructions of each process
    while currTerm < numInstruc:

        with cpu.request() as r:
            yield r

            #checks if the instructions amount is not negative
            if (numInstruc - currTerm)>= velocidad:
                realTime = int(velocidad)
            else:
                realTime = int(numInstruc - currTerm)
            #Prints the amount of instructions completed
            print (process + ': El CPU ejecutara ' + str(realTime) + ' instrucciones')
            yield environment.timeout(realTime/velocidad)

            currTerm = currTerm + realTime
            print (process + ': El CPU ha ejecutado ' + str(currTerm) + ' de ' + str(numInstruc) + ' instrucciones ')

        #Random that determines if simulation is ready or will wait
        choice = random.randint(1,2)

        if (choice == 1) and (currTerm<numInstruc):
            #--------------------Process is waiting
            with wait.request() as r1:
                yield r1
                yield environment.timeout(1)
                print (process + ': Se ha echo operaciones de entrada y salida')

    #--------------------Process Terminated
    yield ram.put(cantMemoria)
    print (process + ': Se regresa del CPU ' + str(cantMemoria)  + ' de RAM ')
    totalTime += (environment.now - realTime)
    currentTime.append(environment.now - realTime)

################################################

#Initial variables with values      
amnRam = 200
totalTime = 0.0
currentTime = []
numProces = 25
velocidad = 3.0    

#Creates simpy environment and other things    
environment = simpy.Environment()
ram = simpy.Container(environment, capacity=amnRam, init=amnRam)
cpu = simpy.Resource(environment, capacity = 1)
wait = simpy.Resource(environment, capacity = 2)

numInt = 1
random.seed()

#sends instructions to function
for i in range(numProces):
    tiempo = random.expovariate(1.0 /numInt)
    numInstruc = random.randint(1,10)
    cantMemoria = random.randint(1,10) 
    environment.process(simulacion('Proceso #'+str(i+1), ram, cantMemoria, numInstruc, velocidad, environment, tiempo))
#Process is finished

environment.run(10000)

suma = 0
promedio = 0

#Calculates the amount of time it takes for each process to occur 
promedio = (totalTime/numProces)
print ('\n\nEl promedio de los procesos es: ' + str(promedio) + ' segundos')

#Standard deviation
for cont in currentTime:
    suma = suma +((cont-promedio)**2)
desv = (suma/(numProces))**5
print('\nLa desviacion estandar del tiempo promedio de los procesos es: ' + str(desv) + ' segundos')
