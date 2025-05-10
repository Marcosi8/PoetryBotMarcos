import tweepy
import time
import random
import json
from flask import Flask
from threading import Thread
import os

app = Flask('')
@app.route('/')
def home():
    return "Bot tá vivo!"
def keep_alive():
    port = int(os.getenv("PORT", 8080))
    t = Thread(target=lambda: app.run(host='0.0.0.0', port=port))
    t.daemon = True
    t.start()

# Credenciais da API 
API_KEY = "aVbJtp8RGp5k5L5nvgZ3JLjaC"
API_SECRET = "18xqJmEhw7js2IVOs4KbHUHql31ze4g0hOVDHDkxLIWk4FlML1"
ACCESS_TOKEN = "1909005048925106176-nsAB47Ftw0niVqDhIjzdIhJeZtPqyx"
ACCESS_TOKEN_SECRET = "CO2YjIxd9nsB43Y6GSlZOlsrOT7AQyLd9wW238UF7Foqp"

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
client = tweepy.Client(consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

with open('conteudo.json', 'r', encoding='utf-8') as file:
    conteudo = json.load(file)

def postar_tweet():
    try:
        texto = random.choice(conteudo)["texto"]
        linhas = texto.split("\n")
        tweet = ""
        for linha in linhas:
            if len(tweet + linha + "\n") <= 280:
                tweet += linha + "\n"
            else:
                break
        tweet = tweet.strip()
        if len(texto) > 280:
            tweet = tweet[:277] + "..."
        client.create_tweet(text=tweet)
        print(f"Tweet postado: {tweet}")
    except tweepy.TweepyException as e:
        if e.response and e.response.status_code == 429:
            print("Erro 429: Limite atingido. Esperando 15 minutos...")
            time.sleep(900)  # 15 min (elon musk viadao)
        else:
            print(f"Erro ao postar: {e}")
            time.sleep(60)
    except Exception as e:
        print(f"Erro geral: {e}")
        time.sleep(60)

def main():
    while True:
        postar_tweet()
        time.sleep(21600)  # 6 horas = 4 tweets/dia

if __name__ == "__main__":
    keep_alive()
    main()
