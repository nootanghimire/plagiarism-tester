#!/usr/bin/python

'''
  @author Nootan Ghimire <nootan.ghimire@gmail.com>
  @license Mozilla Public License
'''

import sys
import difflib
from pyPdf import PdfFileReader

try:
  file1 = sys.argv[1]
  file2 = sys.argv[2]
except:
  print"[!] Couldn't get proper arguments!"
  print"\n\nUsage: main.py file1 file2\n\nExample: main.py \"my document.pdf\" next_document.pdf"
  exit()


try:
  input1 = PdfFileReader(file(file1, "rb"))
  input2 = PdfFileReader(file(file2, "rb"))
except:
  print "[!] Couldn't open pdf file! Is that readable? Or is it really a PDF file?"
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
  for page in range(1,input2.getNumPages()):
    text1 = input1.getPage(page).extractText()
    text2 = input2.getPage(page).extractText()
    seq = difflib.SequenceMatcher(None, text1, text2)
    d = seq.ratio()
    print "[-] For Page ", page, "Match: ", d
    add = add + d
    count = count + 1 
  return add/count

average = compareTexts()
print "\n\n[-]Average Match: ", average

