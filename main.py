#!/usr/bin/python

'''
  @author Nootan Ghimire <nootan.ghimire@gmail.com>
  @license Mozilla Public License
'''

import sys
import difflib
from pyPdf import PdfFileReader

verbose = False

if(len(sys.argv)>3):
  if(sys.argv[1] == "-v"):
    verbose = True
    file1 = sys.argv[2]
    file2 = sys.argv[3]
  else:
    print "[X] Please supply Proper Arguments"
    print"\n\nUsage: main.py file1 file2\n\nExample: main.py \"my document.pdf\" next_document.pdf"
    print"\nOr:  main.py -v file1 file2\n\nExample: main.py -v \"my document.pdf\" next_document.pdf"
    exit()
elif(len(sys.argv)>2):
  file1 = sys.argv[1]
  file2 = sys.argv[2]
else:
  print "[X] Please supply Proper Arguments"
  print "\n\nUsage: main.py file1 file2\n\nExample: main.py \"my document.pdf\" next_document.pdf"
  print "\nOr: main.py -v file1 file2\n\nExample: main.py -v \"my document.pdf\" next_document.pdf"
  exit()

'''
try:
  file1 = sys.argv[1]
  file2 = sys.argv[2]
except:
  print"[X] Couldn't get proper arguments!"
  print"\n\nUsage: main.py file1 file2\n\nExample: main.py \"my document.pdf\" next_document.pdf"
  exit()
'''

try:
  input1 = PdfFileReader(file(file1, "rb"))
  input2 = PdfFileReader(file(file2, "rb"))
except:
  if(verbose):
    print "[X] Couldn't open pdf file! Is that readable? Or is it really a PDF file? Or do you have pyPDF?"
  exit()

#find the larger file
if(input1.getNumPages() < input2.getNumPages()):
  input3 = input2
  input2 = input1
  input1 = input3
  #simple swapping :)

def compareNumPages():
  return( input1.getNumPages() == input2.getNumPages())

def compareTexts():
  add = 0
  count = 0
  max_match_in_page = [] 
  max_match_value = 0
  for page in range(0,input2.getNumPages()):
    text1 = input1.getPage(page).extractText()
    text2 = input2.getPage(page).extractText()
    seq = difflib.SequenceMatcher(None, text1, text2)
    d = seq.ratio()
    if(verbose):
      print "[*] For Page ", page + 1 , "Match: ", d
    if(max_match_value < d):
      max_match_value = d
      max_match_in_page = None
      max_match_in_page = [page + 1] #because page is 0-indexed!
    elif(max_match_value == d):
      max_match_in_page.append(page+1)
    add = add + d
    count = count + 1 
  return {'average':(add/count), 'max_match':max_match_value, 'max_match_page':max_match_in_page}

returnDict  = compareTexts()
print "\n\n[*] Average Match: ", returnDict['average']

if(compareNumPages() == True):
  print "[*] Both files have same number of pages: ", input1.getNumPages()
else:
  print "[*] File \"", file1, ": ", input1.getNumPages(), " pages"
  print "[*] File \"", file2, ": ", input2.getNumPages(), " pages"
print "[*] Max matched page(s): ", returnDict['max_match_page']
print "    Matched value: ", returnDict['max_match']
