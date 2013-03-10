#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/adam/wikt/pywikipedia')
#sys.path.append('/home/alkamid/wikt/pywikipedia')
import wikipedia
import catlib
import pagegenerators
import re
from klasa import *
	
def main():

	site = wikipedia.getSite('fr', 'wiktionary')
	cat = catlib.Category(site,u'Catégorie:Noms_communs_en_français')
	#cat = catlib.Category(site,u'Catégorie:français')
	lista = pagegenerators.CategorizedPageGenerator(cat)
	
	for a in lista:
		h = HasloFr(a.title())
		if h.type == 3:
			h.langs()
			for c in h.list_lang:
				if c.state == 1 and u'fr' in c.lang:
					print u'\n' + h.title
					c.pola()
					if c.noun.typ:
						print c.genre
					
					

if __name__ == '__main__':
	try:
		main()
	finally:
		wikipedia.stopme()
