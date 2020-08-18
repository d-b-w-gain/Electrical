#!/usr/bin/env python
# coding: utf-8

# In[18]:

# Dan - What is this?

class AS3K8:
    """ A simple Class to make using values from the AS3K8 easy """
    def __init__(self):
        self.loadTable10()
        self.loadTable16()
        self.loadTable17()
        self.loadTable27()
        self.loadTable52()
        self.loadTable53()
    def loadTable53(self):
        file_path = 'AS3K8-Table53.csv'#xlsx'
        self.table53 = {}
        with open(file_path) as f:
            headers = [header.strip() for header in next(f).split(",")[1:]]
            for line in f:
                values = [value.strip() for value in line.split(",")]
                self.table53[values[0]] = dict(zip(headers, values[1:]))
    def loadTable52(self):
        file_path = 'AS3K8-Table52.csv'#xlsx'
        self.table52 = {}
        with open(file_path) as f:
            headers = [header.strip() for header in next(f).split(",")[1:]]
            for line in f:
                values = [value.strip() for value in line.split(",")]
                self.table52[values[0]] = dict(zip(headers, values[1:]))
    def loadTable17(self):
        self.table17 = {150:{"x":[-40,15,20,25 ,30,35,40,45,50,55,60,65,70,75,80,85,90,100,110,120,130,140],
                             "y":[1.11,1.11,1.09,1.07,1.04,1.02,1.0,0.98,0.95,0.93,0.90,0.88,0.85,0.83,0.80,0.77,0.74,0.69,0.60,0.52,0.43,0.30]}
                       }
    def loadTable17(self):
        self.table17 = {'C03':{'Cable Type':"Cables and Flexible Cords",
                 'Insulation Type':"R-S-150, Type 10 Fibrous or 150C rated Fluropolymer",
                 'Max Conductor Temp C':150,
                 'Other information':"Two single-core or one two-core, Enclosed in air",
                 0.5  : 15,
                0.75 : 20,
                1.0  : 23,
                1.5  : 28,
                2.5  : 38,
                4.0  : 50,
                6.0  : 67,
                10.0 : 90,
                16.0 : 119,
                25.0 : 160,
                35.0 : 194}};
    def loadTable16(self):
        self.table16 = {'Cable Type':"Flexable cords",
                 'Insulation Type':"Thermoplastic OR Cross-Linked",
                 'Max Conductor Temp C':60,
                 'Other information':"Reference Ambient 25C in air",
                 0.5     : 0.5,
                 0.75     : 7.5,
                 1.0     : 10,
                 1.5     : 16,
                 2.5    : 20,
                 4.0   : 25,
                 6.0   : 0,
                 10.0   : 0,
                 16.0   : 0,
                 25.0   : 0,
                 35.0   : 0};
    def loadTable10(self):
        self.table10 = {'C03':{'Cable Type':"Two-core Sheathed",
                     'Insulation Type':"Thermoplastic",
                     'Max Conductor Temp C':75,
                     'Other information':"Unenclosed, Spaced, Cu, Flexable",
                     0.5 :    0,
                     0.75:    0,
                      1.0     : 16,
                     1.5     : 20,
                     2.5    : 26,
                     4.0   : 35,
                     6.0   : 45,
                     10.0   : 63,
                     16.0   : 83,
                     25.0   : 110,
                     35.0   : 137},
                    'C12':{'Cable Type':"Two-core Sheathed",
                     'Insulation Type':"Thermoplastic",
                     'Max Conductor Temp C':75,
                     'Other information':"Enclosed, in Air, Cu, Flexable",
                     0.5 :    0,
                     0.75:    0,
                     1.0     : 13,
                     1.5     : 17,
                     2.5    : 23,
                     4.0   : 29,
                     6.0   : 38,
                     10.0   : 51,
                     16.0   : 68,
                     25.0   : 87,
                     35.0   : 109}}
    def getTable10(self):
        return self.table10['C03']
    def getTable16(self):
        return self.table16
    def getTable17(self):
        return self.table17['C03']
    def getTable52(self):
        return self.table52
    def getTable53(self):
        return self.table53
    def getTable(self,tableNumber):
        if tableNumber==10:
            return self.getTable10()
        elif tableNumber==16:
            return self.getTable16()
        elif tableNumber==17:
            return self.getTable17()
        elif tableNumber==52:
            return self.getTable52()
        elif tableNumber==53:
            return self.getTable53()
        else:
            raise ValueError('Table '+str(tableNumber)+' has not been installed.')


# In[19]:


