from flask import Flask
import requests

app = Flask(__name__)

peers = []
mensagem_evento = ""

@app.route("/")
def home():
    global mensagem_evento
    base = f"Peers conectados: {len(peers)}"
    if mensagem_evento:
        base += f"<br>{mensagem_evento}"
    return base

@app.route("/addpeer/<nome>/path:url")
def add_peer(nome, url):
    peer = f"{nome} ({url})"
    if peer not in peers:
        peers.append(peer)
        # Avisar o novo peer
        try:
            requests.get(f"{url}/welcome", timeout=3)
        except Exception:
            pass
        return "Novo nó conectado!"
    else:
        return "Este peer já está conectado."

@app.route("/welcome")
def welcome():
    global mensagem_evento
    mensagem_evento = "Você foi conectado a um novo peer"
    return mensagem_evento

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)