#Conteo de fotones
import numpy as np
import matplotlib.pyplot as plt
import os

def poissoniana(media,x):
    result = []
    for i in range(len(x)):
        result.append((np.exp(-media) * (media**int(x[i])))/np.math.factorial(x[i]))
    return  result

def bose_einstein(media,x):
    result = []
    for i in range(len(x)):
        result.append((media**int(x[i]))/((1+media)**(int(x[i])+1)))
    return  result

def progreso(paso,total):
    porcentaje = paso/total
    barras = int(porcentaje*20)
    if paso < total:
        total = '0% ['
        for i in range(barras-1):
            total += '='
        total += '>'
        for i in range(20-barras):
            total += '-'
        total += '] %d' %int(porcentaje*100)
        total += '%'
        print(total, end = '\r')
    elif paso == total:
        total = '0% [====================] 100% Completado'
        print(total)

class datos_class:
    def __init__(self):
        self.tiempo = np.array([])
        self.voltaje = np.array([])
    def plot(self):
        plt.plot(self.tiempo,self.voltaje)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Voltaje (V)')
        plt.show()
    def plot_volt(self):
        plt.plot(self.voltaje)
        plt.xlabel('Número de medición')
        plt.ylabel('Voltaje (V)')
        plt.show() 
    def agregar_tiempo(self,a):
        self.tiempo = np.append(self.tiempo,a)
    def agregar_voltaje(self,a):
        self.voltaje = np.append(self.voltaje,a)             


