# -*- coding: utf-8 -*-
"""new.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hpQ90o69i2qW03nC_vwJUznHc2QALBFk
"""

import json

json_data=open("drive/My Drive/yo_docs/slovari/json/all_yo_2.json")
djson=json.load(json_data)
slovar = dict(djson)
print(slovar)

from google.colab import drive
drive.mount('/content/drive')

txt = 'почему я не пошёл домой сегодня вечером? меня же дома ждет мама и моя микроволновка не чинена. на столе стоит протекшая банка сгущёнки'
#text1=text.read()
spl_text=txt.lower().split(" ")
pre_text = []
znaki=[",","/",".","'",'"',"&","!","?",":",";","«","»"]
for word in spl_text:
  for z in znaki:
    if z in word:
      word = word.replace(z, "")
  pre_text.append(word)
print(pre_text)

!pip install spacy-udpipe

!pip install pymorphy2

import spacy_udpipe

spacy_udpipe.download("ru")
nlp = spacy_udpipe.load("ru")

text = "на столе стоит протекшая банка"
doc = nlp(text)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_)

d = nlp(txt)

yo_true = 0
yo_missed = 0
tags = {'ADJS': 'ADJ', 'ADJF': 'ADJ', 'PRTF': 'VERB', 'PRTS': 'VERB', 'NOUN': 'NOUN'}
ts = []

for i in pre_text:
  if 'ё' in str(i):
    yo_true += 1
  else:
    if 'е' in str(i):
      if i in slovar.keys():
        if slovar.get(i)[0] == 0:
          yo_missed += 1
        else:
          for token in d:
            if token.text == i:
              k = token.pos_ 
          for item in slovar.get(i)[1::2]:
            for h in tags.keys():
              if h in item.split(',')[0]:
                ts.append(str(tags.get(h)))
          ind = ts.index(str(k))
          indexx = slovar.get(i).index(slovar.get(i)[1::2].pop(ind))
          ts.clear()
          if slovar.get(i)[indexx+1] == 'ё':
            yo_missed += 1
          else:
              pass
      else:
        pass
    else:
      pass

print ("слова, написанные с ё:", yo_true, "слова, в которых не хватает буквы ё:", yo_missed)