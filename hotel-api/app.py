import os, psycopg
from psycopg.rows import dict_row
from flask import Flask, request
from flask_cors import CORS 
from dotenv import load_dotenv

# pip install psycopg_binary och python-dotenv

load_dotenv()

PORT=8322

db_url = os.environ.get("DB_URL")

conn = psycopg.connect(db_url, autocommit=True, row_factory=dict_row)

app = Flask(__name__)
CORS(app) # Tillåt cross-origin requests

rooms = [
    { 'number': 101, 'type': "single" },
    { 'number': 202, 'type': "double" },
    { 'number': 303, 'type': "suite" }
]


@app.route("/",)
def info():
    return "<h1>Hotel API, endpoints /rooms, /bookings</h1>"


@app.route("/test",)
def dbtest():
    with conn.cursor() as cur:
        cur.execute("SELECT * from people")
        rows = cur.fetchall()
        return rows


@app.route("/ip")
def ip():
    return { 'ip': request.remote_addr }

@app.route("/bookings", methods=['GET', 'POST'])
def bookings():
    if request.method == 'GET':
        with conn.cursor() as cur:
            cur.execute("""
                SELECT hb.*, hg.firstname AS guest_firstname, hr.room_number
                FROM hotel_booking hb
                INNER JOIN hotel_guest hg ON hb.guest_id = hg.id
                INNER JOIN hotel_room hr ON hb.room_id = hr.id
                ORDER BY hb.datefrom
            """)
            return (cur.fetchall())
        
    if request.method == 'POST':
        body = request.get_json()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO hotel_booking (room_id, guest_id, datefrom) 
                VALUES (%s, %s, %s) RETURNING id
            """, [body['room'], body['guest'], body['datefrom']])
            result = cur.fetchone()
            return ({ "msg": "Du har bokat ett rum", "result": result })

@app.route("/guests", methods=['GET'])
def guests_endpoint():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT hg.*, 
                (SELECT COUNT(*) FROM hotel_booking WHERE guest_id = hg.id) AS num_visits
            FROM hotel_guest hg
            ORDER BY hg.firstname
        """)
        return (cur.fetchall())




@app.route("/rooms", methods=['GET', 'POST'])
def rooms_endpoint():
    if request.method == 'POST':
        request_body = request.get_json()
        print(request_body)
        rooms.append(request_body)
        return {
        'msg': f"Du har skapat ett nytt rum, id: {len(rooms)-1}!",
        }
    else:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM hotel_room ORDER BY room_number")
            return cur.fetchall()

@app.route("/rooms/<int:id>", methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def one_room(id):
    if request.method == 'GET':
       with conn.cursor() as cur:
            cur.execute("SELECT * FROM hotel_room WHERE id = %s", [id])
            return cur.fetchone()
    
    if request.method == 'PUT' or request.method == 'PATCH':
        return {
            'msg': f"Du uppdaterar id: {id}",
            'method': request.method
        }
    
    if request.method == 'DELETE':
        return {
            'msg': f"Du har raderat {id}",
            'method': request.method
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, ssl_context=(
        '/etc/letsencrypt/fullchain.pem', 
        '/etc/letsencrypt/privkey.pem'
    ))
