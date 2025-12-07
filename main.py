import os
import random
import time
import threading
from flask import Flask
from instagrapi import Client

app = Flask(__name__)

# ----------------- ENV VARIABLES -----------------
SESSION_ID = os.getenv("SESSION_ID")              # Instagram session ID
GROUP_IDS = os.getenv("GROUP_IDS", "").split(",") # Thread IDs: 1234567890,9876543210
MESSAGES = os.getenv("MESSAGES", "").split("|")   # msg1|msg2|msg3

# ----------------- LOGIN -----------------
cl = Client()
cl.login_by_sessionid(SESSION_ID)

running = False  # loop switch

# ----------------- LOOP SENDER -----------------
def loop_sender():
    global running
    print("Loop thread started...")
    while running:
        for gid in GROUP_IDS:

            if not running:
                break

            msg = random.choice(MESSAGES)

            try:
                # ✅ latest Instagrapi method
                cl.direct_send(msg, [gid])
                print(f"[SEND] {gid} → {msg}")
            except Exception as e:
                print("[ERROR]", e)

            # ---- SAFE SLOW SPEED ----
            time.sleep(random.uniform(0.8, 1.4))  # safe speed
            # --------------------------

# ----------------- ROUTES -----------------
@app.route("/")
def home():
    return "INSTAGRAM LOOP BOT RUNNING ✔"

@app.route("/start")
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=loop_sender).start()
        return "LOOP STARTED ✔ (SAFE SPEED)"
    else:
        return "LOOP ALREADY RUNNING"

@app.route("/stop")
def stop():
    global running
    running = False
    return "LOOP STOPPED ❌"

# ----------------- SERVER -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
