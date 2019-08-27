#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import pprint
import sys
import logging
import argparse

import numpy as np
import pandas as pd

pgm_ver = '0.0.1-alpha'

स्वर = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ', 'ए', 'ऐ', 'ओ', 'औ', 'अं', 'अः']
#स्वरमात्रा= [' ', 'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॢ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः']
स्वरमात्रा= {' ':'अ', 'ा':'आ', 'ि':'इ', 'ी':'ई', 'ु':'उ', 'ू':'ऊ', 'ृ':'ऋ', 'ॄ':'ॠ', 'ॢ':'ऌ', 'े':'ए', 'ै':'ऐ', 'ो':'ओ', 'ौ':'औ', 'ं':'अं', 'ः':'अः'}

व्यञ्जन = list('कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह')

कु =list('कखगघङ')
चु =list('चछजझञ') 
टु =list('टठडढण')
तु =list('तथदधन')
पु = list('पफबभम')
रकार = 'र'
ञिटुडवः = ('टु', 'डु', 'ञि')
षत्वनिषेध = ('ष्वस्कँ॒', 'ष्ठिवुँ')

initial_dhatus = ('भू', 'एधँ॒', 'स्पर्धँ॒', 'गाधृँ॒', 'बाधृँ॒', 'नाधृँ॒', 'नाथृँ॒', 'दधँ॒', 'स्कुदिँ॒', 'श्विदिँ॒', 'वदिँ॒', 'भिदिर्', 'च्युतिँर्',  'दासृँ॑','ञिक्ष्विदाँ', 'ष्वस्कँ॒', 'ष्ठिवुँ', "ष्ठा॒", "णदँ", "कुर्द॒")
#initial_dhatus = ('एधँ॒', 'स्पर्धँ॒', 'गाधृँ॒', 'बाधृँ॒', 'नाधृँ॒', 'नाथृँ॒', 'दधँ॒', 'स्कुदिँ॒', 'श्विदिँ॒', 'वदिँ॒')

