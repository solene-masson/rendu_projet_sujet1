import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel(r'C:\Users\sosop\OneDrive\Documents\EIVP\Algo\projet_info\EIVP_KM_version_finale.xlsx')

data['sent_at'] = pd.to_datetime(data.sent_at)      #On change le type de la colonne

capteur_1 = data[data['id']==1]
capteur_2 = data[data['id']==2]
capteur_3 = data[data['id']==3]
capteur_4 = data[data['id']==4]
capteur_5 = data[data['id']==5]
capteur_6 = data[data['id']==6]

time1 = capteur_1.sent_at                       #Date et heure pour chaque capteur
time2 = capteur_2.sent_at
time3 = capteur_3.sent_at
time4 = capteur_4.sent_at
time5 = capteur_5.sent_at
time6 = capteur_6.sent_at


##FONCTIONS STATISTIQUES Début

def maximum(L):
    max = L[0]
    for k in range(1,len(L)):
        if L[k]>max:
           max = L[k]
    return(max)

def minimum(L):
    min = L[0]
    for k in range(1,len(L)):
        if L[k]<min:
            min = L[k]
    return(min)

def moyenne(L):
    s=0
    n=len(L)
    for k in range(n):
        s+=L[k]
    return(s/n)
    
def variance(L):
    m=moyenne(L)
    return moyenne([(x-m)**2 for x in L])

def ecart_type(L):
    return variance(L)**0.5


def Fusion(L1,L2) :
    LF=[ ]
    while len(L1)>0 and len(L2)>0 :
        if L1[0]<L2[0] :
            LF.append(L1.pop(0))
        else :
            LF.append(L2.pop(0))
    return LF+L1+L2

def TriFusion(L) :
    if len(L)<=1 :
        return L
    else :
        n=len(L)//2
        L1=TriFusion(L[0 : n])
        L2=TriFusion(L[n : len(L)])
        return Fusion(L1,L2)

