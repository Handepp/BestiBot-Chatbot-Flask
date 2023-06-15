from flask import Flask,render_template,request,jsonify
from joblib import load
import random
from transformers import BertTokenizer
from transformers import TFBertForSequenceClassification
import tensorflow as tf
from keras.models import load_model
from bert import *

app   = Flask(__name__, static_url_path='/static')
model = None

#test
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chatroom")
def chat():
    return render_template("chatroom.html")


# [Routing untuk API]		
@app.route("/get")
def apiDeteksi():
    
    prediction_input = request.args.get('prediction_input')

    input_text_tokenized = bert_tokenizer.encode(prediction_input,
                                             truncation=True,
                                             padding='max_length',
                                             return_tensors='tf')
  
    bert_predict = bert_load_model(input_text_tokenized)          # Lakukan prediksi
    bert_predict = tf.nn.softmax(bert_predict[0], axis=-1)         # Softmax function untuk mendapatkan hasil klasifikasi
    output = tf.argmax(bert_predict, axis=1)

    response_tag = le.inverse_transform([output])[0]
    res = random.choice(responses[response_tag])    
    return res


if __name__ == '__main__':
    
    #Pretrained Model
    PRE_TRAINED_MODEL = 'indobenchmark/indobert-base-p2'

    #Load tokenizer dari pretrained model
    bert_tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL)

    # Load hasil fine-tuning
    bert_load_model = TFBertForSequenceClassification.from_pretrained(PRE_TRAINED_MODEL, num_labels=62)

    #Load Model
    bert_load_model.load_weights('bert-model.h5')

    #Deploy di localhostt
    app.run(host="localhost", port=5000, debug=True)
