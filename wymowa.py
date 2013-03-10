#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
generate a list of Polish words lacking pronunciation; output written to Wikipedysta:AlkamidBot/wymowa and wymowa.txt
groups pages in four categories:
1. starting with a capital letter
2. not 1
3. foreign word in Polish use
4. a list generated from the most visited pages
'''
import os
import codecs
import catlib
import wikipedia
import pagegenerators
import re
import datetime
from klasa import *

def main():
	
	#get the most popular pages (generated by visits.py)
	popularList = []
	popularFile = codecs.open('%s/wikt/moje/log/visits.txt' % os.environ['HOME'], encoding='utf-8')
	for line in popularFile:
		popularList.append(line.split('|')[0])
	popularList.remove(u'\n')
	#end of getting the most popular pages
	
	#get a list of archaic words from XML dump
	lista_przest = []
	lista_przest2 = []
	re_przest = re.compile(ur'{{przest}}')
	re_num = re.compile(ur': \([0-9]\.[0-9]\)')
	lista_stron = getListFromXML('xxx', True)
	for page in lista_stron:
		try: word = Haslo(page.title, page.text)
		except sectionsNotFound:
			pass
		except WrongHeader:
			pass
		else:
			if word.type == 3:
				for lang in word.listLangs:
					if lang.lang == 'polski':
						lang.pola()
						if lang.type == 9:
							s_przest = re.findall(re_przest, lang.znaczeniaWhole.text)
							s_num = re.findall(re_num, lang.znaczeniaWhole.text)
							if len(s_przest) == len(s_num):
								lista_przest.append(word.title)
	
	site = wikipedia.getSite()
	site_co = wikipedia.getSite('commons', 'commons')
	
	cat_main = catlib.Category(site,u'Kategoria:polski (indeks)')
	cat_gwary = catlib.Category(site, u'Kategoria:Polski_(dialekty_i_gwary)')
	cat_obce = catlib.Category(site, u'Kategoria:polski_-_terminy_obce_(indeks)')

	output_main = wikipedia.Page(site, u'Wikipedysta:AlkamidBot/wymowa')
	output_gwary = wikipedia.Page(site, u'Wikipedysta:AlkamidBot/wymowa/gwary')
	output_r = wikipedia.Page(site, u'Wikipedysta:AlkamidBot/wymowa/bez_r')
	output_stat = wikipedia.Page(site, u'Wikipedysta:AlkamidBot/wymowa/stat')
	
	lista_main = pagegenerators.CategorizedPageGenerator(cat_main)
	lista_gwary = pagegenerators.CategorizedPageGenerator(cat_gwary, recurse=True)
	lista_obce = pagegenerators.CategorizedPageGenerator(cat_obce)
	
	re_ipa = re.compile(u'\{\{język polski\}\}\) \=\=.*?\{\{IPA3.*?(\=|)', re.DOTALL)
	re_r = re.compile(u'.*r([^z]|$).*')
	
	final = u''
	r = u''
	
	lista = []
	lista_gwary1 = []
	lista_gwary2 = []
	lista_obce1 = []
	lista_obce2 = []
	lista_ipa = []
	lista_wielkie = []
	lista_male = []
	outputPopular = u''
	count_jest = 0
	count_brak = 0
	count_all = 0
		
	for a in lista_gwary:
		lista_gwary1.append(a.title())
	for b in lista_obce:
		lista_obce1.append(b.title())


	for page in lista_main:

		try:
			wikipedia.ImagePage(site, u'Pl-%s.ogg' % page.title()).fileIsOnCommons()
		except wikipedia.NoPage:
			try:
				wikipedia.ImagePage(site, u'Pl-%s.OGG' % page.title()).fileIsOnCommons()
			except wikipedia.NoPage:
				if page.title() in lista_gwary1:
					lista_gwary2.append(page.title())
				else:
					if page.title() in lista_przest:
						lista_przest2.append(page.title())
					else:
						if page.title() in lista_obce1:
							lista_obce2.append(page.title())
						else:
							s_ipa = re.search(re_ipa, page.get())
							if s_ipa == None:
								lista_ipa.append(page.title())
							else:
								lista.append(page.title())
				count_brak = count_brak + 1
			else:
				count_jest = count_jest + 1
		else:
			count_jest = count_jest + 1
		count_all = count_all + 1

			
	for a in lista:	
		if a[0].isupper():
			lista_wielkie.append(a)
		else:
			lista_male.append(a)
			
	for a in popularList:
		if a in lista:
			outputPopular += u'\n[[%s]]' % a
		
	data = datetime.datetime.now() + datetime.timedelta(hours=1)
	data1 = data.strftime("Ostatnia aktualizacja: %Y-%m-%d, %H:%M:%S")
	
	final = final + data1
	final += u'\n= najczęściej odwiedzane ='
	final += outputPopular
	final = final + u'\n= wielka litera ='
	
	for b in lista_wielkie:
		final = final + u'\n[[%s]]' % b
		
	final = final + u'\n= mała litera ='
	
	for c in lista_male:
		final = final +  u'\n[[%s]]' % c
		
	final_gw = data1 + u'\n= gwary ='
	
	for d in lista_gwary2:
		final_gw = final_gw +  u'\n[[%s]]' % d
		
	final_gw += u'\n= przestarzałe ='
	
	for d in lista_przest2:
		final_gw += u'\n[[%s]]' % d
	
	final = final + u'\n= wyraz obcy w języku polskim ='
	
	for e in lista_obce2:
		final = final +  u'\n[[%s]]' % e
	
	final = final + u'\n= nieznalezione IPA='
	
	for f in lista_ipa:
		final = final +  u'\n[[%s]]' % f

	
	final = final + u'\n: Licznik istniejących: %d' % count_jest
	
	
	#print final
	output_main.put(final, comment = u'Aktualizacja listy', botflag=False)
	if (len(output_gwary.get()) != len(final_gw)):
		output_gwary.put(final_gw, comment = u'Aktualizacja listy')
	
	
	re_po = re.compile(u'zmiana procentowa\n\|-(.*)', re.DOTALL)
	s_po = re.search(re_po, output_stat.get())
	re_proc = re.compile(u'zmiana procentowa\n\|-\n\|.*?\n\|.*?\n\| (.*?)\n')
	s_proc = re.search(re_proc, output_stat.get())
	proc_old = float(s_proc.group(1))
	proc = round(count_jest*100.00/count_all, 1)
	stat = u'{| class="wikitable" style="text-align: center;"\n|-\n! data\n! istniejące\n! % istniejących\n! zmiana procentowa\n|-'
	stat = stat + u'\n| %s\n| %d\n| %.1f\n| ' % ((datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d"), count_jest, proc)
	if (proc-proc_old) < 0:
		stat = stat + u'style="background: #FF927D;" | '
	elif (proc-proc_old) > 0:
		stat = stat + u'style="background: #00E070;" | +'
	stat = stat + u'%.1f\n|-' % (proc-proc_old)	
	stat = stat + s_po.group(1)
	
	if (proc-proc_old != 0):
		output_stat.put(stat, comment = u'Aktualizacja tabeli')
	
	for a in lista_male:
		if re.search(re_r, a) == None:
			r = r + u'\n[[%s]]' % a
	
	#print r		
	output_r.put(r, comment = u'Aktualizacja listy słów bez litery r')

if __name__ == '__main__':
    try:
        main()
    finally:
        wikipedia.stopme()
