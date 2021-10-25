#!/usr/bin/python3

import json
import re

regex = "([^ ]+).+ \[(.+)\] \"([A-Z]{3,}) ([^ ]+) ([^ ]+)\" (\d{3}) ([^ ]+) \"(.+)\" \"(.+)\"$"

#83.149.9.216 - - [17/May/2015:10:05:03 +0000] "GET /presentations/logstash-monitorama-2013/images/kibana-search.png HTTP/1.1" 200 203023 "http://semicomplete.com/presentations/logstash-monitorama-2013/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"

# ^([^ ]+)  --> Groupe 1 : 	Cherche un seul ou une infinité de caractère qui ne vaut pas un espace (début de ligne)	--> 83.149.9.216
#.+ 		--> Groupe 0 : 	Cherche n'importe quel caractere une seule ou une infinité de fois						-->  - - 
#\[			--> Groupe 0 :  Cherche le caractere [ 																	--> [
#(.+)		--> Groupe 2 :	Cherche n'importe quel caractere une seule ou une infinité de fois						--> 17/May/2015:10:05:03 +0000
#\]			--> Groupe 0 : 	Cherche le caractere ]																	--> ]
#\"			--> Groupe 0 : 	Cherche le caractere "																	--> "	
#([A-Z]{3,})-->	Groupe 3 : 	Cherche une suite de 3 caractères ou plus situés entre A et Z							--> GET
#([^ ]+)	--> Groupe 4 : 	Cherche un seul ou une infinité de caractère qui ne vaut pas un espace					--> /presentations/logstash-monitorama-2013/images/kibana-search.png
#([^ ]+)	--> Groupe 5 :  '		'		'		'		'		'		'		'		'						--> HTTP/1.1
#\"			--> Groupe 0 :  Cherche le caractere "																	--> "
#(\d{3})	--> Groupe 6 :	Cherche exactement 3 chiffres situés entre 1 et 9										--> 200
#([^ ]+)	--> Groupe 7 : 	Cherche un seul ou une infinité de caractère qui ne vaut pas un espace					--> 203023
#\"			--> Groupe 0 : 	Cherche le caractere "																	--> "
#(.+)		--> Groupe 8 :	Cherche n'importe quel caractere une seule ou une infinité de fois						--> http://semicomplete.com/presentations/logstash-monitorama-2013/
#\"			--> Groupe 0 : 	Cherche le caractere "																	--> "
#\"			--> Groupe 0 : 	Cherche le caractere "																	--> "
#(.+)		--> Groupe 9 : 	Cherche n'importe quel caractere une seule ou une infinité de fois						--> Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36
#\"$		--> Groupe 0 : 	Cherche le caractere "	& (fin de ligne)												--> "

#Groupe 0 : Ce que l'on ne capture pas en tant qu'élément 

inputFile = "C:/Users/trist/Desktop/apache_logs"

#Fonction qui traite les lignes et les retourne dans une liste et nous indique s'il y a eu une ou des erreurs 
def parseLine(line):					

	doneLine={}							#Création d'un dictionnaire dans la variable "doneLine"
	cutLine=re.search(regex,line)		#On Parcourt la ligne à la recherche du premier emplacement où le 
											#motif de l'expression régulière produit une correspondance, et renvoie
											#un objet match correspondant. Retourne None si aucune position 
											#dans la chaîne ne correspond au motif
	
	if cutLine:											#Si la ligne se découpe correctement on affecte 
		doneLine['remote_ip']=cutLine.group(1)				#les valeurs trouvées grace a l'expression réguliere
		doneLine['time']=cutLine.group(2)					#aux différentes clées (remote_ip, time,...)...
		doneLine['request']=cutLine.group(3)
		doneLine['path']=cutLine.group(4)
		doneLine['protocol']=cutLine.group(5)
		doneLine['response']=cutLine.group(6)
		doneLine['bytes']=cutLine.group(7)
		doneLine['referrer']=cutLine.group(8)
		doneLine['usr_agent'] = cutLine.group(9)
		
		usr_agent=doneLine['usr_agent']
		
		doneLine['system_agent']=wich_os(usr_agent)				#On va utiliser les fonction ci dessous 
		doneLine['browser_agent']=wich_browser(usr_agent)			#pour retrouver l'OS et le navigateur
		
		
		
	
		return doneLine							#...On retourne la ligne découpée dans la variable doneLine (le dictionnaire)
		
	else: 										#...Sinon, on affiche la ligne qui pose problème ainsi qu'un message(1)
		print(line)
		print("L'expression réguliere ne trouve pas de paterne fonctionnant pas avec cette ligne")
			
	return None	

#Fonction va retrouver l'OS utilisé par le client et nous le retourner
def wich_os(usr_agent):
	if "Windows" in usr_agent:
		sys_agent = "Windows"
	elif "Linux" in usr_agent:
		if "Android" in usr_agent:
			sys_agent = "Android"
		else:
			sys_agent = "Linux"
	elif "Mac" in usr_agent:
		if "iPhone" in usr_agent:
			sys_agent = "iPhone OS"
		elif "iPad" in usr_agent:
			sys_agent = "iPad OS"
		else:
			sys_agent = "Mac OS"
	else:
		sys_agent = "Unknown OS"
	return sys_agent

#Fonction va retrouver le navigateur utilisé par le client et nous le retourner
def wich_browser(usr_agent):
    if "Chrome" in usr_agent:
        browser = "Google Chrome"
    elif "Safari" in usr_agent:
        browser = "Safari"
    elif "MSIE" in usr_agent:
        browser = "MS Internet Explorer/Edge"
    elif "Firefox" in usr_agent:
        browser = "Mozilla Firefox"
    elif "bot" in usr_agent:
        browser = "Bot"
    else:
        browser = "Unknown web browser"
    return browser

def parseFile(fileName): 						#Fonction qui va appliquer parseline à toutes les lignes du fichier
	list = []									#Création d'une liste
	with open (inputFile, "r") as opened: 		#On ouvre le fichier et on le lit grace a la fonction "open" ("inputFile" contient le chemin du fichier)
													#(on utilise "with" pour fermer automatiquement le fichier apres l'avoir lu)
		for line in opened:						#Boucle for : Pour chaque ligne lue,
			dic_line=parseLine(line)			#On utilise la fonction parseline et on met le résultat dans la variable "dic_line"
			if dic_line:						#Si la fonction parseline a bien renvoyée un résultat...
				list.append(dic_line)			#...On ajoute le résultat (dictionnaire) à notre liste
			else :								#...Sinon, on affiche le message suivant (qui va de paire avec le message (1) )
				print("La ligne n'est pas ajoutée à la liste")
	return list									#Enfin, on retourne la liste contenant tous les dictionnaires associés a chaques lignes
			
			
data=parseFile(inputFile)	#On utilise la fonction "parseFile" sur le fichier souhaité, 
															#et on met le résultat dans la variable "data"

with open("logs_converted.json", "w") as opened : 		#Un fichier "logs_converted" au format .json est créé en mode écriture
	json.dump(data,opened, indent=4)					#On convertit le résultat de notre fonction "parseFile" contenue dans la 
															#variable "data" au format .json et on le met dans notre fichier péalablement créé
															#On indente de 4 pour que ce soit plus lisible
