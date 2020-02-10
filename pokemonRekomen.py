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
def hasil():
    if request.method == 'POST':
        pokebody = request.form
        favor = pokebody['name'].capitalize()

        if favor not in list(df['Name']):
            return redirect('/notfound')
        index = df[df['Name']==favor].index.values[0]
        pokerekomen = sorted(list(enumerate(cos_score[index])),key=lambda x:x[1],reverse=True) 
        pokefavorit = df.iloc[index][col]
        # print(poke_fav)
        pokelain = []
        for i in pokerekomen:
            pokex = {}
            if i[0] == index:
                continue
            else:
                num = df.iloc[i[0]]['#']
                name = df.iloc[i[0]]['Name']
                tipe = df.iloc[i[0]]['Type 1']
                gen = df.iloc[i[0]]['Generation']
                legend = df.iloc[i[0]]['Legendary']
                pokex['num'] = num
                pokex['name'] = name
                pokex['tipe'] = tipe
                pokex['gen'] = gen
                pokex['legend'] = legend
            pokelain.append(pokex)
            if len(pokelain) == 6:
                break
        # print(poke_lain)
    return render_template('rekomen.html',rekomen = pokelain, favor = pokefavorit)


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