अनुदात्त = list("एधँ॒")[-1]
स्वरित = list('सृँ॑')[-1]
अनुनासिक = list("एधँ॒")[-2]
हलन्त = list('क्')[-1]
विसर्ग = list('कः')[-1]
# Lets rename project as verb form generation of bhvadi gana lat lakar using pushpa dixit method.
# Initial DS to have a demo run, later so many components will be auto generated as pit, haladi / achadi etc.
#                                           pratyaya, after it, type of pratyaya, beginign, 
तिङ्_प्रत्यय = {'अदन्त':{'सार्वधातुक':{'लट्':{'परस्मैपदी':{'तिप्':('ति', 'पित्', 'हलादि', ), 
                                           'तस्':('तः', 'अपित्', 'हलादि', ),
                                           'झि':('अन्ति', 'अपित्', 'अजादि', ), 
                                           'सिप्':('सि', 'पित्', 'हलादि', ), 
                                           'थस्':('थः', 'अपित्', 'हलादि', ), 
                                           'थ':('थ', 'अपित्', 'हलादि', ),
                                           'मिप्':('मि','पित्', 'हलादि', ),
                                           'वस्':('वः','अपित्', 'हलादि', ),
                                           'मस्':('मः', 'अपित्', 'हलादि', )
                                          },
                                 'आत्मनेपदी':{'त':('ते', 'अपित्', 'हलादि', ), 
                                            'आताम्':('इते', 'अपित्', 'अजादि', ), 
                                            'झ':('अन्ते', 'अपित्', 'अजादि', ), 
                                            'थास्':('से', 'अपित्', 'हलादि', ), 
                                            'आथाम्':('इथे', 'अपित्', 'अजादि', ), 
                                            'ध्वम्':('ध्वे', 'अपित्', 'हलादि', ), 
                                            'इट्':('ए', 'अपित्', 'अजादि', ), 
                                            'वहि':('वहे', 'अपित्', 'हलादि', ), 
                                            'महिङ्':('महे', 'अपित्', 'हलादि', ),
                                          },
                                              },
 # Below Pratyayas apit and halidi etc marker is wrong just copy of lat.
                               'लङ्':{'परस्मैपदी':{'तिप्':('त्', 'पित्', 'हलादि', ),
                                           'तस्':('ताम्', 'अपित्', 'हलादि', ),
                                           'झि':('अन्', 'अपित्', 'अजादि', ), 
                                           'सिप्':(विसर्ग, 'पित्', 'हलादि', ), 
                                           'थस्':('तम्', 'अपित्', 'हलादि', ), 
                                           'थ':('त', 'अपित्', 'हलादि', ),
                                           'मिप्':('अम्','पित्', 'हलादि', ),
                                           'वस्':('व','अपित्', 'हलादि', ),
                                           'मस्':('म', 'अपित्', 'हलादि', )
                                          },
                                 'आत्मनेपदी':{'त':('त', 'अपित्', 'हलादि', ), 
                                            'आताम्':('इताम्', 'अपित्', 'अजादि', ), 
                                            'झ':('अन्त', 'अपित्', 'अजादि', ), 
                                            'थास्':('थाः', 'अपित्', 'हलादि', ), 
                                            'आथाम्':('इथाम्', 'अपित्', 'अजादि', ), 
                                            'ध्वम्':('ध्वम्', 'अपित्', 'हलादि', ), 
                                            'इट्':('इ', 'अपित्', 'अजादि', ), 
                                            'वहि':('वहि', 'अपित्', 'हलादि', ), 
                                            'महिङ्':('महि', 'अपित्', 'हलादि', ),
                                          },
                                              },
                               'विधिलिङ्ग्':{'परस्मैपदी':{'तिप्':('इत्', 'पित्', 'हलादि', ), 
                                           'तस्':('इताम्', 'अपित्', 'हलादि', ),
                                           'झि':('ईयुः', 'अपित्', 'अजादि', ), 
                                           'सिप्':('इः', 'पित्', 'हलादि', ), 
                                           'थस्':('इतम्', 'अपित्', 'हलादि', ), 
                                           'थ':('इत', 'अपित्', 'हलादि', ),
                                           'मिप्':('इयम्','पित्', 'हलादि', ),
                                           'वस्':('इव','अपित्', 'हलादि', ),
                                           'मस्':('इम', 'अपित्', 'हलादि', )
                                          },
                                 'आत्मनेपदी':{'त':('ईत', 'अपित्', 'हलादि', ), 
                                            'आताम्':('ईयाताम्', 'अपित्', 'अजादि', ), 
                                            'झ':('ईरन्', 'अपित्', 'अजादि', ), 
                                            'थास्':('ईथाः', 'अपित्', 'हलादि', ), 
                                            'आथाम्':('ईयाथाम्', 'अपित्', 'अजादि', ), 
                                            'ध्वम्':('ईध्वम्', 'अपित्', 'हलादि', ), 
                                            'इट्':('ईय', 'अपित्', 'अजादि', ), 
                                            'वहि':('ईवहि', 'अपित्', 'हलादि', ), 
                                            'महिङ्':('ईमहि', 'अपित्', 'हलादि', ),
                                          },
                                              },
                               'लोट्':{'परस्मैपदी':{'तिप्':('तु', 'पित्', 'हलादि', ), 
                                           'तस्':('ताम् ', 'अपित्', 'हलादि', ),
                                           'झि':('अन्तु', 'अपित्', 'अजादि', ), 
                                           'सिप्':('', 'पित्', 'हलादि', ), 
                                           'थस्':('तम्', 'अपित्', 'हलादि', ), 
                                           'थ':('त', 'अपित्', 'हलादि', ),
                                           'मिप्':('आनि','पित्', 'हलादि', ),
                                           'वस्':('आव','अपित्', 'हलादि', ),
                                           'मस्':('आम', 'अपित्', 'हलादि', )
                                          },
                                 'आत्मनेपदी':{'त':('ताम्', 'अपित्', 'हलादि', ), 
                                            'आताम्':('इताम्', 'अपित्', 'अजादि', ), 
                                            'झ':('अन्ताम्', 'अपित्', 'अजादि', ), 
                                            'थास्':('स्व', 'अपित्', 'हलादि', ), 
                                            'आथाम्':('इथाम्', 'अपित्', 'अजादि', ), 
                                            'ध्वम्':('ध्वम्', 'अपित्', 'हलादि', ), 
                                            'इट्':('ऐ', 'अपित्', 'अजादि', ), 
                                            'वहि':('आवहै', 'अपित्', 'हलादि', ), 
                                            'महिङ्':('आमहै', 'अपित्', 'हलादि', ),
                                          },
	                                      },
                          },
              },
    }
         