class Data:
    'Esta es la clase de los datos'
    def __init__(self):
        self.sl = datos_class()
        self.l  = datos_class()
        self.filtrado = datos_class()
        self.conteomedio = []
        self.conteo_por_pantalla = []
        self.threshold = 'none'
        self.ventana_tiempo = 'none'
    def hist(self,bines):
        plt.hist(self.l.voltaje, bins = bines, density = False, label = 'Con Laser', align = 'left', lw=1, ec="black")
        plt.hist(self.sl.voltaje, bins = bines, density = False, label = 'Sin Laser', align = 'left', lw=1, ec="black")
        plt.xlabel('Voltaje (V)')
        plt.ylabel('Número de veces detectado')
        plt.legend()
        plt.show()
    def hist_l(self,bines):
        plt.hist(self.l.voltaje, bins = bines, density = False, label = 'Con Laser', align = 'left', lw=1, ec="black")
        plt.xlabel('Voltaje (V)')
        plt.ylabel('Número de veces detectado')
        plt.legend()
        plt.show()
    def hist_sl(self,bines):
        plt.hist(self.sl.voltaje, bins = bines, density = False, label = 'Sin Laser', align = 'left', lw=1, ec="black")
        plt.xlabel('Voltaje (V)')
        plt.ylabel('Número de veces detectado')
        plt.legend()
        plt.show()
    def test_thres(self,threshold):
        a = [-element for element in self.l.voltaje if element <= threshold] 
        fp = float(len([element for element in self.sl.voltaje if element <= threshold ])) / len(self.sl.voltaje) * 100
        plt.hist(a, bins = 'auto', align = 'left', lw=1, ec="black", density = False, label = 'Distribución con threshold = %f' %threshold)
        plt.title('Porción de distribución ruido detectada: %f' %fp + '%' )
        plt.xlabel('Voltaje (V)')
        plt.ylabel('Número de veces detectado')
        plt.legend()
        plt.show()
    def set_thres(self,threshold):
        self.filtrado.voltaje = [-element for element in self.l.voltaje if element <= threshold] 
        self.filtrado.tiempo = [self.l.tiempo[i] for i in range(len(self.l.voltaje)) if self.l.voltaje[i] <= threshold]
        self.threshold = threshold
        i = 0
        multiple = False 
        while multiple == False and i<(len(self.l.tiempo)-1):
            if self.l.tiempo[i]>self.l.tiempo[i+1]:
                multiple = True
            i += 1
        if multiple == True:
            pos = 0
            for i in range(len(self.l.tiempo)):
                if self.l.tiempo[(i+1)%len(self.l.tiempo)]<self.l.tiempo[i]:
                    fotones = [element for element in self.l.voltaje[pos:i] if element <= threshold]
                    pos = i
                    self.conteo_por_pantalla = np.append(self.conteo_por_pantalla,(len(fotones)))
            self.conteomedio = np.mean(self.conteo_por_pantalla)
        if multiple == False:
            if self.ventana_tiempo == 'none':
                print('No se ha seteado una ventana temporal. Debe configurarlo según .ventana_tiempo = Tiempo')
            else:
                self.conteo_por_pantalla = []
                pos = int(round(self.ventana_tiempo / (self.l.tiempo[1]-self.l.tiempo[0])))
                print('La ventana temporal real es: %f' %(pos*(self.l.tiempo[1]-self.l.tiempo[0])))
                for i in range(len(self.l.tiempo)-pos):
                    progreso(i,len(self.l.tiempo)-pos-1)
                    fotones = [element for element in self.l.voltaje[i:(i+pos)] if element <= threshold]
                    self.conteo_por_pantalla = np.append(self.conteo_por_pantalla,(len(fotones)))
                self.conteomedio = np.mean(self.conteo_por_pantalla)
    def hist_conteo(self,bines):
            plt.hist(self.conteo_por_pantalla, bins = bines, density = True, lw=1, ec="black", label = 'Probabilidad de conteo', align = 'left')
            plt.xlabel('Cantidad de fotones recibidos')
            plt.ylabel('Número de observaciones')
            plt.legend()
            plt.show()
    def poisson(self,bines):
        plt.hist(self.conteo_por_pantalla, bins = bines, lw=1, ec="black", label = 'Probabilidad de conteo', density = True, align = 'left')
        x = np.linspace(0,int(max(self.conteo_por_pantalla)), int(max(self.conteo_por_pantalla))+1)
        plt.plot(x, poissoniana(self.conteomedio, x), '-o', label = 'Poissoniana con media %f' %self.conteomedio)
        plt.xlabel('Cantidad de fotones recibidos por unidad de tiempo')
        plt.ylabel('Probabilidad')
        plt.legend()
        plt.show()
    def bose(self,bines):
        plt.hist(self.conteo_por_pantalla, bins = bines, lw=1, ec="black", label = 'Probabilidad de conteo', density = True, align = 'left')
        x = np.linspace(0,int(max(self.conteo_por_pantalla)), int(max(self.conteo_por_pantalla))+1)
        plt.plot(x, bose_einstein(self.conteomedio, x), '-o', label = 'Bose-Einstein con media %f' %self.conteomedio)
        plt.xlabel('Cantidad de fotones recibidos por unidad de tiempo')
        plt.ylabel('Probabilidad')
        plt.legend()
        plt.show()
    def tiempo_correlacion(self,pos):
        self.fun_corr = np.correlate(self.l.voltaje[0:pos],self.l.voltaje[0:pos],'same')
        plt.plot(self.l.tiempo[0:pos], self.fun_corr[np.shape(self.fun_corr)[0]/2:]/np.linalg.norm(self.l.voltaje[0:pos]))
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Función de correlación normalizada')
        plt.show()

