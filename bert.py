import json
import nltk
import pandas as pd
import regex as re
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer
from transformers import TFBertForSequenceClassification
import tensorflow as tf
from keras.models import load_model


# Package sentence tokenizer
nltk.download('punkt') 
# Package lemmatization
nltk.download('wordnet')
# Package multilingual wordnet data
nltk.download('omw-1.4')

# Importing the dataset
with open('train/datasets.json') as content:
  data1 = json.load(content)

# Mendapatkan semua data ke dalam list
tags = [] # data tag
inputs = [] # data input atau pattern
responses = {} # data respon
words = [] # Data kata 
classes = [] # Data Kelas atau Tag
documents = [] # Data Kalimat Dokumen
ignore_words = ['?', '!'] # Mengabaikan tanda spesial karakter

for intent in data1['intents']:
  responses[intent['tag']]=intent['responses']
  for lines in intent['patterns']:
    inputs.append(lines)
    tags.append(intent['tag'])
    for pattern in intent['patterns']:
      w = nltk.word_tokenize(pattern)
      words.extend(w)
      documents.append((w, intent['tag']))
      # add to our classes list
      if intent['tag'] not in classes:
        classes.append(intent['tag'])

# Konversi data json ke dalam dataframe
data = pd.DataFrame({"patterns":inputs, "tags":tags})

le = LabelEncoder()
data['tags'] = le.fit_transform(data['tags'])

def text_preprocessing(text):
  text = text.lower()                               # Mengubah teks menjadi lower case
  text = re.sub(r'https?://\S+|www\.\S+', '', text) # Menghapus URL
  text = re.sub(r'[-+]?[0-9]+', '', text)           # Menghapus angka
  text = re.sub(r'[^\w\s]','', text)                # Menghapus karakter tanda baca
  text = text.strip()                               # Menghapus whitespaces
  return text

data['patterns'] = data['patterns'].apply(text_preprocessing)

#Pretrained Model
PRE_TRAINED_MODEL = 'indobenchmark/indobert-base-p2'

#Load tokenizer dari pretrained model
bert_tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL)
    
# Load hasil fine-tuning
bert_load_model = TFBertForSequenceClassification.from_pretrained(PRE_TRAINED_MODEL, num_labels=62)
    
#Load Model
bert_load_model.load_weights('bert-model.h5')
