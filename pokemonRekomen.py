from flask import Flask,abort,jsonify,render_template,url_for,request,send_from_directory,redirect
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
import pandas as pd 
import json 
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pokehome.html')

@app.route('/hasil',methods=['POST','GET'])
def hasilPoke():
    if request.method == 'POST':
        body = request.form
        fav = body['name'].capitalize()

        if fav not in list(df['Name']):
            return redirect('/notfound')
        index = df[df['Name']==fav].index.values[0]

        pokerekomen = sorted(list(enumerate(cos_score[index])),key=lambda x:x[1],reverse=True) 
        pokefav = df.iloc[index][col]

        pokelain = []
        for i in pokerekomen:
            poke_x = {}
            if i[0] == index:
                continue
            else:
                num = df.iloc[i[0]]['#']
                name = df.iloc[i[0]]['Name']
                tipe = df.iloc[i[0]]['Type 1']
                gen = df.iloc[i[0]]['Generation']
                legend = df.iloc[i[0]]['Legendary']
                poke_x['num'] = num
                poke_x['name'] = name
                poke_x['tipe'] = tipe
                poke_x['gen'] = gen
                poke_x['legend'] = legend
            pokelain.append(poke_x)
            if len(pokelain) == 6:
                break
       
    return render_template('hasil.html',rekomen = pokelain, favoritku = pokefav)


@app.route('/notfound')
def notfound():
    return render_template('notfound.html')

if __name__ == "__main__":
    df = pd.read_csv('Pokemon.csv')
    df['Legendary'] = df['Legendary'].replace({False:'Not Legend',True: 'Legend'})
    col = ['#','Name','Type 1','Generation','Legendary']
    df = df[col]
    df['compare'] = df.apply(lambda i: f"{i['Type 1']},{(i['Generation'])},{(i['Legendary'])}",axis = 1)

    model = CountVectorizer(tokenizer= lambda x:x.split(','))
    model_extract = model.fit_transform(df['compare'])

    cos_score = cosine_similarity(model_extract)

    app.run(debug=True)