class Medicion():
    'Esta clase tiene una  caracteristica que es la de datos, dentro de esta se puede poner \\  .hist para ver el histograma \\ .sl o .l para laser o sin laser y dentro de esos ver el .voltaje o .tiempo'
    def __init__(self):
        self.datos = Data()
        self.archivos = []
    def importar(self,path_sin_laser,path_con_laser):
        print('Buscando carpetas con esos nombres...')
        try:
            file_list_sl = [f for f in os.listdir(path_sin_laser) if not f.startswith('.')]
            file_list_l  = [f for f in os.listdir(path_con_laser) if not f.startswith('.')]
        except:
            print('Oops! No se encontraron carpetas con esos nombres!')
        else:
            print('Cargando sin laser')
            for i in range(len(file_list_sl)):
                path_sl = path_sin_laser + '/' +  file_list_sl[i]
                raw = np.genfromtxt(path_sl,delimiter =  ',')
                self.datos.sl.agregar_voltaje(raw[:,1])
                self.datos.sl.agregar_tiempo(raw[:,0])
                progreso(i,len(file_list_sl)-1)
            print('Cargando con laser')
            for i in range(len(file_list_l)):
                path_l = path_con_laser + '/' + file_list_l[i]
                raw = np.genfromtxt(path_l,delimiter =  ',')
                self.datos.l.agregar_voltaje(raw[:,1])
                self.datos.l.agregar_tiempo(raw[:,0])
                progreso(i,len(file_list_l)-1)
            self.archivos.append([path_sin_laser, path_con_laser])
        print('Buscando archivos con esos nombres...')
        try:
            print('Cargando con laser')
            raw = np.genfromtxt(path_con_laser,delimiter =  ',')
        except:
            print('Oops! No se pudo encontrar un archivo csv con el nombre!: '+path_con_laser)
            print('No se pudieron cargar los datos con laser.')
        else:  
            self.datos.l.agregar_voltaje(raw[:,1])
            self.datos.l.agregar_tiempo(raw[:,0])
            self.archivos.append([path_con_laser])
        try:
            print('Cargando sin laser')
            raw = np.genfromtxt(path_sin_laser,delimiter =  ',')
        except:
            print('Oops! No se pudo encontrar un archivo csv con el nombre!: '+path_sin_laser)
            print('No se pudieron cargar los datos sin laser.')
        else:    
            self.datos.sl.agregar_voltaje(raw[:,1])
            self.datos.sl.agregar_tiempo(raw[:,0])
            self.archivos.append([path_sin_laser])
    def importar_l(self,path_con_laser):
        print('Buscando carpeta con ese nombre...')
        try:
            file_list_l  = [f for f in os.listdir(path_con_laser) if not f.startswith('.')]
        except:
            print('Oops! No se encontro una carpeta con ese nombre!')
        else:
            print('Cargando con laser')
            for i in range(len(file_list_l)):
                path_l = path_con_laser + '/' + file_list_l[i]
                raw = np.genfromtxt(path_l,delimiter =  ',')
                self.datos.l.agregar_voltaje(raw[:,1])
                self.datos.l.agregar_tiempo(raw[:,0])
                progreso(i,len(file_list_l)-1)
            self.archivos.append([path_con_laser])
        print('Buscando archivo con ese nombre...')
        try:
            print('Cargando con laser')
            raw = np.genfromtxt(path_con_laser,delimiter =  ',')
        except:
            print('Oops! No se pudo encontrar un archivo csv con el nombre!: '+path_con_laser)
            print('No se pudieron cargar los datos con laser.')
        else:  
            self.datos.l.agregar_voltaje(raw[:,1])
            self.datos.l.agregar_tiempo(raw[:,0])
            self.archivos.append([path_con_laser])
    def importar_sl(self,path_sin_laser):
        print('Buscando carpeta con ese nombre...')
        try:
            file_list_sl = [f for f in os.listdir(path_sin_laser) if not f.startswith('.')]
        except:
            print('Oops! No se encontraron carpetas con esos nombres!')
        else:
            print('Cargando sin laser')
            for i in range(len(file_list_sl)):
                path_sl = path_sin_laser + '/' +  file_list_sl[i]
                raw = np.genfromtxt(path_sl,delimiter =  ',')
                self.datos.sl.agregar_voltaje(raw[:,1])
                self.datos.sl.agregar_tiempo(raw[:,0])
                progreso(i,len(file_list_sl)-1)
            self.archivos.append([path_sin_laser])
        print('Buscando archivo con ese nombre...')
        try:
            print('Cargando con laser')
            raw = np.genfromtxt(path_sin_laser,delimiter =  ',')
        except:
            print('Oops! No se pudo encontrar un archivo csv con el nombre!: '+path_sin_laser)
            print('No se pudieron cargar los datos sin laser.')
        else:  
            self.datos.sl.agregar_voltaje(raw[:,1])
            self.datos.sl.agregar_tiempo(raw[:,0])
            self.archivos.append([path_sin_laser])
            
#Ejemplo de como importar datos:
#a = Medicion()
#a.importar('medicion_sin_laser_100micros','medicion_laser_44_100micros')a

#Hola hola hola

