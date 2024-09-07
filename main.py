from flask import Flask, render_template, request, make_response
import random, json

app = Flask(__name__)

config = {
    "website_name": "ethancord"
}

@app.route("/")
def home_page():
    username = request.args.get("username")
    if not username:
        username = f"Guest-{random.randint(1, 10000)}"
    with open("messages.json", "r") as f:
        messages = json.load(f)
    return render_template("home.html", website_name=config["website_name"], username=username, messages=messages)

@app.route("/api/get-messages")
def get_messages():
    with open("messages.json", "r") as f:
        messages = json.load(f)
    return render_template("htmx_messages.html", messages=messages)

@app.route("/api/send-message", methods=["POST"])
def send_message():
    response = request.get_json()
    with open("messages.json", "r+") as f:
        messages = json.load(f)
        messages.append(response)
        f.seek(0)
        json.dump(messages, f)
        f.truncate()
    return make_response("Message sent!", 200)

if __name__ == "__main__":
    app.run(debug=True)
