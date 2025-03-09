import redis
import requests
from django.core.mail import send_mail

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

TELEGRAM_BOT_TOKEN = "7554541304:AAGnS_mQqPPueAU4ieBXWrQOJIi05qT4zdU"  # Ganti dengan token bot 
TELEGRAM_CHAT_ID = "1838945195"  # Ganti dengan chat ID admin

def send_over_speeding_alert(device_id, speed, timestamp):
    subject = "🚨 Over-Speeding Alert!"
    message = f"Device {device_id} detected over-speeding at {speed} km/h on {timestamp}."
    from_email = "testingwebsitesog@gmail.com"  # Ganti dengan email
    recipient_list = ["raihanannr@gmail.com"]  # Ganti dengan email admin
    
    send_mail(subject, message, from_email, recipient_list)

def send_telegram_alert(device_id, speed, timestamp):
    message = f"🚨 Over-Speeding Alert!\nDevice {device_id} melebihi batas kecepatan {speed} km/h pada {timestamp}."
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def update_ship_location(ship_id, latitude, longitude):
    """
    Menyimpan atau memperbarui lokasi kapal di Redis menggunakan GEOADD.
    """
    redis_client.geoadd("ships", (longitude, latitude, ship_id))

def get_ship_location(ship_id):
    """
    Mengambil lokasi kapal berdasarkan ship_id.
    """
    location = redis_client.geopos("ships", ship_id)
    if location and location[0]:
        return {"longitude": location[0][0], "latitude": location[0][1]}
    return None