सार्वधातुक_लकार् = ('लट्', 'लोट्', 'लङ्', 'विधिलिङ्ग्')

विकरण_प्रत्यय = {'सार्वधातुक':{'भ्वादि':('शप्', 'अ', 'पित्', 'अजादि', ),
                         'दिवादि':('श्यन्', 'य','अपित्', 'हलादि',),
                         'तुदादि':('श', 'अ','अपित्', 'अजादि',),
                         'चुरादि':('शप्', 'अ','पित्', 'अजादि',),
                        },
             }
# If in list there are two componments it means first is for parasmaipadi and 
# second for atmanepadi otherwise if only one is there in case of ubhayapadi 
# dhatu same is applied to both.
भ्वादिगणः_विशेष_धातवः = {'गुह्':('गूह्',''), 'गुप्': ('गोपाय्',''), 'धूप्': ('धूपाय्',''),
                     'पण्': ('पणाय्','पण्'), 'पन्': ('पनाय्',''), 'कम्': ('कामय्',''),
                     'गुप्' :('गोपय्', 'जुगुप्स्'), 'तिज्' :('तेजय्', 'तितिक्श्'), 'कित्' :('चिकित्स्', 'केतय्'),
                     'मान्' : ('मानय्', 'मीमांस्'), 'बध्': ('बाधय्', 'बीभत्स्'), 'दान्': ('दानय्', 'दिदांस्'),
                     'शान्': ('शिशांस्','') , 'भ्राश्': ('भ्लाश्य्', 'भ्लाश्'), 'गम्': ('गच्छ्',''), 'यम्': ('यच्छ्',''),
                     'पा': ('पिब्',''), 'घ्रा' :('जिघ्र्',''), 'ध्मा' :('धम्',''), 'स्था' :('तिष्ठ्',''),
                     'म्ना' :('मन्',''), 'दा':('यच्छ्',''), 'दृश्': ('पश्य्',''), 'ऋ': ('ऋच्छ्',''),
                     'सृ': ('धाव्',''), 'शद्': ('शीय्',''), 'सद्':('सीद्',''), 'दंश्':('दश्',''),
                     'स्वञ्ज्':('स्वज्',''), 'सञ्ज्':('सज्',''), 'रञ्ज्':('रज्',''), 'जभ्': ('जम्भ्',''),
                     'चम्': ('आचाम्',''),  'ष्ठिव्':( 'ष्ठीव्',''),
                    } 

guna = {'अ':'', 'ए':list('वे')[-1], 'ओ':list('ओ')[-1]}
यञादि = ('व', 'म')

def हलन्त्यम्(धातुः):
   it_removed_word = धातुः
   if (धातुः[-1] == हलन्त) and (धातुः[-2] in व्यञ्जन):
      logging.debug("हलन्त्यम् applies")
      logging.debug("Checking for इर इत्संज्ञा वाच्या")
      if (धातुः[-2] == रकार) and (धातुः[-3] == list('कि')[-1]):
         logging.debug("Applying इर इत्संज्ञा वाच्या")
         del it_removed_word[-3:]
         it_removed_word.insert(len(it_removed_word), हलन्त)
         return(it_removed_word)

      if 'ङ' in it_removed_word[-2:]:
         logging.debug("In halyantam: Atmanepadam", ''.join(it_removed_word))
      elif 'ञ' in it_removed_word[-2:]:
         print("In halyantam: Ubhayapadi", ''.join(it_removed_word))

      del it_removed_word[-2:]
      return(it_removed_word)
   logging.debug("हलन्त्यम् doesnt apply")
   return(it_removed_word)