def mediane(L):
    # L = L['colonneintéressante'].tolist()
    L = TriFusion(L)
    n= len(L)
    if n < 1:
        return None
    if n % 2 == 0 :
        return ( L[(n-1)//2] + L[(n+1)//2] ) / 2.0
    else:
        return L[(n-1)//2]
    
def quartiles1_3(L):
    TriFusion(L)
    n = len(L)
    if  n%4==0 :
        Q1 = L[(n//4)-1]
        Q3 = L[(3*n)//4-1]
    if n%4!=0 :
        Q1 = L[(n//4)]
        Q3 = L[((3*n)//4)]
    return Q1,Q3

    
def covariance(X,Y):                   
    L=[]
    for k in range(len(X)):
        L.append((X[k]-moyenne(X))*(Y[k]-moyenne(Y)))
    return moyenne(L)

def indice_corr(X,Y):                   
    return (covariance(X,Y)/(ecart_type(X)*ecart_type(Y)))

def partie_entiere(nombre):
    nb=nombre-int(nombre)
    if nb<0.5:
        return int(nombre)
    else:
        return int(nombre)+1

def humidex(temperature,humidity):
    return partie_entiere((temperature+(5/9)*((6.112)*10**(7.5*(temperature/(237.7+temperature)))*(humidity/100)-10)))

##FONCTIONS STATISTIQUES Fin



##date min et max pour chaque capteur

mdate1,Mdate1 = minimum(time1.tolist()),maximum(time1.tolist())        
mdate2,Mdate2 = minimum(time2.tolist()),maximum(time2.tolist())        
mdate3,Mdate3 = minimum(time3.tolist()),maximum(time3.tolist())         
mdate4,Mdate4 = minimum(time4.tolist()),maximum(time4.tolist())      
mdate5,Mdate5 = minimum(time5.tolist()),maximum(time5.tolist())      
mdate6,Mdate6 = minimum(time6.tolist()),maximum(time6.tolist())   


##Courbes et anomalies

def anomalies(variable,numero):                     #Méthode écart aux extrema
  
    if (numero in ['1','2','3','4','5','6'])==True:
        capteur_numero = []
        
        #On choisit les dates et capteurs pertinents
        
        if numero == '1':  
            time,capteur_numero,date_max,date_min = time1,capteur_1,Mdate1,mdate1
            pas = 1
        elif numero == '2':
            time,capteur_numero,date_max,date_min = time2,capteur_2,Mdate2,mdate2
            pas = 1
        elif numero == '3':
            time,capteur_numero,date_max,date_min = time3,capteur_3,Mdate3,mdate3
            pas = 1
        elif numero == '4':
            time,capteur_numero,date_max,date_min = time4,capteur_4,Mdate4,mdate4
            pas  = 1
        elif numero == '5':
            time,capteur_numero,date_max,date_min = time5,capteur_5,Mdate5,mdate5
            pas = 19
        elif numero == '6':
            time,capteur_numero,date_max,date_min = time6,capteur_6,Mdate6,mdate6
            pas = 1
        
        anomalies = []
        points_anomalies = []
        
        #CAS CO2
        if  variable == 'CO2':
            L = capteur_numero['co2'].tolist()
            T = time.tolist()
            for k in range(len(L)):
                if 380>L[k] or L[k]>1100 :
                    anomalies.append(T[k])
                    points_anomalies.append(L[k])
                return anomalies, points_anomalies
                
        #AUTRES CAS
        var = []
        if variable == 'Température':
             var = 'temp'
                 
        elif variable == 'Bruit':
            var = 'noise'
                 
        elif variable == 'Luminosité':
            var = 'lum'
                 
        elif variable == 'Humidité':
            var = 'humidity' 
                 
        # On détermine la moyenne maximale et minimale sur la période
        t = date_min
        delta = pd.Timedelta( hours = pas ) 
        max_jour = []
        min_jour = []
        
        while t < date_max :
            date = capteur_numero.set_index(['sent_at'])
            selection = date.loc[ t : t+delta ]
            L = selection[var].tolist()
            max = maximum(L)
            min = minimum(L)
            max_jour.append(max)
            min_jour.append(min)
            t += delta
            
        moy_min = moyenne(min_jour)
        moy_max = moyenne(max_jour)
        ecart_type_min = ecart_type(min_jour)
        ecart_type_max = ecart_type(max_jour)
            
        # On cherche les valeurs aberrantes
        Q = capteur_numero[var].tolist()
        T = time.tolist()
        
        for k in range(len(Q)):      
            if Q[k] <= moy_min-2*ecart_type_min or Q[k] >= moy_max+2*ecart_type_max :
                anomalies.append(T[k])
                points_anomalies.append(Q[k])
        
                
        return anomalies, points_anomalies
     
    else :              #Mauvais capteur
        return('Capteur non existant')

    
def anomalies_mzscore(variable,numero):    #Méthode Modified Z-score. Pour l'utiliser, changer anomalies en anomalies_mzscore dans display()
  
    if (numero in ['1','2','3','4','5','6'])==True:
        capteur_numero = []
        
        #On choisit les dates et capteurs pertinents
        
        if numero == '1':  
            time,capteur_numero,date_max,date_min = time1,capteur_1,Mdate1,mdate1
            pas = 14
        elif numero == '2':
            time,capteur_numero,date_max,date_min = time2,capteur_2,Mdate2,mdate2
            pas = 14
        elif numero == '3':
            time,capteur_numero,date_max,date_min = time3,capteur_3,Mdate3,mdate3
            pas = 14
        elif numero == '4':
            time,capteur_numero,date_max,date_min = time4,capteur_4,Mdate4,mdate4
            pas = 14
        elif numero == '5':
            time,capteur_numero,date_max,date_min = time5,capteur_5,Mdate5,mdate5
            pas  = 14
        elif numero == '6':
            time,capteur_numero,date_max,date_min = time6,capteur_6,Mdate6,mdate6
            pas = 14
        

        anomalies = []
        points_anomalies = []
        
        #CAS CO2
        if  variable == 'CO2':
            L = capteur_numero['co2'].tolist()
            T = time.tolist()
            for k in range(len(L)):
                if 380>L[k] or L[k]>1100 :
                    anomalies.append(T[k])
                    points_anomalies.append(L[k])
                return anomalies, points_anomalies
                
        #AUTRES CAS
        var = []
        if variable == 'Température':
             var = 'temp'
                 
        elif variable == 'Bruit':
            var = 'noise'
                 
        elif variable == 'Luminosité':
            var = 'lum'
                
        elif variable == 'Humidité':
            var = 'humidity' 
                             
# Méthode Modified Z-score, on détermine la médiane et le MAD
        t = date_min
        delta = pd.Timedelta( days = pas ) 

        while t < date_max :
            date = capteur_numero.set_index(['sent_at'])
            selection = date.loc[ t : t+delta ]
            L = selection[var].tolist()
            T = selection.index.tolist()
            med =  mediane(L)
            MAD = [(abs(l-mediane(L))) for l in L]
            
            for k in range(len(L)):
        
                if L[k] <= med-2*mediane(MAD)/0.6745 or L[k] >= med+2*mediane(MAD)/0.6745 :
                    anomalies.append(T[k])
                    points_anomalies.append(L[k])
                    
            t += delta
        
                
        return anomalies, points_anomalies
     
    else :              #Mauvais capteur
        return('Capteur non existant')    


    
def display():
    variable = input('Choisir Température, Bruit, Luminosité, CO2, Humidité ou Humidex : ')
    
    if variable not in ['Température','Bruit','Luminosité', 'CO2', 'Humidité', 'Humidex', 'Corrélation'] :
            return("La variable choisie n'existe pas...")
    
    
    numero = input('Saisir le numéro du capteur : ' )
    
    if (numero in ['1','2','3','4','5','6'])==True:
        time = []
        capteur_numero = []
        
        #Dates choisies
        
        start_date = pd.to_datetime(input('Saisir date début AAAA-MM-JJ HH:MM : ')).tz_localize('CET')
        end_date = pd.to_datetime(input('Saisir date fin AAAA-MM-JJ HH:MM : ')).tz_localize('CET')
          
        #On choisit les dates et capteurs pertinents
        
        if numero == '1':  
            time,capteur_numero,date_max,date_min = time1,capteur_1,Mdate1,mdate1
        elif numero == '2':
            time,capteur_numero,date_max,date_min = time2,capteur_2,Mdate2,mdate2
        elif numero == '3':
            time,capteur_numero,date_max,date_min = time3,capteur_3,Mdate3,mdate3
        elif numero == '4':
            time,capteur_numero,date_max,date_min = time4,capteur_4,Mdate4,mdate4
        elif numero == '5':
            time,capteur_numero,date_max,date_min = time5,capteur_5,Mdate5,mdate5
        elif numero == '6':
            time,capteur_numero,date_max,date_min = time6,capteur_6,Mdate6,mdate6
        
        time_anomalies, pos_anomalies = anomalies(variable,numero)
        
       # Problème
       
        if start_date<date_min or end_date>date_max :
            return('Dates non valides, les dates limites pour ce capteur sont :', date_min, date_max)
        
            
        if variable == 'Température':
            df = capteur_numero.set_index(['sent_at'])
            selection = df.loc[ start_date : end_date ]
            L = selection.temp.tolist()
            
            plt.figure("Courbe de la température en fonction du temps")
            plt.gcf().subplots_adjust(left = 0.1, bottom = 0.5, right = 0.9, top = 0.95, wspace = 0, hspace = 0)
            plt.plot(time,capteur_numero.temp)
            plt.plot(time_anomalies, pos_anomalies, "x")
            
            plt.title('Température en fonction du temps', color='r')
            plt.xlabel('Date')        
            plt.xticks(rotation='vertical') 
            plt.xlim(start_date, end_date)                       
            plt.ylabel('Température (°C)')

            plt.annotate('minimum :', xycoords = 'figure fraction', xy = (0.025, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(minimum(L), xycoords = 'figure fraction', xy = (0.15,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('maximum :', xycoords = 'figure fraction', xy = (0.025, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(maximum(L), xycoords = 'figure fraction', xy = (0.15,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('moyenne :', xycoords = 'figure fraction', xy = (0.27, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(moyenne(L), xycoords = 'figure fraction', xy = (0.37,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('mediane :', xycoords = 'figure fraction', xy = (0.27, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(mediane(L), xycoords = 'figure fraction', xy = (0.37,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('variance :', xycoords = 'figure fraction', xy = (0.65, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(variance(L), xycoords = 'figure fraction', xy = (0.76,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')  
            plt.annotate('ecart-type :', xycoords = 'figure fraction', xy = (0.65, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(ecart_type(L), xycoords = 'figure fraction', xy = (0.76,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')  
    
            plt.show()
            
        elif variable == 'Bruit' :
            df = capteur_numero.set_index(['sent_at'])
            selection = df.loc[ start_date : end_date ]
            L = selection.noise.tolist()
            
            plt.figure("Courbe du bruit en fonction du temps")
            plt.gcf().subplots_adjust(left = 0.1, bottom = 0.5, right = 0.9, top = 0.95, wspace = 0, hspace = 0)
            plt.plot(time,capteur_numero.noise)
            plt.plot(time_anomalies, pos_anomalies, "x")
            
            plt.title('Bruit en fonction du temps', color='r')
            plt.xlabel('Date')        
            plt.xticks(rotation='vertical') 
            plt.xlim(start_date, end_date)                      
            plt.ylabel('Bruit (en dBA)')
            
            plt.annotate('minimum :', xycoords = 'figure fraction', xy = (0.025, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(minimum(L), xycoords = 'figure fraction', xy = (0.15,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('maximum :', xycoords = 'figure fraction', xy = (0.025, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(maximum(L), xycoords = 'figure fraction', xy = (0.15,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('moyenne :', xycoords = 'figure fraction', xy = (0.27, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(moyenne(L), xycoords = 'figure fraction', xy = (0.37,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('mediane :', xycoords = 'figure fraction', xy = (0.27, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(mediane(L), xycoords = 'figure fraction', xy = (0.37,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('variance :', xycoords = 'figure fraction', xy = (0.65, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(variance(L), xycoords = 'figure fraction', xy = (0.76,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')  
            plt.annotate('ecart-type :', xycoords = 'figure fraction', xy = (0.65, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(ecart_type(L), xycoords = 'figure fraction', xy = (0.76,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')     
            
            plt.show()
            
        elif variable == 'Luminosité' :
            df = capteur_numero.set_index(['sent_at'])
            selection = df.loc[ start_date : end_date ]
            L = selection.lum.tolist()
            
            plt.figure("Courbe de la luminosité en fonction du temps")
            plt.gcf().subplots_adjust(left = 0.1, bottom = 0.5, right = 0.9, top = 0.95, wspace = 0, hspace = 0)
            plt.plot(time,capteur_numero.lum)
            plt.plot(time_anomalies, pos_anomalies, "x")
            
            plt.title('Luminosité en fonction du temps', color='r')
            plt.xlabel('Date')        
            plt.xticks(rotation='vertical') 
            plt.xlim(start_date, end_date)                       
            plt.ylabel('Luminosité (en lux)')
            
            plt.annotate('minimum :', xycoords = 'figure fraction', xy = (0.025, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(minimum(L), xycoords = 'figure fraction', xy = (0.15,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('maximum :', xycoords = 'figure fraction', xy = (0.025, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(maximum(L), xycoords = 'figure fraction', xy = (0.15,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('moyenne :', xycoords = 'figure fraction', xy = (0.27, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(moyenne(L), xycoords = 'figure fraction', xy = (0.37,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('mediane :', xycoords = 'figure fraction', xy = (0.27, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(mediane(L), xycoords = 'figure fraction', xy = (0.37,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('variance :', xycoords = 'figure fraction', xy = (0.65, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(variance(L), xycoords = 'figure fraction', xy = (0.76,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')  
            plt.annotate('ecart-type :', xycoords = 'figure fraction', xy = (0.65, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(ecart_type(L), xycoords = 'figure fraction', xy = (0.76,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            
            plt.show()
        
        elif variable == 'CO2' :
            df = capteur_numero.set_index(['sent_at'])
            selection = df.loc[ start_date : end_date ]
            L = selection.co2.tolist()
            
            plt.figure("Courbe de CO2 en fonction du temps")
            plt.gcf().subplots_adjust(left = 0.1, bottom = 0.5, right = 0.9, top = 0.95, wspace = 0, hspace = 0)
            plt.plot(time,capteur_numero.co2)
            plt.plot(time_anomalies, pos_anomalies, "x")
                
            plt.title('Teneur en CO2 en fonction du temps', color='r')
            plt.xlabel('Date')        
            plt.xticks(rotation='vertical') 
            plt.xlim(start_date, end_date)                       
            plt.ylabel('Teneur en CO2 (ppm)')
            
            plt.annotate('minimum :', xycoords = 'figure fraction', xy = (0.025, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(minimum(L), xycoords = 'figure fraction', xy = (0.15,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('maximum :', xycoords = 'figure fraction', xy = (0.025, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(maximum(L), xycoords = 'figure fraction', xy = (0.15,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('moyenne :', xycoords = 'figure fraction', xy = (0.27, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(moyenne(L), xycoords = 'figure fraction', xy = (0.37,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('mediane :', xycoords = 'figure fraction', xy = (0.27, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(mediane(L), xycoords = 'figure fraction', xy = (0.37,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('variance :', xycoords = 'figure fraction', xy = (0.65, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(variance(L), xycoords = 'figure fraction', xy = (0.76,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')  
            plt.annotate('ecart-type :', xycoords = 'figure fraction', xy = (0.65, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(ecart_type(L), xycoords = 'figure fraction', xy = (0.76,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            
            plt.show()
        
        elif variable == 'Humidité' :
            df = capteur_numero.set_index(['sent_at'])
            selection = df.loc[ start_date : end_date ]
            L = selection.humidity.tolist()
            
            plt.figure("Courbe de l'humidité en fonction du temps")
            plt.gcf().subplots_adjust(left = 0.1, bottom = 0.5, right = 0.9, top = 0.95, wspace = 0, hspace = 0)
            plt.plot(time,capteur_numero.humidity)
            plt.plot(time_anomalies, pos_anomalies, "x")
            
            plt.title('Humidité relative en fonction du temps', color='r')
            plt.xlabel('Date')        
            plt.xticks(rotation='vertical') 
            plt.xlim(start_date, end_date)                       
            plt.ylabel('Humidité relative (en %)')
            
            plt.annotate('minimum :', xycoords = 'figure fraction', xy = (0.025, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(minimum(L), xycoords = 'figure fraction', xy = (0.15,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('maximum :', xycoords = 'figure fraction', xy = (0.025, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(maximum(L), xycoords = 'figure fraction', xy = (0.15,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('moyenne :', xycoords = 'figure fraction', xy = (0.27, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(moyenne(L), xycoords = 'figure fraction', xy = (0.37,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('mediane :', xycoords = 'figure fraction', xy = (0.27, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(mediane(L), xycoords = 'figure fraction', xy = (0.37,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')
            plt.annotate('variance :', xycoords = 'figure fraction', xy = (0.65, 0.09), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(variance(L), xycoords = 'figure fraction', xy = (0.76,0.09), fontsize=7, color = 'blue', backgroundcolor = 'white')  
            plt.annotate('ecart-type :', xycoords = 'figure fraction', xy = (0.65, 0.05), fontsize=7, color = 'g', backgroundcolor = 'white')
            plt.annotate(ecart_type(L), xycoords = 'figure fraction', xy = (0.76,0.05), fontsize=7, color = 'blue', backgroundcolor = 'white')

            plt.show()
            
        elif variable == 'Humidex' :
            df = capteur_numero.set_index(['sent_at'])
            selection = df.loc[ start_date : end_date ]
            H = selection.humidity.tolist()
            T = selection.temp.tolist()
            temperature = moyenne(T)
            humidity = moyenne(H)
            return partie_entiere((temperature+(5/9)*((6.112)*10**(7.5*(temperature/(237.7+temperature)))*(humidity/100)-10)))
        
        else :
            return("La variable choisie n'existe pas...")
        
    
    else :              #Mauvais capteur
        return('Capteur non existant')


## FONCTION CORRELATION

def corrélation():
    variable1 = input('Choisir Température, Bruit, Luminosité, CO2, Humidité : ')
    variable2 = input('Choisir Température, Bruit, Luminosité, CO2, Humidité : ')
    
    if variable1 not in ['Température','Bruit','Luminosité', 'CO2', 'Humidité'] :
        return("La variable choisie n'existe pas...")
    
    if variable2 not in ['Température','Bruit','Luminosité', 'CO2', 'Humidité'] :
        return("La variable choisie n'existe pas...")
    
    if variable1 == variable2 :
        return ("Les variables choisies sont les mêmes")
    
    numero = input('Saisir le numéro du capteur : ' )
    
    if (numero in ['1','2','3','4','5','6'])==True:
        capteur_numero = []
        
        start_date = pd.to_datetime(input('Saisir date début AAAA-MM-JJ HH:MM : ')).tz_localize('CET')
        end_date = pd.to_datetime(input('Saisir date fin AAAA-MM-JJ HH:MM : ')).tz_localize('CET')
        
        #On choisit les dates et capteurs pertinents
        
        if numero == '1':  
            time,capteur_numero,date_max,date_min = time1,capteur_1,Mdate1,mdate1
        elif numero == '2':
            time,capteur_numero,date_max,date_min = time2,capteur_2,Mdate2,mdate2
        elif numero == '3':
            time,capteur_numero,date_max,date_min = time3,capteur_3,Mdate3,mdate3
        elif numero == '4':
            time,capteur_numero,date_max,date_min = time4,capteur_4,Mdate4,mdate4
        elif numero == '5':
            time,capteur_numero,date_max,date_min = time5,capteur_5,Mdate5,mdate5
        elif numero == '6':
            time,capteur_numero,date_max,date_min = time6,capteur_6,Mdate6,mdate6
    
        if start_date<date_min or end_date>date_max :
            return('Dates non valides, les dates limites pour ce capteur sont :', date_min, date_max)
        
        var1 = []

        if variable1 == 'Température':
            var1 = 'temp'
                 
        elif variable1 == 'Bruit':
            var1 = 'noise'
                     
        elif variable1 == 'Luminosité':
            var1 = 'lum'
                 
        elif variable1 == 'CO2':
            var1 = 'co2'
                 
        elif variable1 == 'Humidité':
            var1 = 'humidity' 
    
        df = capteur_numero.set_index(['sent_at'])
        selection = df.loc[ start_date : end_date ]
        X = selection[var1].tolist()
        
        var2 = []
    
        if variable2 == 'Température' :
            var2 = 'temp'
    
        elif variable2 == 'Bruit':
            var2 = 'noise'
                 
        elif variable2 == 'Luminosité':
            var2 = 'lum'
                 
        elif variable2 == 'CO2':
            var2 = 'co2'
                 
        elif variable2 == 'Humidité':
            var2 = 'humidity'
            
        else :
            return("La variable choisie n'existe pas...")
        
        df = capteur_numero.set_index(['sent_at'])
        selection = df.loc[ start_date : end_date ]
        Y = selection[var2].tolist()
        
        correlation = covariance(X,Y)/(ecart_type(X)*ecart_type(Y))
        
            
        plt.figure("Courbe des variables en fonction du temps")
        plt.gcf().subplots_adjust(left = 0.1, bottom = 0.5, right = 0.9, top = 0.95, wspace = 0, hspace = 0)
        plt.plot(time, capteur_numero[var1], label=variable1)
        plt.plot(time, capteur_numero[var2], label=variable2)
        plt.title('Variables en fonction du temps', color='r')
        plt.xlabel('Date')        
        plt.xticks(rotation='vertical') 
        plt.xlim(start_date, end_date)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
                   
        plt.annotate('indice de corrélation :', xycoords = 'figure fraction', xy = (0.18, 0.09), fontsize=10, color = 'g', backgroundcolor = 'white')
        plt.annotate(correlation, xycoords = 'figure fraction', xy = (0.42,0.09), fontsize=10, color = 'blue', backgroundcolor = 'white')
        plt.show()
        
        
    
    else :              #Mauvais capteur
        return('Capteur non existant')

