from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import os
from bson.json_util import dumps

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connexion à MongoDB
mongo_uri = os.environ.get('MONGO_URI', "mongodb://admin:password@mongodb:27017/reviews_db?authSource=admin")
client = MongoClient(mongo_uri)
db = client.reviews_db

@app.route('/')
def index():
    return render_template('dashboard.html')


def emit_latest_data():
    """Emit the latest data to connected clients"""
    try:
        reviews = list(db.reviews.find().sort("timestamp", -1).limit(5))
        # Convert ObjectId to string for JSON serialization
        for review in reviews:
            review['_id'] = str(review['_id'])  # Convert ObjectId to string
            
        stats = list(db.reviews.aggregate([
            {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
        ]))
        
        socketio.emit('update', {'reviews': reviews, 'stats': stats})
    except Exception as e:
        print(f"Error fetching data: {e}")
        socketio.emit('error', {'message': str(e)})
        
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit_latest_data()

@socketio.on('start_updates')
def start_updates():
    """Démarrer l'envoi des mises à jour périodiques"""
    socketio.start_background_task(target=background_updates)

def background_updates():
    """Tâche en arrière-plan pour émettre les données périodiquement"""
    while True:
        emit_latest_data()
        socketio.sleep(5)  # Mise à jour toutes les 5 secondes

if __name__ == '__main__':
    print("Démarrage de l'application Flask...")
    # Mode debug pour développement
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    socketio.run(app, host='0.0.0.0', port=5000, debug=debug_mode, allow_unsafe_werkzeug=True)
