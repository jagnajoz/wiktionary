#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
sys.path.append('/home/adam/pywiki/pywikipedia')
#sys.path.append('/home/alkamid/wikt/pywikipedia')
import pywikibot
import re
import time
from pywikibot import pagegenerators

def main():
    #lista = pagegenerators.AllpagesPageGenerator()
    #lista_svg = pagegenerators.RegexFilterPageGenerator(lista, u'.*(clerical|kaishu|xinshu|still|caoshu|songti|oracle|bronze|bigseal|seal)\.(svg|SVG|PNG|GIF)')

    lista = ['a', 'b', 'c']
    for a in lista:
        print(a)
    for b in lista:
        print(b)
    #for a in lista_svg:
    #       print a.title()

if __name__ == '__main__':
    try:
        main()
    finally:
        pywikibot.stopme()
