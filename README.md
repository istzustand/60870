# 60870calc
translation-class for 60870

dependencies: bitstring


In the IEC60870-Protocoll each Informationobject(IOA) is adressed via a 24bit adress.
Also there is an Application Service Data Unit wich is adressed via a 8 or 16bit adress.

Mostly the IOAs adress is written down as either an 24bit integer or as the integer-representation
of 3 bytes (IOA1 to IOA3).
Same goes for the ASDU: either a 16bit integer or 2 8bit integers.

Some operators are using the so called RWE-profile. Basically what it means is, they structure the
adresses in a certain way.

So the ASDU still conists of 2 integers but one (ANL) has 12bit while the other (SPG) consists of 
the remaining 4 bits.

The IOA adresses are strucured like 6bit for FELD, 4 bits for IMG, 3 bits for BMG, 3 bits for BEG 
and the last 8bits are for BEL.

This Class calculates the different representations from a given input.

```python
  import rwecalc as rc

  # suppose you get your adresslist like this:
  # meldetext, Anlagennummer, Spannungsebene, Feldnummer, Informationsgruppe, Betriebsmittelgruppe, Basiselementgruppe, Basiselemente, TK
  # you can instanciate the class like

  IOA = rc.InformationObject('test', 1, 1, 1, 1, 1, 1, 1, 59)

  #now you can get the adressinformation in any other representation:

  print('asdu    \t' + str(IOA.asdu.uint) + '   \t' + str(IOA.asdu.bin))
  print('asdu1   \t' + str(IOA.asdu_1.uint) + '   \t' + str(IOA.asdu_1.bin))
  print('asdu2   \t' + str(IOA.asdu_2.uint) + '   \t' + str(IOA.asdu_2.bin))
  print('Station \t' + str(IOA.anl.uint) + '   \t' + str(IOA.anl.bin))
  print('Ebene   \t' + str(IOA.spg.uint) + '   \t' + str(IOA.spg.bin))
  
  print('ioa \t\t' + str(IOA.ioa.uint) + '\t' + str(IOA.ioa.bin))
  print('ioa_1 \t\t' + str(IOA.ioa_1.uint) + '   \t' + str(IOA.ioa_1.bin))
  print('ioa_2 \t\t' + str(IOA.ioa_2.uint) + '   \t' + str(IOA.ioa_2.bin))
  print('ioa_3 \t\t' + str(IOA.ioa_3.uint) + '   \t' + str(IOA.ioa_3.bin))
  
```

```python
  #more useful in the realworld would be if you'd convert the adresslist to an csvfile, loop through it and save the result
  #again so you end up with a list ready to be punched into your telecontrolsystem
  
  import rwecalc as rc
  
  import csv
  
  infoobjects = []
  csvorg = 'data.csv'
  newcsv = 'newdata.csv'
  

  with open(csvorg) as csvfile
    csvdata = csv.reader(csvfile, delimiter=';')
      for row in csvdata:
          infoobjects.append(rc.InformationObject(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))


  with open(newcsv,mode='w') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter=';')
      csvwriter.writerow(['Meldetext', 'Station', 'Spannungsebene', 'ASDU', 'ASDU1', 'ASDU2', 'IOA', 'IOA1', 'IOA2',
                          'IOA3', 'TK'])
      for i in infoobjects:
          csvwriter.writerow([i.meldetext, i.anl.uint, i.spg.uint, i.asdu.uint, i.asdu_1.uint,
                              i.asdu_2.uint, i.ioa.uint, i.ioa_1.uint, i.ioa_2.uint, i.ioa_3.uint, i.tk])
                              
```
                              
