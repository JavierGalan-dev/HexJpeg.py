#!/usr/bin/python3
# -*- coding: iso-8859-15 -*-
#
# This script is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) [2020] [Javier Galán] [www.javiergalanrico.com/]
#
# Use: HexJPEG.Py <directori> <dataoffset> <length> <HEXvalue>
#
#


from subprocess import Popen, PIPE
from subprocess import STDOUT
import os, time, signal, psutil
import sys
import io #Per manipular binary data


#Importar primer comand lines i establir variables
#
#	$1 nom d'arxiu
#	$2 percentatge (posició-offset de l'arxiu)
#	$quantitata de bytes?

print ("HexJPEG.Py")

print ("We write bytes within a given offset in a whole jpeg folder to perform glitch")

if len(sys.argv) < 5 :

	print ("Arguments missing")
	print ("Use: HexJPEG.Py <directori> <dataoffset> <length> <HEXvalue>")
	
	sys.exit()

WorkingDir = sys.argv[1]
DataOffset = int(sys.argv[2])
DataLen = int(sys.argv[3])
HEXvalue=str.encode(sys.argv[4])


WorkingFiles = os.listdir(WorkingDir)

for file in WorkingFiles :

	currentFile = WorkingDir + file

	MIMECheck = Popen(["file", currentFile, "--mime-type"], stdout=PIPE)
	MIMECheck_Output = MIMECheck.communicate()[0].rstrip()
	
	#Amb aquesta linia "magica" decodifiquem l'output de Popen 
	#necesariament per convertir-ho a string i despres apliquem
	#split per l'espai per obtenir el mime type :)
	MIMEType = MIMECheck_Output.decode().split(" ")[1] 
	
	#Si la imatge es un JPEG, aleshores
	if MIMEType == "image/jpeg" :
	
		#Primer obrim l'arxiu i llegim la data
		f = open (currentFile, 'r+b')
		data = f.read()
		f.close()
			
		#Si sumant DataOffset + Datalen 
		#superem les dimenssions de l'arxiu
		#abortem
		if (DataOffset + DataLen) > len(data) :
		
		
			print ("The given offset and byte quantity exceed the filesize")
			print ("Exiting")
			sys.exit()
		

		#LLegim streams de bytes amb io.BytesIO object!
		#el qual ens permet fer seeking dintre d'un flux
		#de data binaria
			
		binary_stream = io.BytesIO()
		binary_stream.write(data)
		
		binary_stream.seek(DataOffset)
		
		BCount = 0
		
		#Després escrivim els bytes que demani l'usuari
		#a partir de l'offset indicat
		while BCount < DataLen:
		
			binary_stream.write(HEXvalue)
			BCount += 1
			
		#Re-Escrivim l'arxiu
		
		with open( currentFile, "wb") as FNew:
		
			print ( currentFile + " : HEXing " + str(DataLen) + " bytes with " + str(HEXvalue) )
			#Destacar que usem .getvalue() per convertir el stream
			#de bytes en un objecte que puguem utilitzar
			#per escriure en un arxiu binari.
			
			FNew.write(binary_stream.getvalue())
			FNew.close()
			
			#Voilà, ja ho tenim hexejat :)
		
		
	else :
		print ("Detected non-jpeg file. Skipping")
		pass
		#sys.exit()
	pass


