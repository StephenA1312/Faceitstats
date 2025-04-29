from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1366287147845292132/JWU-E8p3bnzhJFykuhJPZurl5SJNaTCbw9n7QI2cvBocBqvUN55rgO687XzGLaZ6d3da"

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Function to send cleaned stats to Discord
def send_to_discord(match_summary):
    message = {
        "embeds": [
            {
                "title": f"{match_summary['Player']}'s Match Summary",
                "description": f"[View Match]({match_summary['Match Link']})",
                "color": 65280,  # Green color
                "fields": [
                    {"name": "Map", "value": match_summary["Map"], "inline": True},
                    {"name": "Score", "value": match_summary["Final Score"], "inline": True},
                    {"name": "Result", "value": match_summary["Result"], "inline": True},
                    {"name": "Kills", "value": match_summary["Kills"], "inline": True},
                    {"name": "Deaths", "value": match_summary["Deaths"], "inline": True},
                    {"name": "K/D Ratio", "value": match_summary["K/D Ratio"], "inline": True},
                    {"name": "Headshots %", "value": match_summary["Headshots %"], "inline": True},
                    {"name": "ADR", "value": match_summary["ADR"], "inline": True},
                    {"name": "MVPs", "value": match_summary["MVPs"], "inline": True}
                ],
                "timestamp": match_summary["Date"]
            }
        ]
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    if response.status_code == 204:
        print("✅ Message sent to Discord!")
    else:
        print(f"❌ Error sending message: {response.status_code} - {response.text}")

# Endpoint to handle webhook POST requests
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Faceit sends data in JSON format
    print("Incoming Faceit Data:", data)

    if "items" in data and len(data["items"]) > 0:
        match = data["items"][0]["stats"]

        # Build cleaned summary
        match_summary = {
            "Player": match.get("Nickname"),
            "Map": match.get("Map"),
            "Final Score": match.get("Score"),
            "Result": "🏆 Win" if match.get("Result") == "1" else "💔 Loss",
            "Kills": match.get("Kills"),
            "Deaths": match.get("Deaths"),
            "K/D Ratio": match.get("K/D Ratio"),
            "Headshots %": match.get("Headshots %"),
            "ADR": match.get("ADR"),
            "MVPs": match.get("MVPs"),
            "Date": match.get("Created At"),
            "Match Link": f"https://www.faceit.com/en/cs2/room/{match.get('Match Id')}"
        }

        send_to_discord(match_summary)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
