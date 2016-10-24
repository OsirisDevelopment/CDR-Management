import Tkinter, Tkconstants, tkFileDialog 
import Image, ImageTk
import datetime
import time
import ttk
import os


#"01/12/2011"
def dateTimestamp(string):
    return time.mktime(datetime.datetime.strptime(string, "%d/%m/%Y").timetuple())

def timestampDate(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')



clear=lambda:os.system('cls')

imagenAnchuraMaxima=640
imagenAlturaMaxima=480

# abrimos una imagen
img = Image.open('PortadaCUCM.jpg')

# modificamos el tamano de la imagen
#img.thumbnail((imagenAnchuraMaxima,imagenAlturaMaxima), Image.ANTIALIAS)


class TkFileDialogExample(Tkinter.Frame):
 
   def __init__(self, root):
 
     Tkinter.Frame.__init__(self, root)     

    
 
     # options for buttons
     button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
 
     # define buttons
     Tkinter.Button(self, text='Seleccionar archivo', command=self.askopenfile).pack(**button_opt)
     #Tkinter.Button(self, text='askopenfilename', command=self.askopenfilename).pack(**button_opt)
#    Tkinter.Button(self, text='asksaveasfile', command=self.asksaveasfile).pack(**button_opt)
#    Tkinter.Button(self, text='asksaveasfilename', command=self.asksaveasfilename).pack(**button_opt)
#    Tkinter.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)
 
     # define options for opening or saving a file
     self.file_opt = options = {}
     options['defaultextension'] = '.txt'
     options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
     options['initialdir'] = 'C:\\'
     options['initialfile'] = 'myfile.txt'
     options['parent'] = root
     options['title'] = 'Sistema generador de reportes para CDRs'
 
     # This is only available on the Macintosh, and only when Navigation Services are installed.
     #options['message'] = 'message'
 
     # if you use the multiple file version of the module functions this option is set automatically.
     #options['multiple'] = 1
 
     # defining options for opening a directory
     self.dir_opt = options = {}
     options['initialdir'] = 'C:\\'
     options['mustexist'] = False
     options['parent'] = root
     options['title'] = 'Generador de reportes CCAF'
 
   def askopenfile(self):

    """Returns an opened file in read mode."""
    #ejecutar lectura
    filename = tkFileDialog.askopenfilename(**self.file_opt)
    #print filename
    #source=tkFileDialog.askopenfile(mode='r', **self.file_opt)

    #-----------------------    Fecha y hora del sistema      -----------------------
    #MM/DD/AA HH:MM:SS
    hora=time.strftime("%c")
    listahora=hora.replace("/","-").replace(":","-").replace(" ","-").split("-")
    #AAAAMMDDHHMM
    cadenafecha="20"+listahora[2]+listahora[0]+listahora[1]+listahora[3]+listahora[4]
    listanombre=filename.replace(".","/").split("/")
    #12345678765432123456754321CDR
    cadenanombre=listanombre[-2]
    #--------------------------------------------------------------------------------

    #----------Primer parse de archivo para determinar cantidad de llamadas --------------
    archivo=open(filename,"r")
    source=open(filename,"r")

    countfile=0.0
    countlines=0.0
    lastavance=0

    #diasLlamadas={}
    contadorDiario=dict()
    maxday=(1999,01,01)
    minday=(2100,12,31)

    for linea in source:
        if countfile!=0.0:
            lista2= linea.strip().split(",")
            #TIMESTAMP
            origintime=lista2[4]

            #print origintime
            #date del TIMESTAMP
            day=datetime.datetime.fromtimestamp(int(origintime)).strftime('%d-%m-%Y')

            minday2=day+" 08:00:00"
            maxday2=day+" 19:00:00"

            minTimestamp=time.mktime(datetime.datetime.strptime(minday2, '%d-%m-%Y %H:%M:%S').timetuple())
            maxTimestamp=time.mktime(datetime.datetime.strptime(maxday2, '%d-%m-%Y %H:%M:%S').timetuple())

            tupladay=(int(day.split("-")[2]),int(day.split("-")[1]),int(day.split("-")[0]))
            if tupladay>maxday:
                maxday=tupladay
            elif tupladay<minday:
                minday=tupladay
            #diasLlamadas.add(day)
            contadorDiario[day]=0
        #Conteo de lineas para el porcentaje
        countfile+=1.0
    umbral=(minday,maxday)

    source.close() 


    horas=[]
    timestampa=minTimestamp
    #print timestampa
    while timestampa < maxTimestamp+3600:
        horas.append(timestampa)
        timestampa+=3600 
    
    #-------------------------------------------------------------------------------------

    #-----------------   Apertura de archivos a escribir   -------------------
    general=open("ReporteGeneral_From_"+str(minday[2])+"-"+str(minday[1])+"-"+str(minday[0])+"_to_"+str(maxday[2])+"-"+str(maxday[1])+"-"+str(maxday[0])+".csv","w")
    siptrunk_file=open("SipTrunk_From_"+str(minday[2])+"-"+str(minday[1])+"-"+str(minday[0])+"_to_"+str(maxday[2])+"-"+str(maxday[1])+"-"+str(maxday[0])+".csv","w")  
    Auxiliar_file=open("Auxiliar_From_"+str(minday[2])+"-"+str(minday[1])+"-"+str(minday[0])+"_to_"+str(maxday[2])+"-"+str(maxday[1])+"-"+str(maxday[0])+".csv","w")
    #-------------------------------------------------------------------------

    for linea in archivo:
        lista= linea.strip().split(",")
        if countlines>0:
            try:
                #Categorizacion de Columnas
                #------------------Cuando se origina la llamada----------------------
                #TIMESTAMP
                origintime=lista[4]
                #AAAA-MM-DD HH:MM:SS
                dateorigintime=datetime.datetime.fromtimestamp(int(origintime)).strftime('%Y-%m-%d %H:%M:%S')
                #DD-MM-AAAA
                day=datetime.datetime.fromtimestamp(int(origintime)).strftime('%d-%m-%Y')
                #---------------------------------------------------------------------

                #------------------Cuando se contesta la llamada----------------------
                #TIMESTAMP
                connecttime=lista[47]
                #AAAA-MM-DD HH:MM:SS
                dateconnecttime=datetime.datetime.fromtimestamp(int(connecttime)).strftime('%Y-%m-%d %H:%M:%S')
                #---------------------------------------------------------------------

                #------------------Cuando se termina la llamada----------------------
                #TIMESTAMP
                disconnecttime=lista[48]
                #AAAA-MM-DD HH:MM:SS
                datedisconnecttime=datetime.datetime.fromtimestamp(int(disconnecttime)).strftime('%Y-%m-%d %H:%M:%S')
                #---------------------------------------------------------------------

                #--------------------Numeros que se llaman---------------------------
                callingnumber=lista[8]
                callednumber=lista[29]
                #---------------------------------------------------------------------

                #-------------------- Duracion de llamada ---------------------------
                duration=lista[55]
                #---------------------------------------------------------------------

                #--------------------------  Troncales  ------------------------------
                originDeviceName=lista[56]
                destDeviceName=lista[57]
                #---------------------------------------------------------------------

                if duration==0 or duration =="0":
                    pass

                if duration!=0 and duration !="0":
                    general.write(str(dateorigintime)+";"+str(callingnumber)+";"+str(callednumber)+";"+str(dateconnecttime)+";"+str(datedisconnecttime)+";"+str(duration)+";"+str(originDeviceName)+";"+str(destDeviceName)+"\n")
                    
                    if originDeviceName=="CUCM_To_NEC_SIP_Trunk" or originDeviceName=="CUCM_To_NEC_SIP_Trunk_II" or destDeviceName=="CUCM_To_NEC_SIP_Trunk" or destDeviceName=="CUCM_To_NEC_SIP_Trunk_II":  
                        siptrunk_file.write(str(dateorigintime)+";"+str(callingnumber)+";"+str(callednumber)+";"+str(dateconnecttime)+";"+str(datedisconnecttime)+";"+str(duration)+";"+str(originDeviceName)+";"+str(destDeviceName)+"\n")
                        Auxiliar_file.write(str(dateorigintime)+";"+str(callingnumber)+";"+str(callednumber)+";"+str(dateconnecttime)+";"+str(datedisconnecttime)+";"+str(duration)+";"+str(originDeviceName)+";"+str(destDeviceName)+"\n")   
                        
                        contadorDiario[day]=contadorDiario[day]+1
                        #+++++++++++++++

            except:
                pass


        else:
            #Cabeceras
            general.write(str(lista[4])+";"+str(lista[8])+";"+str(lista[29])+";"+str(lista[47])+";"+str(lista[48])+";"+str(lista[55])+";"+str(lista[56])+";"+str(lista[57])+"\n")
            siptrunk_file.write(str(lista[4])+";"+str(lista[8])+";"+str(lista[29])+";"+str(lista[47])+";"+str(lista[48])+";"+str(lista[55])+";"+str(lista[56])+";"+str(lista[57])+"\n")
            Auxiliar_file.write(str(lista[4])+";"+str(lista[8])+";"+str(lista[29])+";"+str(lista[47])+";"+str(lista[48])+";"+str(lista[55])+";"+str(lista[56])+";"+str(lista[57])+"\n")
            

        #Porcentaje de avance de lectura de archivo
        avance= int((countlines/countfile)*100)
        countlines+=1

        #Actualizacion de barra GUI
        if lastavance!=avance:
            lastavance=avance
            #print avance
            #return avance, countlines,countfile
            pb.step()
            pb.update()

        #time.sleep(.01)
    general.close()
    siptrunk_file.close()
    Auxiliar_file.close()


    #raw_input(":")
    #------------- Contadores por dia -------------------------
    contador_file=open("CDR_Counters.csv","w")
    contador_file.write("Dia;Cantidad\n")
    for dia,contador in contadorDiario.items():
        contador_file.write(str(dia)+";"+str(contador)+"\n")
    contador_file.close()
    #----------------------------------------------------------

    #STEP 2 - Concurrencia de llamadas por hora
    
    #print concurrent_read
    concurrent_file=open("ReporteConcurrencia_From_"+str(minday[2])+"-"+str(minday[1])+"-"+str(minday[0])+"_to_"+str(maxday[2])+"-"+str(maxday[1])+"-"+str(maxday[0])+".csv","w")

    concurrent_file.write("FechaInicial;FechaFinal;Concurrencia\n")


    contadorConcurrencia=0
    concurrenciaMaxima=0

    print "Comienzo de analisis de concurrencia"

    Horasanalizadas=0
    #marcador=0
    for hours in range(len(horas)-1):
        desde=int(horas[hours])
        hasta=int(horas[hours+1])
        for segundos in range(desde,hasta+1):            
            concurrent_read=open("Auxiliar_From_"+str(minday[2])+"-"+str(minday[1])+"-"+str(minday[0])+"_to_"+str(maxday[2])+"-"+str(maxday[1])+"-"+str(maxday[0])+".csv","r")
            countlineas=0
            Flag=True
            for linea in concurrent_read:
                if countlineas!=0:
                    #if Flag and countlineas>marcador:
                    if Flag:
                        lista=linea.strip().split(";")
                        tiempo=lista[0]
                        conecttiempo=int(time.mktime(datetime.datetime.strptime(lista[3], '%Y-%m-%d %H:%M:%S').timetuple()))
                        #print conecttiempo
                        disconnecttiempo=int(time.mktime(datetime.datetime.strptime(lista[4], '%Y-%m-%d %H:%M:%S').timetuple()))
                        if conecttiempo>hasta:
                            #marcador=countlineas-1
                            Flag=False
                        elif (conecttiempo>desde and conecttiempo<hasta):
                            if int(conecttiempo)==segundos:
                                contadorConcurrencia+=1
                            if int(disconnecttiempo)==segundos:
                                contadorConcurrencia-=1                
                countlineas+=1
            if contadorConcurrencia>concurrenciaMaxima:
                concurrenciaMaxima=contadorConcurrencia
            concurrent_read.close()
                
        Horasanalizadas+=1
        print Horasanalizadas, concurrenciaMaxima
        concurrent_file.write(str(timestampDate(desde))+";"+str(timestampDate(hasta))+";"+str(concurrenciaMaxima)+"\n")
        concurrenciaMaxima=0
        contadorConcurrencia=0

    ttk.Label(self, text="Reportes generados con exito").grid(row=1, column=1)

 
   def askopenfilename(self):
 
     """Returns an opened file in read mode.
     This time the dialog just returns a filename and the file is opened by your own code.
     """
 
     # get filename
     filename = tkFileDialog.askopenfilename(**self.file_opt)
 
     # open file on your own
     if filename:
       return open(filename, 'r')
 


if __name__=='__main__':
   root = Tkinter.Tk()

   root.iconbitmap('py.ico')
   # Convertimos la imagen a un objeto PhotoImage de Tkinter
   tkimage = ImageTk.PhotoImage(img)
   # Ponemos la imagen en un Lable dentro de la ventana
   label= Tkinter.Label(root, image=tkimage, width=imagenAnchuraMaxima, height=imagenAlturaMaxima).pack()
   root.title("Sistema Filtro de CDR")
   pb = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
   pb.pack()
   TkFileDialogExample(root).pack()
   #ttk.Label(self, text="Generando reportes, por favor espere... - "+  str(avance)+ "%  - "+ str(countlines) + " lineas leidas de "+ str(countfile)+".").grid(row=1, column=1)
   root.mainloop()