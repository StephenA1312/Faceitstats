from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Your Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1366287147845292132/JWU-E8p3bnzhJFykuhJPZurl5SJNaTCbw9n7QI2cvBocBqvUN55rgO687XzGLaZ6d3da"

# Function to send message to Discord
def send_to_discord(nickname, team, kills, deaths, adr, kd_ratio, score, result, date):
    formatted_score = f"{score} - {result}"
    message = {
        "content": f"**🎮 Game Stats for {nickname}:** 🎮\n"
                   f"🔹 **Team:** {team}\n"
                   f"🔸 **Kills - Deaths:** {kills} - {deaths}\n"
                   f"⚡ **ADR:** {adr}\n"
                   f"💣 **K/D Ratio:** {kd_ratio}\n"
                   f"📊 **Score:** {formatted_score}\n"
                   f"📅 **Date:** {date}"
    }
    
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    if response.status_code == 204:
        print("Message sent to Discord!")
    else:
        print(f"Error sending message: {response.status_code}")

# Endpoint to handle webhook POST requests
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Faceit sends data in JSON format
    print("faceit data", data)
    if "items" in data and len(data["items"]) > 0:
        match_data = data["items"][0]["stats"]
        
        # Extract the required fields from the match data
        nickname = match_data.get("Nickname")
        team = match_data.get("Team")
        kills = match_data.get("Kills")
        deaths = match_data.get("Deaths")
        adr = match_data.get("ADR")
        kd_ratio = match_data.get("K/D Ratio")
        score = match_data.get("Score")
        result = "🏆 **Won**" if match_data.get("Result") == "1" else "💔 **Lost**"
        date = match_data.get("Created At")[:10]  # Format date as YYYY-MM-DD
        
        # Send stats to Discord
        send_to_discord(nickname, team, kills, deaths, adr, kd_ratio, score, result, date)
    
    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    app.run(debug=True)