def उपदेशेऽजनुनासिक(धातुः):
   global parsed_dhatu_db
   it_removed_word = धातुः
   it_comp = []

   # Check last letter may be anudatta or svarita
   # As of now just removing later we will register atmanepadi / ubhaya padi etc.
   if it_removed_word[-1] == अनुदात्त:
      logging.debug("अनुदात्त धातु.")
      it_comp.insert(0, अनुदात्त)
      #dhatu_type = 'आत्मनेपदी' 
      del it_removed_word[-1:]
   elif it_removed_word[-1] == स्वरित:
      logging.debug("स्वरित धातु")
      it_comp.insert(0, स्वरित)
      #dhatu_type = 'उभयपदी'
      del it_removed_word[-1:]
   else:
      logging.debug("उदात्त धातु")
      #dhatu_type = 'परस्मैपदी'
   # Dirty hack for now, will be re-addressed during optimization review.
   # Still need to do for matra.
   if (len(it_removed_word) >= 2) and (it_removed_word[0] in स्वर) and (it_removed_word[1] == अनुनासिक):
      logging.debug("removing initial anunasika aca")
      del it_removed_word[0]
      del it_removed_word[0]
   # check for अनुनासिक
   if it_removed_word[-1] == अनुनासिक:
      logging.debug("अनुनासिक found")
      it_comp.insert(0, अनुनासिक)
      del it_removed_word[-1:]
      if it_removed_word[-1] in स्वरमात्रा.keys():
         logging.debug("मात्रा found" )
         #logging.debug(स्वरमात्रा[it_removed_word[-1]])
         #logging.debug("{} {}", len(it_removed_word), स्वरमात्रा[it_removed_word[-1]])
         it_comp.insert(0, स्वरमात्रा[it_removed_word[-1]])
         del it_removed_word[-1:]
         it_removed_word.insert(len(it_removed_word), हलन्त)
      else:
         logging.debug("A व्यञ्जन following add हलन्त")
         it_comp.insert(0, स्वर[0])
         it_removed_word.insert(len(it_removed_word), हलन्त)
   # check for preceding matra or व्यञ्जन
   # if matra then add respective स्वर and add halant after व्यञ्जन or at place of matra.
   # if not matra then insert हलन्त after व्यञ्जन.
   #TODO: Below line is just for test, will optimize later once it works for all the cases., later make it numagama function.
   #TODO: Below code is causing numagama in च्युतिँर् also where in excel it is not there.
   if 'इ' in it_comp:
      it_removed_word = इदितो_नुम्_धातोः(it_removed_word)
   
   #FIXME: some list is empty and since we are in acha it routine only we are checking first letter to be in svara.  
   dhatu_type = 'परस्मैपदी'
   if len(it_comp) and it_comp[0] in स्वर:
      #अनुदात्तङित_आत्मनेपदम्  for nit we need to do it in halyantam.
      if अनुदात्त in it_comp:
         #print("Dhatu: ", ''.join(it_removed_word), "is aatmanepadi.")
         if it_comp[it_comp.index(अनुदात्त)-2] in स्वर:
            dhatu_type = 'आत्मनेपदी' 

      # स्वरितञितः_कर्त्रभिप्राये_क्रियाफले  for nit we need to test in other modules.
      elif स्वरित in it_comp:
         #print("Dhatu: ", ''.join(it_removed_word), "is ubhayapadi.")
         if it_comp[it_comp.index(स्वरित)-2] in स्वर:
            dhatu_type = 'उभयपदी'
         
      #TODO: Put all in parasmaipadi by default.
      #else:
         #print("Dhatu: ", ''.join(it_removed_word), "is parasmaipadi.")
         

   return(it_removed_word, dhatu_type)

def आदिर्ञिटुडवः(धातुः):
   it_removed_word = धातुः
   #if len(it_removed_word) < 3:
   #   return(it_removed_word) # bhu case it is too small
   if ''.join(it_removed_word[0:2]) in ञिटुडवः:
      logging.debug('आदिर्ञिटुडवः applies.')
      del it_removed_word[:2]
   else:
      logging.debug('आदिर्ञिटुडवः doesnt apply.')
   return(it_removed_word)

def धात्वादेः_षः_सः(धातुः):
   it_removed_word = धातुः
   #if len(it_removed_word) < 3:
   #   return(it_removed_word) # bhu case it is too small
   # TODO: Remember original word also as we need to match with that. may be we can keep in one DS.
   if ''.join(it_removed_word) not in षत्वनिषेध:
      logging.debug("Came in धात्वादेः षः सः case")
      #if ''.join(it_removed_word[0:2]) == 'ष्':
      if it_removed_word[0] == 'ष':
         logging.debug("Came in धात्वादेः षः सः case")
         if (len(it_removed_word) >= 3) and (it_removed_word[2] in टु):
            logging.debug("धात्वादेः षः सः - next word also need to be changed.")
            it_removed_word[2] = तु[टु.index(it_removed_word[2])]
         it_removed_word[0] = 'स'
   return(it_removed_word)

def णो_नः(धातुः):
   logging.debug("Came in णो नः case")
   it_removed_word = धातुः
   if it_removed_word[0] == 'ण':
      logging.debug('णो नः applies.')
      it_removed_word[0] = 'न'
   else:
      logging.debug('णो नः doesnt apply.')
   return(it_removed_word)

def varga_anunashik(letter):
   if letter in कु:
      return(कु[4])
   if letter in चु:
      return(चु[4])
   if letter in टु:
      return(टु[4])
   if letter in तु:
      return(तु[4])
   if letter in पु:
      return(पु[4])
   return(letter)
#'न्'
def इदितो_नुम्_धातोः(धातुः):
   logging.debug("Came in इदितो नुम् धातोः case")
   if (धातुः[-1] == हलन्त)  and (धातुः[-3] in व्यञ्जन):
           धातुः.insert(-2, varga_anunashik(धातुः[-2]))
           धातुः.insert(-2, हलन्त)
   if (धातुः[-1] == हलन्त)  and ((धातुः[-3] in स्वर) or (धातुः[-3] in स्वरमात्रा)):
           धातुः.insert(-2, varga_anunashik(धातुः[-2]))
           धातुः.insert(-2, हलन्त)
   return(धातुः)

def उपधायां_च(धातुः):
   logging.debug("Came in उपधायां च case")
   if len(धातुः) < 3:
      return(धातुः) # bhu case it is too small

   if धातुः[-1] == हलन्त:
         उपधा = -3
   else:
         उपधा = -2
   if धातुः[उपधा] == हलन्त and धातुः[उपधा-1] == 'र':
      if धातुः[उपधा-2] == 'ि':
              धातुः[उपधा-2] = 'ी'
      if धातुः[उपधा-2] == 'ु':
              धातुः[उपधा-2] = 'ू'
   return(धातुः)

def add_vikaran_to_dhatu(dhatu, gana, padi):
   vikaran = विकरण_प्रत्यय['सार्वधातुक'][gana][1]
   if dhatu in भ्वादिगणः_विशेष_धातवः.keys():
      logging.debug("This is a special dhatu..", len(भ्वादिगणः_विशेष_धातवः[dhatu]))
      if padi == 'आत्मनेपदी': # Ubhayapadi should call this function twice with each type once
         dhatu = भ्वादिगणः_विशेष_धातवः[dhatu][1]
      else:
         dhatu = भ्वादिगणः_विशेष_धातवः[dhatu][0]

   if ((len(dhatu) >= 3) and (dhatu[-1] == list('प्')[-1]) and (dhatu[-3] == 'ि')): # Laghu ik in upadha
      logging.debug("came in laghu igupadha dhatu")
      new = list(dhatu)
      new[-3] = 'े'
      dhatu = ''.join(new)
      return dhatu[:-1]

   if ((len(dhatu) >= 3) and (dhatu[-1] == list('प्')[-1]) and (dhatu[-3] == list('पु')[-1])): # Laghu u in upadha
      logging.debug("came in laghu ugupadha dhatu")
      new = list(dhatu)
      new[-3] = list('पो')[-1]
      dhatu = ''.join(new)
      return dhatu[:-1]

   if ((len(dhatu) >= 3) and (dhatu[-1] == list('प्')[-1]) and (dhatu[-3] == list('पृ')[-1])): # Laghu u in upadha
      logging.debug("came in laghu riupadha dhatu")
      new = list(dhatu)
      new[-3] = 'र्'
      dhatu = ''.join(new)
      return dhatu[:-1]

   if (dhatu[-1] == list('प्')[-1]) and (vikaran == 'अ'):
      return dhatu[:-1]
   if ((dhatu[-1] == list('रि')[-1]) or (dhatu[-1] == list('री')[-1]) or (dhatu[-1] == list('वे')[-1])) and (vikaran == 'अ'):
      return dhatu[:-1]+'य' # Guna will convert e or EE to ae and then ae+a will conver it to aya and then only ya additional
   if ((dhatu[-1] == list('कु')[-1]) or (dhatu[-1] == list('कू')[-1]) or (dhatu[-1] == list('ओ')[-1])) and (vikaran == 'अ'):
      return dhatu[:-1]+'व'
   if ((dhatu[-1] == list('धृ')[-1]) or (dhatu[-1] == list('झॄ')[-1])) and (vikaran == 'अ'):
      return dhatu[:-1]+'र'
   if ((dhatu[-1] == list('वै')[-1])) and (vikaran == 'अ'):
      return dhatu[:-1]+'ा' + 'य'
   if ((dhatu[-1] == list('वौ')[-1])) and (vikaran == 'अ'):
      return dhatu[:-1]+'ा' + 'व'

   logging.debug("None cases matched.", dhatu)
 
   return dhatu+vikaran

def अतो_गुणे_6_1_96(dhatu, pratyaya):
   if len(pratyaya) and pratyaya[0] in guna.keys():
      return dhatu+guna[pratyaya[0]], pratyaya[1:]
   return dhatu, pratyaya

def अतो_दीर्घो_यञि_7_3_101(dhatu, pratyaya):
   if not pratyaya:
      return dhatu
   if pratyaya[0] in यञादि:
      return dhatu+list('सा')[-1]
   return dhatu

def print_roopa(roopa_lst):
   rpa = np.array(roopa_lst)
   df = pd.DataFrame(np.split(rpa, 3), columns=['एकवचन','द्विवचन','बहुवचन'], index=['प्रथम पुरुषः', 'मध्यं पुरुषः',  'उत्तम पुरुषः'])
   print(df.to_string())

def gen_verb_forms(dhatu_w_vakaran, lakar, padi):      
   #'अदन्त':{'सार्वधातुक':{'लट्':{'परस्मैपदी'
   counter = 0
   roopa_lst = []
   for i in तिङ्_प्रत्यय['अदन्त']['सार्वधातुक'][lakar][padi].keys():
      counter += 1
      local_dhatu = dhatu_w_vakaran
      local_pratyaya = तिङ्_प्रत्यय['अदन्त']['सार्वधातुक'][lakar][padi][i][0]
      roopa = local_dhatu+local_pratyaya
      if local_dhatu[-1] in व्यञ्जन: # Sarvadhatuk Adant dhatu
         #logging.debug("Calling ato guna Dhatu and pratyaya is: ", local_dhatu, local_pratyaya)
         local_dhatu, local_pratyaya = अतो_गुणे_6_1_96(dhatu_w_vakaran, local_pratyaya)
         #logging.debug("Dhatu and pratyaya is: ", local_dhatu, local_pratyaya)
         local_dhatu = अतो_दीर्घो_यञि_7_3_101(local_dhatu, तिङ्_प्रत्यय['अदन्त']['सार्वधातुक'][lakar][padi][i][0])

         if local_pratyaya and local_pratyaya[0] in स्वर:
            if local_pratyaya[0] == 'इ' or local_pratyaya[0] == 'ई':
               roopa = local_dhatu+list('के')[-1]+local_pratyaya[1:]
            if local_pratyaya[0] == 'आ':
               roopa = local_dhatu+list('सा')[-1]+local_pratyaya[1:]
            if local_pratyaya[0] == 'ऐ':
               roopa = local_dhatu+list('लै')[-1]+local_pratyaya[1:]

         else:
            roopa = local_dhatu+local_pratyaya
      if lakar == 'लङ्':
         # आडजादीनाम्_6.4.72 आटश्च_6.1.90
         if roopa[0] == 'अ':
            roopa = 'आ'+roopa[1:]   
         elif roopa[0] == 'इ' or roopa[0] == 'ई':
            roopa = 'ऐ'+roopa[1:]   
         elif roopa[0] == 'उ' or roopa[0] == 'ऊ':
            roopa = 'औ'+roopa[1:]
         elif roopa[0] == 'ऋ' or roopa[0] == 'ॠ':
            roopa = 'आर्'+roopa[1:]
         elif roopa[0] == 'ए':
            roopa = 'ऐ'+roopa[1:]   
         elif roopa[0] == 'ओ':
            roopa = 'औ'+roopa[1:]
         else:
            roopa = 'अ'+roopa
           
      roopa_lst.append(roopa)
      #print(roopa, end ='   ')
      #if counter % 3 == 0:
      #   print()
   print('------------------------')
   print_roopa(roopa_lst)
   print('------------------------')

def call_verb_form_gen(dhatu, gana, dh_type, lakar):
   print("धातु -- ", dhatu, ", लकार --", lakar)
   if dhatu == 'उ':
      dhatu = 'अव्'
   dhatu_with_vikaran = add_vikaran_to_dhatu(dhatu, gana, dh_type)
   logging.debug(dhatu_with_vikaran)
   gen_verb_forms(dhatu_with_vikaran, lakar, dh_type)



#TODO: Keep all the its, starting from begining and end both ones.
# We are checking this as dict items are not in order they are defined 
# in other versions and causes tin pratyayas to be shifted.
try:
   assert sys.version_info >= (3, 6)
except:
   logging.error("Python 3.6 or onwards version needed to run this program")
   sys.exit()

parser = argparse.ArgumentParser(description='Verb form generator:\nVersion: %s.' % pgm_ver)
parser.add_argument('-अ', '--आर्धधातुक', action='store_true', help='Aardhdhatuak prattya.')
parser.add_argument('-स', '--सार्वधातुक', action='store_true', help='Sarvadhatuak prattya.')
parser.add_argument('-न', '--नामधातु', action='store_true', help='Naam dhatu.')
parser.add_argument('-v', '--verbose', type=int, choices=[1,2], help='Adjust verbocity level.')
parser.add_argument('word', nargs='?', help='niranubandh dhatu.')
args = parser.parse_args()

if not args.verbose:
    logging.basicConfig(level=logging.WARNING)
elif args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose == 2:
    logging.basicConfig(level=logging.DEBUG)

logging.info("Arguments to program status: \n %s" % args)

if not args.word:
   logging.error("Provide dhatu to generate forms. Exiting...")
   sys.exit(2)

if args.सार्वधातुक:
   logging.debug("Sarva")
   प्रत्यय = सार्वधातुक_लकार्
elif args.आर्धधातुक:
   logging.debug("Ardhadhatuk not implemented")
   प्रत्यय = ('')
   sys.exit(3)
elif args.नामधातु:
   logging.debug("Naamdhatu section")
else:
   logging.debug("Else")
   प्रत्यय = ('लट्',)
    
if args.नामधातु:
   print("In Naam dhatu")
   dhatu_l = args.word
   for ii in प्रत्यय:
      call_verb_form_gen(dhatu_l, 'भ्वादि', 'परस्मैपदी', ii)
   sys.exit(0)

dhatu_file = 'dhatu_list.json'

fieldnames = ('धातु', 'गण', 'कारक','पद', 'पाठ')

with open('dhatu-pata-short.csv', 'r', encoding = "utf8") as csvfile:
    reader = csv.DictReader(csvfile, fieldnames)
    rows = list(reader)

csvfile.close()
#print(rows)

#with open(dhatu_file, 'w', encoding = "utf8") as jsonfile:
#    json.dump(rows, jsonfile, ensure_ascii=False, indent=4,separators=(',', ':'))

parsed_dhatu_db = {}
dhatu_orig_list = []
dhatu_wo_it_list = []
diff = 0
same = 0

for each in range(0, len(rows)):
   if rows[each]['धातु'][0] == '#':
      logging.debug("Comment found.. continuing..")
      continue
   if rows[each]['गण'] != 'भ्वादि':
      logging.debug("Only भ्वादि गण supported as of now.")
      break
   dhatu = rows[each]['पाठ'].split(' ')[0]
   wo_it = rows[each]['धातु']
   
   parsed_dhatu_db[dhatu] = [dhatu, rows[each]['पाठ'], rows[each]['गण'],]

   logging.debug('*' * 80)
   #print(each, "Trying for: ", dhatu)
   dh_expen = हलन्त्यम्(list(dhatu))
   dh_expen, dh_type = उपदेशेऽजनुनासिक(dh_expen)
   parsed_dhatu_db[dhatu].append(dh_type)
   dh_expen = आदिर्ञिटुडवः(dh_expen)
   dh_expen = धात्वादेः_षः_सः(dh_expen)
   dh_expen = णो_नः(dh_expen)
   dh_expen = उपधायां_च(dh_expen)
   # TODO: Loop to figureout if more than one svara is there and remove. 
   if अनुदात्त in dh_expen:
      # remove anudatta
      del dh_expen[dh_expen.index(अनुदात्त)]
   if स्वरित in dh_expen:
      # remove anudatta
      del dh_expen[dh_expen.index(स्वरित)]
   
   final_dhatu = ''.join(dh_expen)
   logging.info(final_dhatu)

   parsed_dhatu_db[dhatu].append(final_dhatu)
   parsed_dhatu_db[final_dhatu] = parsed_dhatu_db[dhatu]
   if dhatu != final_dhatu: # Some dhatus will be same after it also so deleting w/o this check will delete entry itself.
      del parsed_dhatu_db[dhatu]   
   
   if ''.join(dh_expen) != wo_it:
      #print("Dhatu output differs- calculated - excel", final_dhatu, wo_it)
      diff += 1
      #input("enter any key to proceed")
   else:
      #print("Output matched for: ", wo_it)
      same += 1
   #print("Diff - same", diff, same)
   #dhatu_orig_list.append(rows[each]['पाठ'].split(' ')[0])
   #dhatu_wo_it_list.append(rows[each]['धातु'])
#print('*' * 80)
#pp = pprint.PrettyPrinter(indent=4)
#logging.debug(pp.pprint(parsed_dhatu_db))

logging.info(parsed_dhatu_db.keys())
#print(parsed_dhatu_db)
# TODO: Remove svara marker whereever it is present if it is not removed by it function.
# TODO: ट्वोँस्फूर्ज्  in this case anunashik acha is at the begining which also we need to do it.
# TODO: Program will take input as dhatu nirabandh and then generate forms as per its classification means
# if it is parasmai or aatmane or ubhaya. 

if args.word not in parsed_dhatu_db.keys():
   logging.error("Given dhatu is not handled. Exiting...")
   sys.exit(2)

logging.info(parsed_dhatu_db[args.word])

dhatu_l = args.word
logging.info(dhatu_l)


if dhatu_l in  parsed_dhatu_db.keys():
   print("Calling verb generate for: ", parsed_dhatu_db[dhatu_l], end='\n\n')
   for ii in प्रत्यय:
      if parsed_dhatu_db[dhatu_l][3] == 'उभयपदी':
         print("उभयपदी dhatu, roopas will be in both आत्मनेपदी and परस्मैपदी")
         call_verb_form_gen(dhatu_l, parsed_dhatu_db[dhatu_l][2], 'परस्मैपदी', ii)
         call_verb_form_gen(dhatu_l, parsed_dhatu_db[dhatu_l][2], 'आत्मनेपदी', ii)
      else:
         call_verb_form_gen(dhatu_l, parsed_dhatu_db[dhatu_l][2], parsed_dhatu_db[dhatu_l][3], ii)
else:
   logging.error("Dhatu %s not found", dhatu_l)

''' 
#Test case 
dhatu_l = ('पठ्', 'वन्द्',)# 'भू', 'गम्', 'धे', 'म्लै', 'धौ', 'चित्', 'चित्', 'मुद्', 'वृष्', 'मील्', 'मूष्', 'वद्',
           #'ज्रि', 'नी', 'प्लु', 'पू' , 'दे', 'गै', 'पै', 'जि', 'धृ', 'दा', 'पण्', 'सृ', 'वन्द्', 'लिख्',
          #)
# Not working , 'लिख्', 

#dhatu_l = ('चित्', 'मुद्', 'वृष्')
#gana = 'भ्वादि'
#gana = 'दिवादि'
#'लट्'

for i in dhatu_l:
   for ii in सार्वधातुक_लकार्:
      print("For: ", ii)
      if i in  parsed_dhatu_db.keys():
         #print("Calling verb generate for: ", parsed_dhatu_db[i])
         call_verb_form_gen(i, parsed_dhatu_db[i][2], parsed_dhatu_db[i][3], ii)
      else:
         logging.error("Dhatu %s not found", i)
'''

#TODO  'इख्' in all forms becomes aekhati but we are getting only in lang.
#TODO: add nit etc also in detecting atmanepadi parasmai.
#TODO: Add logic to generate it/set/wait in dhatu DS, make a proper DS with all fields 
# and load at init time.
# ऋज् in all forms starting with a but we are doing only in lang