import convertWire as convert
from scipy import interpolate
class Cable:
    def __init__(self, application):
        self.loadAS3K8()
        self.setApplication(application)
    def loadAS3K8(self):
        self.as3K8 = AS3K8()
    def setApplication(self, application):
        if application=='flexable lead':
            self.application = application
            self.table = 16 # set up with Table 16 when using a flexable lead
            self.unit = ''
        elif application=='fixed':
            self.application = application
            self.unit = ''
        else:
            raise ValueError('Cable application needs to be defined as either flexable lead or fixed')
    def setCSA(self,CSA):
        self.unit = 'CSA'
        self.value = CSA
    def setAWG(self,AWG):
        self.unit = 'AWG'
        self.value = AWG
    def setTable(self,tableNumber):
        if self.application=='flexable lead':
            raise ValueError('table can not be changed for a flexable lead')
        elif self.application=='fixed':
            self.table = tableNumber
    def setK(self):
        table52 = self.as3K8.getTable(52)#openTable52()
        self.setMaxConductorTemp()
        self.K = table52[str(self.getMaxConductorTemp())][str(self.getMaxCableTemp())]
    def setInsulation(self,insulation):
        self.insulation = insulation
        self.setMaxCableTemp()
    def setMaxConductorTemp(self):
        self.maxConductorTemp = self.as3K8.getTable(self.table)['Max Conductor Temp C']
    def setMaxCableTemp(self):
        table53 = self.as3K8.getTable(53)#openTable53()
        if self.getCSA()<=300:
            self.maxCableTemp = table53[self.insulation]['<=300']
        else:
            self.maxCableTemp = table53[self.insulation]['>300']
    def getCSA(self):
        if self.unit=='CSA':
            return float(self.value)
        elif self.unit=='AWG':
            return float(convert.AWG2CSA(self.value))
        else:
            raise ValueError('No value set for CSA or AWG')
    def getAWG(self):
        if self.unit=='AWG':
            return float(self.value)
        elif self.unit=='CSA':
            return float(convert.CSA2AWG(self.value))
        else:
            raise ValueError('No value set for CSA or AWG')
    def getK(self):
        return self.K
    def getMaxCableTemp(self):
        return self.maxCableTemp
    def getMaxConductorTemp(self):
        return self.maxConductorTemp
    def getAmpacity(self):
        i=0
        self.x=[]
        self.y=[]
        for value in self.as3K8.getTable(10):
            if isinstance(value,str)!=1:
                self.x.append(value)
                self.y.append(self.as3K8.getTable(10)[value])
        f = interpolate.interp1d(self.x, self.y)
        ampacity = f(self.getCSA())
        return ampacity #self.as3K8.getTable(self.table)[self.getCSA()]
    def plotFaultCurve(self):
        import matplotlib.pyplot as plt
        import numpy as np
        plotTime = np.arange(0.001,1000,0.001)
        plotCurrent = (float(self.K)**2*self.getCSA()**2/plotTime)**0.5
        #plotArray = {self.insulation:{self.getCSA():{'time':plotTime,'current':plotCurrent}}}
        #print(plotTime)
        plt.yscale('log')
        plt.xlabel('Current')
        plt.ylabel('Time')
        plt.title( str(self.getCSA())+' mm2 fault curve')
        plt.plot(plotTime,plotCurrent)


# In[22]:


##TESTING
# cable1 = Cable('flexable lead')
# cable1.setCSA(25)
# print(cable1.application)
# print(cable1.unit)
# print(cable1.value)
# CSA1 = cable1.getCSA()
# print(CSA1)
# AWG1 = cable1.getAWG()
# print(AWG1)
# cable2 = Cable('flexable lead')
# cable2.setAWG(16)
# print(cable2.application)
# print(cable2.unit)
# print(cable2.value)
# CSA2 = cable2.getCSA()
# print(CSA2)
# AWG2 = cable2.getAWG()
# print(AWG2)
# cable3 = Cable('fixed')
# cable3.setAWG(5)
# cable3.setInsulation('X-90')
# cable3.setTable(17)
# cable3.setK()
# print('K = '+str(cable3.getK()))
# print('CSA = '+str(cable3.getCSA()))
# print('AWG = '+str(cable3.getAWG()))
# print('MaxCableTemp = '+str(cable3.getMaxCableTemp())+' C')
# print('Maximum allowable current = '+str(cable3.getAmpacity())+' Amps')
# cable3.plotFaultCurve()


# In[24]:


# cable3.as3K8.table17['C03']


# In[ ]:




