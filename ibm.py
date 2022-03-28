# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 17:32:57 2020

@author: Vishal
"""

import json 
from os.path import join, dirname 
from ibm_watson import SpeechToTextV1 
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
from punctuator import Punctuator

p = Punctuator('Demo-Europarl-EN.pcl')
# Insert API Key in place of  
# 'YOUR UNIQUE API KEY' 
authenticator = IAMAuthenticator('{IBM CREDENTIALS KEY HERE}')  
service = SpeechToTextV1(authenticator = authenticator) 
   
#Insert URL in place of 'API_URL'  
service.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/{API KEY HERE}') 

# Insert local mp3 file path in 
# place of 'LOCAL FILE PATH'  
with open(join(dirname('__file__'), r'm1.wav'), 'rb') as audio_file: 
      
        dic = json.loads( 
                json.dumps( 
                    service.recognize( 
                        audio=audio_file, 
                        content_type='audio/wav',    
                        model='en-US_NarrowbandModel', 
                        speaker_labels=True).get_result(),
                        indent=2)) 

with open(join(dirname('__file__'), r'm1.wav'), 'rb') as audio_file: 
      
        dicn = json.loads( 
                json.dumps( 
                    service.recognize( 
                        audio=audio_file, 
                        content_type='audio/wav',    
                        model='en-US_NarrowbandModel', 
                        speaker_labels=True).get_result(),
                        indent=2))
        
# Stores the transcribed text
#dicn=dic

str0 = "" 
str1 = []
str2 = []

# list = ""
#welp=dic.get('results')
#wel=dic.get('results')
  
       
while bool(dicn.get('results')): 
    str1 = dicn.get('results').pop().get('alternatives').pop().get('timestamps')
    str2.append(str1)
    
str2.reverse()

welp1=dic.get('speaker_labels')

#wel1=dicn.get('speaker_labels')

#while bool(welp): 
#    str = welp.pop().get('alternatives').pop().get('transcript')+str[:] 
 
#while bool(wel): 
#    str1 = wel.pop().get('alternatives').pop().get('timestamps')
    
# print(str)
# print(str1)
# print(str1[0][1])
# print(str1[0][0])
# print(welp1[0]['from'])
# print(welp1[0]['speaker'])
# print(str2[1][0][1])
# print(len(welp1))

flat_list = []
for sublist in str2:
    for item in sublist:
        flat_list.append(item)

speak1=""
speak2=""

# speak3=""
# speak4=""

for x in range(len(welp1)):
    if welp1[x]['speaker']==1:
        speak1=speak1[:]+" "+flat_list[x][0]
        
    else:
        speak2=speak2[:]+" "+flat_list[x][0]
    
# for x in range(len(welp1)):
#     if welp1[x]['speaker']==1:
#         speak1=speak1[:]+" "+flat_list[x][0]
#     else:
#         break
    
# for x in range(len(welp1)):
#     if welp1[x]['speaker'] > 1:
#         speak2=speak2[:]+" "+flat_list[x][0]
#     else:
#         break

# for x in range(len(welp1)):
#     if welp1[x]['speaker']==1:
#         speak3=speak3[:]+" "+flat_list[x][0]
#     else:
#         break

# for x in range(len(welp1)):
#     if welp1[x]['speaker']==2:
#         speak4=speak4[:]+" "+flat_list[x][0]
#     else:
#         break

while bool(dic.get('results')): 
    str0 = dic.get('results').pop().get('alternatives').pop().get('transcript')+str0[:] 

print("\n\nFull Speech Without Punctuation : ",str0)

s=p.punctuate(str0)
print("\n\nFull Speech With Punctuation : ",s)

f=open("AA_FINAL_SPEECH_TO_TEXT.txt","w+")
f.write(s)
f.close()

s1=p.punctuate(speak1)
s2=p.punctuate(speak2)
print("\n\nSpeaker 1 :",s1)  
print("\n\nSpeaker 2 :",s2)    
   
f=open("CC_SPEAKER_1_IBM_DIARIZITAION.txt","w+")
f.write(s1)
f.close()

f=open("CC_SPEAKER_2_IBM_DIARIZITAION.txt","w+")
f.write(s2)
f.close()

# print("Speaker 1 :",speak3)
# print("Speaker 2 :",speak4)

#-------------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 16:33:42 2020

@author: Vishal
"""
import string
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
import en_core_web_sm

#creating nlp object
nlp = spacy.load("en_core_web_sm")

#reading text file 
with open("AA_FINAL_SPEECH_TO_TEXT.txt", "r", encoding="utf-8") as f:

        text = " ".join(f.readlines())

doc = nlp(text)

#priting word and part of speech of the word 
print([(w.text, w.pos_) for w in doc])
print(doc)

#creating lower case characters 
corpus=[]

for sent in doc.sents:

   c=sent.text.lower()
   corpus.append(c)

print(corpus)

#count total number of words 
cv = CountVectorizer()
corpus_a=cv.fit(corpus)

#unique word in text

word_list = cv.get_feature_names()
print(word_list)

#stopword in englishlanguage 
stop_words=list(STOP_WORDS)
print(stop_words)

# Create our list of punctuation marks
punctuation = string.punctuation

#counting occurance of a word in text
word_frequencies= {}

for word in doc:

  if word.text.lower() not in stop_words:

    if word.text.lower() not in punctuation:

      if word.text not in word_frequencies.keys():
        word_frequencies[word.text]=1

      else:
        word_frequencies[word.text] +=1

word_frequencies

#calculating higher frequency (Normalize frequency)
val=sorted(word_frequencies.values())

higher_word_frequencies = [word for word,freq in word_frequencies.items()if freq in val[-3:]]

print("\nWords with higher frequencies: ", higher_word_frequencies)

# gets relative frequency of words
higher_frequency = val[-1]

for word in word_frequencies.keys():  

  word_frequencies[word] = (word_frequencies[word]/higher_frequency)

#word_frequencies now
print(word_frequencies)

#Ranking Sentences 
sentence_rank={}

for sent in doc.sents:

    for word in sent :       

        if word.text.lower() in word_frequencies.keys():            

            if sent in sentence_rank.keys():
                sentence_rank[sent]+=word_frequencies[word.text.lower()]

            else:
                sentence_rank[sent]=word_frequencies[word.text.lower()]

top_sentences=(sorted(sentence_rank.values())[::-1])
print(top_sentences)

#top 2 sentences rank
top_sent=top_sentences[:2]
print(top_sent)

#creating final summary of document
summary=[]

for sent,strength in sentence_rank.items():  

    if strength in top_sent:
        summary.append(sent)

    else:
        continue

suma=""
for i in summary:
    # suma=print(i)
    suma=suma[:]+" "+str(i)
print(suma) 

#------------------------------------------------------------------------------------

"""
1>>>>how to install textblob :: https://textblob.readthedocs.io/en/dev/


2>>>>textblob for nlp / sentiment :: https://textblob.readthedocs.io/en/dev/index.html
"""    ###############

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

with open("CC_SPEAKER_1_IBM_DIARIZITAION.txt","r") as fp:
    text=fp.read()

te1=text.translate(str.maketrans('', '', string.punctuation))

blob = TextBlob(te1, analyzer=NaiveBayesAnalyzer())
blob.tags
blob.noun_phrases

tex1=""
for sentence in blob.sentences:
    print("\n\nSentiment of Speaker 1 : ",sentence.sentiment)
    tex1=tex1[:]+" "+str(sentence.sentiment)
#------------------------------
blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
blob.tags
blob.noun_phrases

sent1=""
for sentence in blob.sentences:
    print("\n\nSentiment of Each Sentences of Speaker 1 : ",sentence.sentiment)
    sent1=sent1[:]+" "+str(sentence.sentiment)

#---------------------------------------------------------

with open("CC_SPEAKER_2_IBM_DIARIZITAION.txt","r") as fp:
    text1=fp.read()

te2=text1.translate(str.maketrans('', '', string.punctuation))

blob = TextBlob(te2, analyzer=NaiveBayesAnalyzer())
blob.tags
blob.noun_phrases

tex2=""
for sentence in blob.sentences:
    print("\n\nSentiment of Speaker 2 : ",sentence.sentiment)
    tex2=tex2[:]+" "+str(sentence.sentiment)
#---------------------------------
blob1 = TextBlob(text1, analyzer=NaiveBayesAnalyzer())
blob1.tags
blob1.noun_phrases

sent2=""
for sentence1 in blob1.sentences:
    print("\n\nSentiment of Each Sentences of Speaker 2 : ",sentence1.sentiment)
    sent2=sent2[:]+" "+str(sentence1.sentiment)

#------------------------------------------------------------------------------
f=open("A_FINAL_RESULT.txt","w+")
f.write("\n\nFull Speech Without Punctuation : "+str0)
f.write("\n\nFull Speech With Punctuation : "+s)
f.write("\n\nText Summarization : "+suma)
f.write("\n\nSpeaker 1 : "+s1)
f.write("\n\nSpeaker 2 : "+s2)
f.write("\n\nSentiment of Speaker 1 : "+tex1)
f.write("\n\nSentiment of Speaker 2 : "+tex2)
f.close()