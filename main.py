#!/usr/bin/env python3
# 🔥 SMS BLAST BOT - FINAL ULTIMATE (FIXED) 🔥
# Daily 2 Free Credits + 1000 User Scale

import re
import os
import sys
import requests
import json
import sqlite3
import random
import string
import time
import asyncio
import concurrent.futures
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ============================
# LOGGING
# ============================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# ============================
# CONFIG
# ============================
TOKEN = '8881226400:AAH7qky3qMsv6j97CiIHgaUuUcIV35fCwAU'
OWNER_ID = 8535388961
OWNER_USERNAME = "@Dragon_X_1"
FORCE_CHANNEL_USERNAME = "Dragon_X_111"
FORCE_CHANNEL_LINK = "https://t.me/Dragon_X_111"
OWNER_CONTACT_USERNAME = "@Dragon_X_king1"
OWNER_CONTACT_LINK = "https://t.me/Dragon_X_king1"
OWNER_PHONE = "+380 98 781 8214"

# 🎁 Daily free credits given to each user once per day
DAILY_FREE_CREDITS = 2

VIDEO_URLS = [
    "https://files.catbox.moe/iex2o2.mp4",
    "https://files.catbox.moe/n444eb.mp4",
    "https://files.catbox.moe/xf4tqz.mp4",
]

# ============================
# STYLISH FONT
# ============================
STYLISH_MAP = {
    'a':'ᴀ','b':'ʙ','c':'ᴄ','d':'ᴅ','e':'ᴇ','f':'ғ','g':'ɢ','h':'ʜ','i':'ɪ',
    'j':'ᴊ','k':'ᴋ','l':'ʟ','m':'ᴍ','n':'ɴ','o':'ᴏ','p':'ᴘ','q':'ǫ','r':'ʀ',
    's':'s','t':'ᴛ','u':'ᴜ','v':'ᴠ','w':'ᴡ','x':'x','y':'ʏ','z':'ᴢ',
    'A':'ᴀ','B':'ʙ','C':'ᴄ','D':'ᴅ','E':'ᴇ','F':'ғ','G':'ɢ','H':'ʜ','I':'ɪ',
    'J':'ᴊ','K':'ᴋ','L':'ʟ','M':'ᴍ','N':'ɴ','O':'ᴏ','P':'ᴘ','Q':'ǫ','R':'ʀ',
    'S':'s','T':'ᴛ','U':'ᴜ','V':'ᴠ','W':'ᴡ','X':'x','Y':'ʏ','Z':'ᴢ',
}
def st(text):
    if not text: return text
    return ''.join(STYLISH_MAP.get(c, c) for c in str(text))

# ============================
# BUTTONS
# ============================
BTN_BOMB      = "💣 sᴇɴᴅ sᴍs"
BTN_CREDITS   = "💰 ᴄʀᴇᴅɪᴛs"
BTN_REFERRAL  = "🔗 ʀᴇғᴇʀʀᴀʟ"
BTN_HISTORY   = "📜 ʜɪsᴛᴏʀʏ"
BTN_STATUS    = "🛡️ sᴛᴀᴛᴜs"
BTN_DEV       = "👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ"
BTN_REDEEM    = "🔑 ʀᴇᴅᴇᴇᴍ"
BTN_ADMIN     = "⚙️ ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ"

# ============================
# FIREBASE URLS
# ============================
FIREBASE_URLS = [
    "https://vasu-panel-default-rtdb.firebaseio.com",
    "https://retameta-default-rtdb.firebaseio.com",
    "https://krishna4343-e45fd-default-rtdb.firebaseio.com",
    "https://kdbhai-25325-default-rtdb.firebaseio.com",
    "https://land-le-mera-default-rtdb.firebaseio.com",
    "https://kichudjdudh-default-rtdb.firebaseio.com",
    "https://mithun-da-default-rtdb.firebaseio.com",
    "https://ajay-5cac9-default-rtdb.firebaseio.com",
    "https://back-b40b7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://pmnew230-default-rtdb.firebaseio.com",
    "https://rahul-panel-default-rtdb.firebaseio.com",
    "https://birend-b39e9-default-rtdb.firebaseio.com",
    "https://baba15-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://mamu-4db6e-default-rtdb.firebaseio.com",
    "https://bihar-master-panel-fb7cd-default-rtdb.firebaseio.com",
    "https://bhai-138a8-default-rtdb.firebaseio.com",
    "https://raj-bhai-1c1ad-default-rtdb.firebaseio.com",
    "https://ranimukarji-1182a-default-rtdb.firebaseio.com",
    "https://biharibhaiya-c718b-default-rtdb.firebaseio.com",
    "https://shukla2-default-rtdb.firebaseio.com",
    "https://ranjit-58640-default-rtdb.firebaseio.com",
    "https://newpanel-4412c-default-rtdb.firebaseio.com",
    "https://bittu3pannel-default-rtdb.firebaseio.com",
    "https://lalan-c7e44-default-rtdb.firebaseio.com",
    "https://uffuuf-d1a3c-default-rtdb.firebaseio.com",
    "https://fir-new-3-b572a-default-rtdb.firebaseio.com",
    "https://lol40-5bab7-default-rtdb.firebaseio.com",
    "https://rajaji-8d135-default-rtdb.firebaseio.com",
    "https://panelwalababa-ddd53-default-rtdb.firebaseio.com",
    "https://vikash-da-default-rtdb.firebaseio.com",
    "https://rea72-1566e-default-rtdb.firebaseio.com",
    "https://hospital-new-11-default-rtdb.firebaseio.com",
    "https://nowammyxdd-default-rtdb.firebaseio.com",
    "https://jujuboorchodi-default-rtdb.firebaseio.com",
    "https://seuihd-default-rtdb.firebaseio.com",
    "https://suman0h55-default-rtdb.firebaseio.com",
    "https://whithex-741e0-default-rtdb.firebaseio.com",
    "https://bsjshd-7e1bf-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://expert-5e1a0-default-rtdb.firebaseio.com",
    "https://jakepau-default-rtdb.firebaseio.com",
    "https://raj-londa-49db5-default-rtdb.firebaseio.com",
    "https://pm280reolc-default-rtdb.firebaseio.com",
    "https://botsieeee-af07c-default-rtdb.firebaseio.com",
    "https://topx-e09c6-default-rtdb.firebaseio.com",
    "https://lallo-6d4c5-default-rtdb.firebaseio.com",
    "https://second-wife-2-default-rtdb.firebaseio.com",
    "https://nand-d09e7-default-rtdb.firebaseio.com",
    "https://krishna5454-94fc5-default-rtdb.firebaseio.com",
    "https://asda-271a6-default-rtdb.firebaseio.com",
    "https://trigonnnnnnnn-default-rtdb.firebaseio.com",
    "https://xxxdrafft-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://arun-4024e-default-rtdb.firebaseio.com",
    "https://landlele-20855-default-rtdb.firebaseio.com",
    "https://arjun-singh-43d2f-default-rtdb.firebaseio.com",
    "https://dark-ka-app-default-rtdb.firebaseio.com",
    "https://nidhi-rani-default-rtdb.firebaseio.com",
    "https://nitu-23980-default-rtdb.firebaseio.com",
    "https://krijhjuiiiccyy-default-rtdb.firebaseio.com",
    "https://rahul-g11-default-rtdb.firebaseio.com",
    "https://rto-56-6cccf-default-rtdb.firebaseio.com",
    "https://download-b7393-default-rtdb.firebaseio.com",
    "https://rohet10-8919f-default-rtdb.firebaseio.com",
    "https://lol11-7da1c-default-rtdb.firebaseio.com",
    "https://ankitpanel-59086-default-rtdb.firebaseio.com",
    "https://rason00-default-rtdb.firebaseio.com",
    "https://ne-2db23-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://itslooksexp-default-rtdb.firebaseio.com",
    "https://raj-madarchodo-default-rtdb.firebaseio.com",
    "https://admin-sonu-8a567-default-rtdb.firebaseio.com",
    "https://randipelega-default-rtdb.firebaseio.com",
    "https://e21turnament2-default-rtdb.firebaseio.com",
    "https://ambani-19a25-default-rtdb.firebaseio.com",
    "https://sonuganduu-9d4da-default-rtdb.firebaseio.com",
    "https://gadhalalund-default-rtdb.firebaseio.com",
    "https://ahmedpanel-76b9c-default-rtdb.firebaseio.com",
    "https://khanipanel-d58cf-default-rtdb.firebaseio.com",
    "https://jyotiya75-default-rtdb.firebaseio.com",
    "https://saanvi-ji95-default-rtdb.firebaseio.com",
    "https://rto8-7f24f-default-rtdb.firebaseio.com",
    "https://penal-a93a8-default-rtdb.firebaseio.com",
    "https://ubhanhazx-default-rtdb.firebaseio.com",
    "https://pikachu-customer-16-default-rtdb.firebaseio.com",
    "https://e8383jsndn-default-rtdb.firebaseio.com",
    "https://saimharshji-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://mypnl01-ush-default-rtdb.firebaseio.com",
    "https://proof-abf73-default-rtdb.firebaseio.com",
    "https://apna3-e04f8-default-rtdb.firebaseio.com",
    "https://bola-2a0d3-default-rtdb.firebaseio.com",
    "https://lol24-95c49-default-rtdb.firebaseio.com",
    "https://fatmaadminpanel-default-rtdb.firebaseio.com",
    "https://rahulsharma-13303-default-rtdb.firebaseio.com",
    "https://myypppp-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://shsh-fb9c8-default-rtdb.firebaseio.com",
    "https://raj-panel-3e09a-default-rtdb.firebaseio.com",
    "https://khanpanel-c31a2-default-rtdb.firebaseio.com",
    "https://pornllllll-default-rtdb.firebaseio.com",
    "https://riyy-e012e-default-rtdb.firebaseio.com",
    "https://rajanmadarchod-fa98d-default-rtdb.firebaseio.com",
    "https://workohplic-default-rtdb.firebaseio.com",
    "https://panel-no-21-default-rtdb.firebaseio.com",
    "https://comkingdir-default-rtdb.firebaseio.com",
    "https://badka-3181b-default-rtdb.firebaseio.com",
    "https://kalui-a8e2b-default-rtdb.firebaseio.com",
    "https://vickyadmin45-default-rtdb.firebaseio.com",
    "https://iqrapanel-2f21d-default-rtdb.firebaseio.com",
    "https://rahul-8b7eb-default-rtdb.firebaseio.com",
    "https://bali-7acc3-default-rtdb.firebaseio.com",
    "https://firstlove2-1f2d9-default-rtdb.firebaseio.com",
    "https://sourav-f057d-default-rtdb.firebaseio.com",
    "https://pappuraj-714bd-default-rtdb.firebaseio.com",
    "https://astha-rani80-default-rtdb.firebaseio.com",
    "https://rohitbona-d8308-default-rtdb.firebaseio.com",
    "https://adityakaapp-default-rtdb.firebaseio.com",
    "https://hghg-6f0a8-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://tabuna-4e962-default-rtdb.firebaseio.com",
    "https://biki-3ae6e-default-rtdb.firebaseio.com",
    "https://adamm-green-default-rtdb.firebaseio.com",
    "https://gdgdgdgd-c1a32-default-rtdb.firebaseio.com",
    "https://nitish232626-default-rtdb.firebaseio.com",
    "https://amaat-a7916-default-rtdb.firebaseio.com",
    "https://project-1-16da0-default-rtdb.firebaseio.com",
    "https://aditya-9f66b-default-rtdb.firebaseio.com",
    "https://aya-tandi-default-rtdb.firebaseio.com",
    "https://ahmedpanel-e3d2d-default-rtdb.firebaseio.com",
    "https://mera-lala-default-rtdb.firebaseio.com",
    "https://iqrapanel-37c8d-default-rtdb.firebaseio.com",
    "https://baba-tillu-2-default-rtdb.firebaseio.com",
    "https://tuuui-60b15-default-rtdb.firebaseio.com",
    "https://fir-d327e-default-rtdb.firebaseio.com",
    "https://iiilsoee-default-rtdb.firebaseio.com",
    "https://vikasda-a78d5-default-rtdb.firebaseio.com",
    "https://polti-1317f-default-rtdb.firebaseio.com",
    "https://rahulbhi-default-rtdb.firebaseio.com",
    "https://arrun01-b1ece-default-rtdb.firebaseio.com",
    "https://rto-sandeep3-default-rtdb.firebaseio.com",
    "https://xrafaf-bfe94-default-rtdb.firebaseio.com",
    "https://vijay-afb12-default-rtdb.firebaseio.com",
    "https://rontem-a082b-default-rtdb.firebaseio.com",
    "https://adultapk-c3c4f-default-rtdb.firebaseio.com",
    "https://harrwp-6be36-default-rtdb.firebaseio.com",
    "https://pmnew157-default-rtdb.firebaseio.com",
    "https://madam-ji-17e1c-default-rtdb.firebaseio.com",
    "https://ramu-c81a7-default-rtdb.firebaseio.com",
    "https://pm-kisan-22f92-default-rtdb.firebaseio.com",
    "https://mainapanel-cleint-default-rtdb.firebaseio.com",
    "https://allinone-cf029-default-rtdb.firebaseio.com",
    "https://ramjidost-default-rtdb.firebaseio.com",
    "https://demon-4-default-rtdb.firebaseio.com",
    "https://hkfs-38ed5-default-rtdb.firebaseio.com",
    "https://ashishraj2-7e2e2-default-rtdb.firebaseio.com",
    "https://ak-boss-3a292-default-rtdb.firebaseio.com",
    "https://yellowpanel-9f036-default-rtdb.firebaseio.com",
    "https://tanvi-ji77-default-rtdb.firebaseio.com",
    "https://raj-admin-nokia-default-rtdb.firebaseio.com",
    "https://maxjoker98-2b75f-default-rtdb.firebaseio.com",
    "https://sagarguddu-268cb-default-rtdb.firebaseio.com",
    "https://akdk-f23fa-default-rtdb.firebaseio.com",
    "https://tracegod-168d5-default-rtdb.firebaseio.com",
    "https://uday-gaw-default-rtdb.firebaseio.com",
    "https://abhirt-58f65-default-rtdb.firebaseio.com",
    "https://krish-gana-default-rtdb.firebaseio.com",
    "https://e10ttqaq-default-rtdb.firebaseio.com",
    "https://oooo-2f098-default-rtdb.firebaseio.com",
    "https://subhash-45fb2-default-rtdb.firebaseio.com",
    "https://commotazee-darkness-default-rtdb.firebaseio.com",
    "https://kanak-ji99-default-rtdb.firebaseio.com",
    "https://saiyaraaa-ee8c4-default-rtdb.firebaseio.com",
    "https://priyaknn-3e914-default-rtdb.firebaseio.com",
    "https://urmila-ji12-default-rtdb.firebaseio.com",
    "https://amulyaji8080-default-rtdb.firebaseio.com",
    "https://lucky-c0915-default-rtdb.firebaseio.com",
    "https://priya-cfdb7-default-rtdb.firebaseio.com",
    "https://alwayssukuna-4dbb7-default-rtdb.firebaseio.com",
    "https://jrahh-83b83-default-rtdb.firebaseio.com",
    "https://videocalls-f3434-default-rtdb.firebaseio.com",
    "https://mama-ji-09-default-rtdb.firebaseio.com",
    "https://dark-1b5d9-default-rtdb.firebaseio.com",
    "https://sakshi1-dfc80-default-rtdb.firebaseio.com",
    "https://gojohere-29ab1-default-rtdb.firebaseio.com",
    "https://zamzam-baba77-default-rtdb.firebaseio.com",
    "https://ankit-raj-chutiya-default-rtdb.firebaseio.com",
    "https://akdh-e4bf4-default-rtdb.firebaseio.com",
    "https://arda-2fc05-default-rtdb.firebaseio.com",
    "https://amit-6f40a-default-rtdb.firebaseio.com",
    "https://usa-n-landon-default-rtdb.firebaseio.com",
    "https://hjmi-5af19-default-rtdb.firebaseio.com",
    "https://chumma-70293-default-rtdb.firebaseio.com",
    "https://hdfc-chodo-default-rtdb.firebaseio.com",
    "https://ravindra-d7887-default-rtdb.firebaseio.com",
    "https://ak47-e3976-default-rtdb.firebaseio.com",
    "https://mkdg-6a8f6-default-rtdb.firebaseio.com",
    "https://arunku25-9479d-default-rtdb.firebaseio.com",
    "https://ajio-427d1-default-rtdb.firebaseio.com",
    "https://htbc51-default-rtdb.firebaseio.com",
    "https://rurukatiu-default-rtdb.firebaseio.com",
    "https://new-panel-1e4a9-default-rtdb.firebaseio.com",
    "https://vasu-3rd-panel-default-rtdb.firebaseio.com",
    "https://rrt1-c797a-default-rtdb.firebaseio.com",
    "https://akumar-12eb3-default-rtdb.firebaseio.com",
    "https://riya-f1832-default-rtdb.firebaseio.com",
    "https://ghostx-panel-default-rtdb.firebaseio.com",
    "https://rajendra-2934a-default-rtdb.firebaseio.com",
    "https://e-challan-54-default-rtdb.firebaseio.com",
    "https://vrajbhai-4aa6e-default-rtdb.firebaseio.com",
    "https://hacker-panel-dcc53-default-rtdb.firebaseio.com",
    "https://atifhehu-7ec17-default-rtdb.firebaseio.com",
    "https://private-522a9-default-rtdb.firebaseio.com",
    "https://bittu-panal-cleint-default-rtdb.firebaseio.com",
    "https://soni-bbb64-default-rtdb.firebaseio.com",
    "https://zxcvbnm-13fb3-default-rtdb.firebaseio.com",
    "https://rahu-96df7-default-rtdb.firebaseio.com",
    "https://courier40-30jan-default-rtdb.firebaseio.com",
    "https://fixhogya-5b6e3-default-rtdb.firebaseio.com",
    "https://bega-8457c-default-rtdb.firebaseio.com",
    "https://mr-dr-72761-default-rtdb.firebaseio.com",
    "https://sintuadmin-default-rtdb.firebaseio.com",
    "https://vijayda-default-rtdb.firebaseio.com",
    "https://rto-47-b39f4-default-rtdb.firebaseio.com",
    "https://maja-1c323-default-rtdb.firebaseio.com",
    "https://benga-7d896-default-rtdb.firebaseio.com",
    "https://bipin-57f82-default-rtdb.firebaseio.com",
    "https://sumankr5764-e0ba8-default-rtdb.firebaseio.com",
    "https://kattapa-7faf3-default-rtdb.firebaseio.com",
    "https://rahudf-default-rtdb.firebaseio.com",
    "https://udyydfuuhc-default-rtdb.firebaseio.com",
]

# ============================
# HTTP SESSION (safe for high concurrency)
# ============================
try:
    import urllib3
    urllib3.disable_warnings()
except Exception:
    pass

HTTP_SESSION = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=50,
    pool_maxsize=100,
    max_retries=0,
    pool_block=False
)
HTTP_SESSION.mount('http://', adapter)
HTTP_SESSION.mount('https://', adapter)
HTTP_SESSION.headers.update({'Connection': 'keep-alive'})

# Safer worker limits for small hosts
EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=50)
GLOBAL_SEMAPHORE = asyncio.Semaphore(100)

# ============================
# GLOBAL STATE
# ============================
ACTIVE_TASKS = {}
ACTIVE_STOP_FLAGS = {}

# Device count cache (avoid hammering 200+ URLs every /start)
_DEVICE_CACHE = {"count": 8347, "ts": 0}
_DEVICE_CACHE_LOCK = asyncio.Lock()

# ============================
# DATABASE
# ============================
DB_PATH = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY, credits INTEGER DEFAULT 0,
        referrer_id INTEGER, joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_daily_credit TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
        user_id INTEGER PRIMARY KEY, banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        banned_by INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, amount INTEGER,
        credits_given INTEGER, transaction_id TEXT, screenshot_id TEXT,
        status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, action TEXT,
        details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS redeem_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT UNIQUE, credits INTEGER,
        used_by INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        used_at TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS maintenance (
        id INTEGER PRIMARY KEY, status INTEGER DEFAULT 0,
        message TEXT DEFAULT 'Bot is under maintenance.')''')
    c.execute("INSERT OR IGNORE INTO maintenance (id, status) VALUES (1, 0)")
    # ---- migrations for existing DBs ----
    try:
        c.execute("ALTER TABLE users ADD COLUMN last_daily_credit TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

init_db()

# ============================
# DB HELPERS
# ============================
def _get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn

def is_owner(user_id): return user_id == OWNER_ID

def get_user_credits(user_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row: return row[0]
    add_new_user(user_id)
    return DAILY_FREE_CREDITS

def add_new_user(user_id, referrer_id=None):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if c.fetchone():
        conn.close(); return
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute("INSERT INTO users (user_id, credits, referrer_id, last_daily_credit) VALUES (?, ?, ?, ?)",
              (user_id, DAILY_FREE_CREDITS, referrer_id, today))
    conn.commit()
    conn.close()
    if referrer_id and referrer_id != user_id:
        conn2 = _get_conn()
        c2 = conn2.cursor()
        c2.execute("SELECT credits FROM users WHERE user_id = ?", (referrer_id,))
        if c2.fetchone():
            c2.execute("UPDATE users SET credits = credits + 1 WHERE user_id = ?", (referrer_id,))
            conn2.commit()
        conn2.close()

def give_daily_credits(user_id):
    """Give daily free credits if not claimed today. Returns (given: bool, amount: int)."""
    today = datetime.now().strftime('%Y-%m-%d')
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT credits, last_daily_credit FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        add_new_user(user_id)
        return False, 0
    credits, last_claim = row
    if last_claim == today:
        conn.close()
        return False, 0
    new_credits = (credits or 0) + DAILY_FREE_CREDITS
    c.execute("UPDATE users SET credits = ?, last_daily_credit = ? WHERE user_id = ?",
              (new_credits, today, user_id))
    conn.commit()
    conn.close()
    return True, DAILY_FREE_CREDITS

def deduct_credit(user_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits - 1 WHERE user_id = ? AND credits > 0", (user_id,))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def add_credits(user_id, amount):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def remove_credits(user_id, amount):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET credits = credits - ? WHERE user_id = ? AND credits >= ?", (amount, user_id, amount))
    affected = c.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def ban_user(user_id, admin_id):
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO banned_users (user_id, banned_by) VALUES (?, ?)", (user_id, admin_id))
        conn.commit()
        conn.close()
        return True
    except Exception: return False

def unban_user(user_id):
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
        affected = c.rowcount
        conn.commit()
        conn.close()
        return affected > 0
    except Exception: return False

def is_user_banned(user_id):
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("SELECT user_id FROM banned_users WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        return row is not None
    except Exception: return False

def create_payment(user_id, amount, credits_given, transaction_id=None, screenshot_id=None):
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO payments (user_id, amount, credits_given, transaction_id, screenshot_id, status)
        VALUES (?, ?, ?, ?, ?, 'pending')''', (user_id, amount, credits_given, transaction_id, screenshot_id))
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid

def get_payment(payment_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT id, user_id, amount, credits_given, transaction_id, screenshot_id, status FROM payments WHERE id = ?", (payment_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_payment_status(payment_id, status):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE payments SET status = ? WHERE id = ?", (status, payment_id))
    conn.commit()
    conn.close()

def log_user_action(user_id, action, details=""):
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO user_history (user_id, action, details) VALUES (?, ?, ?)", (user_id, action, details))
        conn.commit()
        conn.close()
    except Exception: pass

def get_user_history(user_id, limit=10):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT action, details, created_at FROM user_history WHERE user_id = ? ORDER BY id DESC LIMIT ?", (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows

def get_referral_link(user_id, bot_username):
    return f"https://t.me/{bot_username}?start=ref_{user_id}"

def get_maintenance_status():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT status, message FROM maintenance WHERE id = 1")
    row = c.fetchone()
    conn.close()
    if row: return bool(row[0]), row[1]
    return False, ""

def set_maintenance_status(status):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE maintenance SET status = ? WHERE id = 1", (1 if status else 0,))
    conn.commit()
    conn.close()

def set_maintenance_message(message):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("UPDATE maintenance SET message = ? WHERE id = 1", (message,))
    conn.commit()
    conn.close()

def generate_redeem_key(credits):
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    conn = _get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO redeem_keys (key, credits) VALUES (?, ?)", (key, credits))
    conn.commit()
    conn.close()
    return key

def redeem_key(user_id, key):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT credits, used_by FROM redeem_keys WHERE key = ?", (key,))
    row = c.fetchone()
    if not row:
        conn.close(); return False, "Invalid key"
    credits, used_by = row
    if used_by:
        conn.close(); return False, "Key already used"
    c.execute("UPDATE redeem_keys SET used_by = ?, used_at = CURRENT_TIMESTAMP WHERE key = ?", (user_id, key))
    conn.commit()
    conn.close()
    add_credits(user_id, credits)
    return True, credits

def get_total_users():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]
    conn.close()
    return total

# ============================
# NETWORK (sync wrappers)
# ============================
def _sync_fetch(url, path, auth=None):
    try:
        base = url.rstrip('/')
        full_url = f"{base}/{path}.json"
        if auth and str(auth).strip():
            full_url += f"?auth={auth}"
        r = HTTP_SESSION.get(full_url, timeout=5, verify=False)
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return None
        return None
    except Exception:
        return None

def _sync_put(url, key, path, data):
    try:
        base = url.rstrip('/')
        full_url = f"{base}/{path}.json"
        if key and str(key).strip():
            full_url += f"?auth={key}"
        r = HTTP_SESSION.put(full_url, json=data, timeout=5, verify=False)
        return r.status_code in (200, 201)
    except Exception:
        return False

async def afetch(url, path, auth=None):
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(EXECUTOR, _sync_fetch, url, path, auth)
    except Exception:
        return None

async def aput(url, key, path, data):
    try:
        async with GLOBAL_SEMAPHORE:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(EXECUTOR, _sync_put, url, key, path, data)
    except Exception:
        return False

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def validate_phone_number(number):
    number = number.strip()
    if not number.startswith('+91'):
        return False, "❌ ɴᴜᴍʙᴇʀ ᴍᴜsᴛ sᴛᴀʀᴛ ᴡɪᴛʜ +91"
    remaining = number[3:]
    if not remaining.isdigit():
        return False, "❌ ᴏɴʟʏ ᴅɪɢɪᴛs ᴀʟʟᴏᴡᴇᴅ ᴀғᴛᴇʀ +91"
    if len(remaining) != 10:
        return False, "❌ ᴇɴᴛᴇʀ ᴇxᴀᴄᴛʟʏ 10 ᴅɪɢɪᴛs ᴀғᴛᴇʀ +91"
    return True, "✅ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ"

async def get_online_devices_async(force=False):
    """Cached device count — only refresh every 5 minutes"""
    global _DEVICE_CACHE
    now = time.time()
    if not force and (now - _DEVICE_CACHE["ts"]) < 300:
        return _DEVICE_CACHE["count"]
    try:
        async with _DEVICE_CACHE_LOCK:
            if not force and (time.time() - _DEVICE_CACHE["ts"]) < 300:
                return _DEVICE_CACHE["count"]
            async def check_one(url):
                try:
                    clients = await asyncio.wait_for(afetch(url, "/clients"), timeout=5)
                    if clients and isinstance(clients, dict):
                        return len(clients)
                except Exception:
                    pass
                return 0
            tasks = [check_one(url) for url in FIREBASE_URLS]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total = sum(r for r in results if isinstance(r, int))
            if total > 0:
                _DEVICE_CACHE["count"] = total
            _DEVICE_CACHE["ts"] = time.time()
    except Exception as e:
        logger.warning(f"device count error: {e}")
    return _DEVICE_CACHE["count"]

# ============================
# KEYBOARDS
# ============================
def get_main_keyboard(user_id=None):
    keyboard = [
        [KeyboardButton(BTN_BOMB)],
        [KeyboardButton(BTN_CREDITS), KeyboardButton(BTN_REFERRAL)],
        [KeyboardButton(BTN_HISTORY), KeyboardButton(BTN_STATUS)],
        [KeyboardButton(BTN_REDEEM)],
        [KeyboardButton(BTN_DEV)],
    ]
    if user_id and is_owner(user_id):
        keyboard.insert(0, [KeyboardButton(BTN_ADMIN)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔑 ɢᴇɴᴇʀᴀᴛᴇ ᴋᴇʏ", callback_data="admin_genkey")],
        [InlineKeyboardButton("📋 ʟɪsᴛ ᴋᴇʏs", callback_data="admin_listkeys")],
        [InlineKeyboardButton("🗑️ ᴅᴇʟᴇᴛᴇ ᴋᴇʏ", callback_data="admin_delkey")],
        [InlineKeyboardButton("🔧 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴛᴏɢɢʟᴇ", callback_data="admin_toggle_maint")],
        [InlineKeyboardButton("✏️ sᴇᴛ ᴍᴀɪɴᴛ ᴍsɢ", callback_data="admin_setmaint")],
        [InlineKeyboardButton("📊 ᴅᴇᴠɪᴄᴇ sᴛᴀᴛᴜs", callback_data="admin_devstatus")],
        [InlineKeyboardButton("👥 ᴜsᴇʀs", callback_data="admin_users")],
        [InlineKeyboardButton("💰 ᴘᴇɴᴅɪɴɢ ᴘᴀʏᴍᴇɴᴛs", callback_data="admin_payments")],
        [InlineKeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="admin_broadcast")],
        [InlineKeyboardButton("💵 ᴀᴅᴅ ᴄʀᴇᴅɪᴛs", callback_data="admin_addcredits")],
        [InlineKeyboardButton("💸 ʀᴇᴍᴏᴠᴇ ᴄʀᴇᴅɪᴛs", callback_data="admin_removecredits")],
        [InlineKeyboardButton("🚫 ʙᴀɴ", callback_data="admin_ban")],
        [InlineKeyboardButton("✅ ᴜɴʙᴀɴ", callback_data="admin_unban")],
        [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="admin_close")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ============================
# CANCEL
# ============================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for key in ['bulk_step','recharge_step','admin_step','redeem_step','waiting_for']:
        context.user_data.pop(key, None)
    await update.message.reply_text("❌ ᴄᴀɴᴄᴇʟʟᴇᴅ.", reply_markup=get_main_keyboard(update.effective_user.id))

# ============================
# START
# ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id

        for key in ['bulk_step','recharge_step','admin_step','redeem_step','waiting_for']:
            context.user_data.pop(key, None)

        if is_user_banned(user_id):
            await update.message.reply_text("❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ.")
            return

        maint_status, maint_msg = get_maintenance_status()
        if maint_status and not is_owner(user_id):
            await update.message.reply_text(f"🛠️ *ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ*\n\n{maint_msg}", parse_mode="HTML")
            return

        # Force channel check (non-fatal)
        try:
            member = await asyncio.wait_for(
                context.bot.get_chat_member(f"@{FORCE_CHANNEL_USERNAME}", user_id),
                timeout=10
            )
            if member.status in ['left', 'kicked']:
                markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=FORCE_CHANNEL_LINK)],
                    [InlineKeyboardButton("✅ ɪ ᴊᴏɪɴᴇᴅ", callback_data="check_join")]
                ])
                await update.message.reply_text(
                    f"🔐 *ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ!*\n\n{FORCE_CHANNEL_LINK}",
                    parse_mode="HTML", reply_markup=markup
                )
                return
        except Exception as e:
            logger.warning(f"channel check failed: {e}")

        referrer_id = None
        if context.args and len(context.args) > 0:
            payload = context.args[0]
            if payload.startswith("ref_"):
                try: referrer_id = int(payload.split("_")[1])
                except Exception: pass

        add_new_user(user_id, referrer_id)
        # Daily free credits
        got_daily, daily_amt = give_daily_credits(user_id)
        credits = get_user_credits(user_id)

        user = update.effective_user
        username = f"@{user.username}" if user.username else (user.first_name or "User")
        role = "👑 ᴏᴡɴᴇʀ" if is_owner(user_id) else "👤 ᴜsᴇʀ"

        # Video (non-fatal, short timeout)
        video_url = random.choice(VIDEO_URLS)
        try:
            await asyncio.wait_for(
                update.message.reply_video(video=video_url, caption="🔥 *sᴍs ʙʟᴀsᴛ ʙᴏᴛ* 🔥", parse_mode="HTML"),
                timeout=15
            )
        except Exception:
            pass

        # Cached device count
        try:
            device_count = await asyncio.wait_for(get_online_devices_async(), timeout=8)
        except Exception:
            device_count = _DEVICE_CACHE["count"]

        welcome = f"""╔═════════════════════╗
║     📱 sᴍs ʙʟᴀsᴛ ʙᴏᴛ   ║
║     ᴏᴡɴᴇʀ: {OWNER_USERNAME}    ║
║     ── ⋆⋅☆⋅⋆ ──                ║
║     👤 ʀᴏʟᴇ    : {role}        ║
║     📛 ᴜsᴇʀɴᴀᴍᴇ : {username}   ║
║     💰 ᴄʀᴇᴅɪᴛs : {credits}          ║
║     🎁 ᴅᴀɪʟʏ  : +{DAILY_FREE_CREDITS}/ᴅᴀʏ  ║
║     🔥 ᴀᴘɪs    : {len(FIREBASE_URLS)} ║
║     🔄 ᴅᴇᴠɪᴄᴇs : 🟢 {device_count} ║
║     ── ⋆⋅☆⋅⋆ ──                ║
║     ᴛᴀᴘ sᴇɴᴅ sᴍs ᴛᴏ sᴛᴀʀᴛ 🚀 ║
╚═════════════════════╝"""

        await update.message.reply_text(welcome, parse_mode="HTML", reply_markup=get_main_keyboard(user_id))

        if got_daily:
            try:
                await update.message.reply_text(
                    f"🎁 *ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅ ᴄʟᴀɪᴍᴇᴅ!*\n+{daily_amt} ғʀᴇᴇ ᴄʀᴇᴅɪᴛs ᴀᴅᴅᴇᴅ.\n💰 ʙᴀʟᴀɴᴄᴇ: `{credits}`",
                    parse_mode="HTML"
                )
            except Exception:
                pass

    except Exception as e:
        logger.exception(f"start error: {e}")
        try:
            await update.message.reply_text("⚠️ sᴛᴀʀᴛ ᴇʀʀᴏʀ. ᴛʀʏ ᴀɢᴀɪɴ.", reply_markup=get_main_keyboard(update.effective_user.id))
        except Exception:
            pass

# ============================
# HANDLE TEXT
# ============================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        text = update.message.text if update.message.text else ""

        if is_user_banned(user_id):
            await update.message.reply_text("❌ ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ.")
            return

        maint_status, maint_msg = get_maintenance_status()
        if maint_status and not is_owner(user_id):
            await update.message.reply_text(f"🛠️ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ: {maint_msg}")
            return

        # Silently grant daily credits on any interaction
        got_daily, daily_amt = give_daily_credits(user_id)
        if got_daily and not (text in (BTN_ADMIN,) and is_owner(user_id)):
            try:
                await update.message.reply_text(
                    f"🎁 *ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅ!* +{daily_amt} ᴄʀᴇᴅɪᴛs ᴀᴅᴅᴇᴅ.",
                    parse_mode="HTML"
                )
            except Exception:
                pass

        # MENU BUTTONS
        if text == BTN_ADMIN and is_owner(user_id):
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            await update.message.reply_text("⚙️ *ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ*", parse_mode="HTML", reply_markup=get_admin_keyboard())
            return

        if text == BTN_BOMB:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            await update.message.reply_text(
                "📞 *ᴇɴᴛᴇʀ ʀᴇᴄɪᴘɪᴇɴᴛ ɴᴜᴍʙᴇʀ:*\n✅ ғᴏʀᴍᴀᴛ: +91xxxxxxxxxx\n\n_ᴛʏᴘᴇ /cancel ᴛᴏ ᴀʙᴏʀᴛ._",
                parse_mode="HTML"
            )
            context.user_data['bulk_step'] = 'number'
            return

        if text == BTN_CREDITS:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            credits = get_user_credits(user_id)
            await update.message.reply_text(
                f"💰 *ʏᴏᴜʀ ᴄʀᴇᴅɪᴛs:* `{credits}`\n"
                f"🎁 ᴅᴀɪʟʏ ʀᴇᴡᴀʀᴅ: +{DAILY_FREE_CREDITS} ᴇᴠᴇʀʏ ᴅᴀʏ\n"
                f"🔗 ɪɴᴠɪᴛᴇ ғʀɪᴇɴᴅs ғᴏʀ +1 ᴄʀᴇᴅɪᴛ ᴇᴀᴄʜ",
                parse_mode="HTML"
            )
            return

        if text == BTN_REFERRAL:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            try:
                bot_username = (await context.application.bot.get_me()).username
            except Exception:
                bot_username = "bot"
            link = get_referral_link(user_id, bot_username)
            await update.message.reply_text(f"🔗 *ʏᴏᴜʀ ʟɪɴᴋ:*\n`{link}`", parse_mode="HTML")
            return

        if text == BTN_HISTORY:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            history = get_user_history(user_id, 10)
            if not history:
                await update.message.reply_text("📭 ɴᴏ ʜɪsᴛᴏʀʏ.")
                return
            reply = "📜 *ʀᴇᴄᴇɴᴛ ᴀᴄᴛɪᴠɪᴛʏ:*\n"
            for action, details, created_at in history:
                dt = created_at[:19] if created_at else "N/A"
                reply += f"• {action} – {details} ({dt})\n"
            await update.message.reply_text(reply, parse_mode="HTML")
            return

        if text == BTN_STATUS:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            try:
                device_count = await asyncio.wait_for(get_online_devices_async(), timeout=8)
            except Exception:
                device_count = _DEVICE_CACHE["count"]
            await update.message.reply_text(
                f"🟢 *sᴛᴀᴛᴜs*\n📡 ᴀᴘɪs: {len(FIREBASE_URLS)}\n📱 ᴅᴇᴠɪᴄᴇs: {device_count}\n👥 ᴜsᴇʀs: {get_total_users()}\n🎁 ᴅᴀɪʟʏ: +{DAILY_FREE_CREDITS} ᴄʀᴇᴅɪᴛ",
                parse_mode="HTML"
            )
            return

        if text == BTN_REDEEM:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            await update.message.reply_text("🔑 *ᴇɴᴛᴇʀ ʀᴇᴅᴇᴇᴍ ᴋᴇʏ:*", parse_mode="HTML")
            context.user_data['redeem_step'] = 'enter_key'
            return

        if text == BTN_DEV:
            for k in ['bulk_step','recharge_step','admin_step','redeem_step']:
                context.user_data.pop(k, None)
            await update.message.reply_text(
                f"👨‍💻 *ᴅᴇᴠᴇʟᴏᴘᴇʀ:* {OWNER_USERNAME}\n📞 *ᴄᴏɴᴛᴀᴄᴛ:* {OWNER_CONTACT_USERNAME}\n"
                f"📱 *ᴘʜᴏɴᴇ:* {OWNER_PHONE}\n🔗 [ᴄᴏɴᴛᴀᴄᴛ]({OWNER_CONTACT_LINK})",
                parse_mode="HTML", disable_web_page_preview=True
            )
            return

        # FLOW STATES
        admin_step = context.user_data.get('admin_step')
        redeem_step = context.user_data.get('redeem_step')
        recharge_step = context.user_data.get('recharge_step')
        bulk_step = context.user_data.get('bulk_step')

        # Admin inputs
        if admin_step == 'genkey_credits':
            try:
                credits = int(text.strip())
                key = generate_redeem_key(credits)
                await update.message.reply_text(f"✅ ᴋᴇʏ:\n`{key}`\nᴄʀᴇᴅɪᴛs: {credits}", parse_mode="HTML")
            except Exception:
                await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'delkey':
            key = text.strip().upper()
            conn = _get_conn(); c = conn.cursor()
            c.execute("DELETE FROM redeem_keys WHERE key = ?", (key,))
            aff = c.rowcount
            conn.commit(); conn.close()
            await update.message.reply_text("✅ ᴅᴇʟᴇᴛᴇᴅ." if aff else "❌ ɴᴏᴛ ғᴏᴜɴᴅ.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'setmaint_msg':
            set_maintenance_message(text)
            await update.message.reply_text("✅ ᴜᴘᴅᴀᴛᴇᴅ.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'broadcast':
            conn = _get_conn(); c = conn.cursor()
            c.execute("SELECT user_id FROM users")
            users = c.fetchall(); conn.close()
            sent = 0
            for (uid,) in users:
                try:
                    await context.bot.send_message(uid, text)
                    sent += 1
                    await asyncio.sleep(0.05)
                except Exception:
                    pass
            await update.message.reply_text(f"✅ sᴇɴᴛ ᴛᴏ {sent} ᴜsᴇʀs.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'addcredits_input':
            parts = text.strip().split()
            if len(parts) == 2:
                try:
                    add_credits(int(parts[0]), int(parts[1]))
                    await update.message.reply_text("✅ ᴀᴅᴅᴇᴅ.")
                except Exception:
                    await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'removecredits_input':
            parts = text.strip().split()
            if len(parts) == 2:
                try:
                    if remove_credits(int(parts[0]), int(parts[1])):
                        await update.message.reply_text("✅ ʀᴇᴍᴏᴠᴇᴅ.")
                    else:
                        await update.message.reply_text("❌ ɪɴsᴜғғɪᴄɪᴇɴᴛ.")
                except Exception:
                    await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'ban_input':
            try:
                if ban_user(int(text.strip()), user_id):
                    await update.message.reply_text("✅ ʙᴀɴɴᴇᴅ.")
            except Exception:
                await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ.")
            context.user_data.pop('admin_step', None)
            return

        if admin_step == 'unban_input':
            try:
                if unban_user(int(text.strip())):
                    await update.message.reply_text("✅ ᴜɴʙᴀɴɴᴇᴅ.")
                else:
                    await update.message.reply_text("❌ ɴᴏᴛ ʙᴀɴɴᴇᴅ.")
            except Exception:
                await update.message.reply_text("❌ ɪɴᴠᴀʟɪᴅ.")
            context.user_data.pop('admin_step', None)
            return

        # Redeem
        if redeem_step == 'enter_key':
            success, result = redeem_key(user_id, text.strip().upper())
            if success:
                await update.message.reply_text(f"✅ ʀᴇᴅᴇᴇᴍᴇᴅ! ɢᴏᴛ {result} ᴄʀᴇᴅɪᴛs.")
            else:
                await update.message.reply_text(f"❌ {result}")
            context.user_data.pop('redeem_step', None)
            return

        # Bulk SMS
        if bulk_step == 'number':
            number = text.strip()
            valid, msg = validate_phone_number(number)
            if not valid:
                await update.message.reply_text(f"{msg}\n\n📞 ғᴏʀᴍᴀᴛ: +91xxxxxxxxxx", parse_mode="HTML")
                return
            context.user_data['bulk_number'] = number
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔢 ʀᴀɴᴅᴏᴍ ᴏᴛᴘ", callback_data="msgtype_random")],
                [InlineKeyboardButton("✏️ ᴄᴜsᴛᴏᴍ sᴍs", callback_data="msgtype_custom")],
                [InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="msgtype_cancel")]
            ])
            await update.message.reply_text("📝 *sᴇʟᴇᴄᴛ ᴍᴇssᴀɢᴇ ᴛʏᴘᴇ:*", reply_markup=keyboard, parse_mode="HTML")
            context.user_data['bulk_step'] = 'msgtype'
            return

        if bulk_step == 'custom_msg':
            msg_text = text
            if not msg_text:
                await update.message.reply_text("❌ ᴇᴍᴘᴛʏ.")
                return
            context.user_data['custom_message'] = msg_text
            if user_id in ACTIVE_TASKS and not ACTIVE_TASKS[user_id].done():
                await update.message.reply_text("⚠️ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ!")
                context.user_data.pop('bulk_step', None)
                return
            log_user_action(user_id, "Bulk SMS Started", f"Target: {context.user_data['bulk_number']}")
            number = context.user_data['bulk_number']
            chat_id = update.effective_chat.id
            bot = context.application.bot
            progress_msg = await update.message.reply_text("🚀 *ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...*", parse_mode="HTML")
            ACTIVE_STOP_FLAGS[user_id] = False
            task = asyncio.create_task(
                bulk_send_worker(user_id, chat_id, bot, number, msg_text, progress_msg.message_id)
            )
            ACTIVE_TASKS[user_id] = task
            context.user_data.pop('bulk_step', None)
            return

        await update.message.reply_text("❌ ᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs.", reply_markup=get_main_keyboard(user_id))

    except Exception as e:
        logger.exception(f"handle_text error: {e}")
        try:
            await update.message.reply_text("⚠️ ᴇʀʀᴏʀ. ᴛʀʏ ᴀɢᴀɪɴ.")
        except Exception:
            pass

# ============================
# BULK WORKER
# ============================
async def bulk_send_worker(user_id, chat_id, bot, number, msg_text, progress_msg_id):
    total_sent = 0
    total_failed = 0
    cycle = 1
    active_devices = 0
    start_time = time.time()

    stop_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏹ sᴛᴏᴘ sᴇɴᴅɪɴɢ", callback_data="stop_bulk")]
    ])

    otp_placeholder = re.search(r'\{otp(:\d+)?\}', msg_text)
    otp_length = 6
    if otp_placeholder and otp_placeholder.group(1):
        try:
            otp_length = max(1, min(10, int(otp_placeholder.group(1)[1:])))
        except Exception:
            otp_length = 6

    last_update = 0
    progress_emojis = ["🚀","⚡","💥","🔥","✨","🌟","💫","🎯"]

    try:
        while not ACTIVE_STOP_FLAGS.get(user_id, False):
            if is_user_banned(user_id):
                break

            now = time.time()
            if now - last_update > 2.5:
                emoji = random.choice(progress_emojis)
                elapsed = int(now - start_time)
                mins = elapsed // 60
                secs = elapsed % 60
                elapsed_str = f"{mins}ᴍ {secs}s" if mins else f"{secs}s"
                rate = total_sent / max(elapsed, 1)
                progress_text = (
                    f"╔══════════════════════╗\n"
                    f"║  {emoji} *sᴍs ʙʟᴀsᴛɪɴɢ* {emoji}  ║\n"
                    f"╚══════════════════════╝\n"
                    f"🔄 ᴄʏᴄʟᴇ: *#{cycle}*\n"
                    f"📱 ᴀᴄᴛɪᴠᴇ ᴅᴇᴠɪᴄᴇs: *{active_devices}*\n"
                    f"✅ sᴇɴᴛ: *{total_sent}*\n"
                    f"❌ ғᴀɪʟᴇᴅ: *{total_failed}*\n"
                    f"⚡ sᴘᴇᴇᴅ: *{rate:.1f}/s*\n"
                    f"⏱️ ʀᴜɴɴɪɴɢ: *{elapsed_str}*\n"
                    f"🎯 ᴛᴀʀɢᴇᴛ: `{number}`\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                )
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id, message_id=progress_msg_id,
                        text=progress_text, parse_mode="HTML", reply_markup=stop_markup
                    )
                    last_update = now
                except Exception:
                    pass

            # Parallel fetch of all Firebase clients
            url_results = await asyncio.gather(
                *[afetch(url, "/clients") for url in FIREBASE_URLS],
                return_exceptions=True
            )

            cycle_device_count = 0
            send_tasks = []
            for idx, clients in enumerate(url_results):
                if ACTIVE_STOP_FLAGS.get(user_id, False) or is_user_banned(user_id):
                    break
                if not clients or not isinstance(clients, dict):
                    continue
                url = FIREBASE_URLS[idx]
                for dev_id in clients.keys():
                    cycle_device_count += 1
                    for _ in range(2):
                        final_msg = msg_text
                        if otp_placeholder:
                            otp = generate_otp(otp_length)
                            final_msg = re.sub(r'\{otp(:\d+)?\}', otp, msg_text)
                        path = f"clients/{dev_id}/webhookEvent/sendSms"
                        payload = {"sim": 1, "to": number, "message": final_msg, "isSended": False}
                        send_tasks.append(aput(url, None, path, payload))

                        if len(send_tasks) >= 2000:
                            break
                    if len(send_tasks) >= 2000:
                        break
                if len(send_tasks) >= 2000:
                    break

            active_devices = cycle_device_count

            chunk_size = 100
            for i in range(0, len(send_tasks), chunk_size):
                if ACTIVE_STOP_FLAGS.get(user_id, False) or is_user_banned(user_id):
                    break
                chunk = send_tasks[i:i+chunk_size]
                results = await asyncio.gather(*chunk, return_exceptions=True)
                for r in results:
                    if r is True:
                        total_sent += 1
                    else:
                        total_failed += 1
                await asyncio.sleep(0.05)

            cycle += 1
            await asyncio.sleep(0.3)

    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.exception(f"worker error: {e}")
    finally:
        elapsed = int(time.time() - start_time)
        mins = elapsed // 60
        secs = elapsed % 60
        elapsed_str = f"{mins}ᴍ {secs}s" if mins else f"{secs}s"
        final_text = (
            f"╔══════════════════════╗\n"
            f"║  🛑 *sᴛᴏᴘᴘᴇᴅ* 🛑       ║\n"
            f"╚══════════════════════╝\n"
            f"✅ ᴛᴏᴛᴀʟ sᴇɴᴛ: *{total_sent}*\n"
            f"❌ ᴛᴏᴛᴀʟ ғᴀɪʟᴇᴅ: *{total_failed}*\n"
            f"🔄 ᴄʏᴄʟᴇs: *{cycle - 1}*\n"
            f"⏱️ ᴛɪᴍᴇ: *{elapsed_str}*\n"
            f"🎯 ᴛᴀʀɢᴇᴛ: `{number}`\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=progress_msg_id, text=final_text, parse_mode="HTML")
        except Exception:
            pass
        try:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=progress_msg_id, reply_markup=None)
        except Exception:
            pass
        log_user_action(user_id, "Bulk SMS Ended", f"Sent {total_sent}, Failed {total_failed}")
        ACTIVE_TASKS.pop(user_id, None)
        ACTIVE_STOP_FLAGS.pop(user_id, None)

# ============================
# CALLBACKS
# ============================
async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        data = query.data

        if data == "check_join":
            try:
                member = await context.bot.get_chat_member(f"@{FORCE_CHANNEL_USERNAME}", user_id)
                if member.status in ['left', 'kicked']:
                    await query.edit_message_text("❌ ɴᴏᴛ ᴊᴏɪɴᴇᴅ!")
                    return
                await query.edit_message_text("✅ ᴠᴇʀɪғɪᴇᴅ! ᴜsᴇ /start")
            except Exception:
                await query.edit_message_text("❌ ᴇʀʀᴏʀ.")
            return

        # Admin
        if data.startswith("admin_"):
            if not is_owner(user_id):
                await query.edit_message_text("⛔")
                return
            if data == "admin_close":
                await query.edit_message_text("❌ ᴄʟᴏsᴇᴅ.")
            elif data == "admin_genkey":
                await query.edit_message_text("🔑 ᴇɴᴛᴇʀ ᴄʀᴇᴅɪᴛs:")
                context.user_data['admin_step'] = 'genkey_credits'
            elif data == "admin_listkeys":
                conn = _get_conn(); c = conn.cursor()
                c.execute("SELECT key, credits, used_by FROM redeem_keys ORDER BY id DESC LIMIT 20")
                rows = c.fetchall(); conn.close()
                if not rows:
                    await query.edit_message_text("📭 ɴᴏ ᴋᴇʏs.")
                    return
                t = "📋 *ᴋᴇʏs:*\n"
                for k, cr, ub in rows:
                    s = "❌" if ub else "✅"
                    t += f"`{k}` - {cr}ᴄ {s}\n"
                await query.edit_message_text(t, parse_mode="HTML")
            elif data == "admin_delkey":
                await query.edit_message_text("🗑️ ᴋᴇʏ:")
                context.user_data['admin_step'] = 'delkey'
            elif data == "admin_toggle_maint":
                s, _ = get_maintenance_status()
                set_maintenance_status(not s)
                await query.edit_message_text(f"🔧 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ: *{'ᴏɴ' if not s else 'ᴏғғ'}*", parse_mode="HTML")
            elif data == "admin_setmaint":
                await query.edit_message_text("✏️ ᴍsɢ:")
                context.user_data['admin_step'] = 'setmaint_msg'
            elif data == "admin_devstatus":
                try:
                    dc = await asyncio.wait_for(get_online_devices_async(force=True), timeout=15)
                except Exception:
                    dc = _DEVICE_CACHE["count"]
                await query.edit_message_text(f"📊 ᴀᴘɪs: {len(FIREBASE_URLS)}\n📱 ᴅᴇᴠɪᴄᴇs: {dc}", parse_mode="HTML")
            elif data == "admin_users":
                conn = _get_conn(); c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM users")
                t = c.fetchone()[0]
                c.execute("SELECT COUNT(*) FROM banned_users")
                b = c.fetchone()[0]
                conn.close()
                await query.edit_message_text(f"👥 {t}\n🚫 {b}", parse_mode="HTML")
            elif data == "admin_payments":
                conn = _get_conn(); c = conn.cursor()
                c.execute("SELECT id, user_id, amount FROM payments WHERE status = 'pending' ORDER BY id DESC LIMIT 10")
                rows = c.fetchall(); conn.close()
                if not rows:
                    await query.edit_message_text("📭 ɴᴏɴᴇ.")
                    return
                t = "💰 *ᴘᴇɴᴅɪɴɢ:*\n"
                for pid, uid, amt in rows:
                    t += f"#{pid} {uid} ₹{amt}\n"
                await query.edit_message_text(t, parse_mode="HTML")
            elif data == "admin_broadcast":
                await query.edit_message_text("📢 ᴍsɢ:")
                context.user_data['admin_step'] = 'broadcast'
            elif data == "admin_addcredits":
                await query.edit_message_text("💵 `<ɪᴅ> <ᴀᴍᴛ>`", parse_mode="HTML")
                context.user_data['admin_step'] = 'addcredits_input'
            elif data == "admin_removecredits":
                await query.edit_message_text("💸 `<ɪᴅ> <ᴀᴍᴛ>`", parse_mode="HTML")
                context.user_data['admin_step'] = 'removecredits_input'
            elif data == "admin_ban":
                await query.edit_message_text("🚫 ɪᴅ:")
                context.user_data['admin_step'] = 'ban_input'
            elif data == "admin_unban":
                await query.edit_message_text("✅ ɪᴅ:")
                context.user_data['admin_step'] = 'unban_input'
            return

        # Bulk msgtype
        if data.startswith("msgtype_"):
            if data == "msgtype_cancel":
                await query.edit_message_text("❌")
                context.user_data.pop('bulk_step', None)
                return
            msg_type = data.split("_")[1]
            if msg_type == "random":
                default_msg = "आपका OTP है: {otp} | कृपया इसे किसी को न बताएँ।"
                context.user_data['custom_message'] = default_msg
                if user_id in ACTIVE_TASKS and not ACTIVE_TASKS[user_id].done():
                    await query.edit_message_text("⚠️ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ!")
                    return
                number = context.user_data.get('bulk_number')
                if not number:
                    await query.edit_message_text("❌ sᴇssɪᴏɴ ᴇxᴘɪʀᴇᴅ.")
                    return
                chat_id = query.message.chat_id
                await query.edit_message_text("🚀 *sᴛᴀʀᴛɪɴɢ...*", parse_mode="HTML")
                progress_msg = await context.bot.send_message(chat_id, "⚡ ɪɴɪᴛɪᴀʟɪᴢɪɴɢ...")
                log_user_action(user_id, "Bulk SMS Started", f"Target: {number}")
                ACTIVE_STOP_FLAGS[user_id] = False
                task = asyncio.create_task(
                    bulk_send_worker(user_id, chat_id, context.bot, number, default_msg, progress_msg.message_id)
                )
                ACTIVE_TASKS[user_id] = task
                context.user_data.pop('bulk_step', None)
            else:
                await query.edit_message_text("✏️ ᴄᴜsᴛᴏᴍ ᴍsɢ:\n💡 `{otp}` ғᴏʀ ᴏᴛᴘ.", parse_mode="HTML")
                context.user_data['bulk_step'] = 'custom_msg'
            return

        if data == "stop_bulk":
            ACTIVE_STOP_FLAGS[user_id] = True
            if user_id in ACTIVE_TASKS:
                try:
                    ACTIVE_TASKS[user_id].cancel()
                except Exception:
                    pass
            await query.answer("sᴛᴏᴘᴘɪɴɢ...", show_alert=True)
            return

    except Exception as e:
        logger.exception(f"callback error: {e}")

# ============================
# OWNER COMMANDS
# ============================
async def add_credits_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    args = context.args
    if len(args) < 2: return
    try:
        add_credits(int(args[0]), int(args[1]))
        await update.message.reply_text("✅")
    except Exception:
        await update.message.reply_text("❌")

async def remove_credits_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    args = context.args
    if len(args) < 2: return
    try:
        if remove_credits(int(args[0]), int(args[1])):
            await update.message.reply_text("✅")
        else:
            await update.message.reply_text("❌ ɪɴsᴜғғɪᴄɪᴇɴᴛ")
    except Exception:
        await update.message.reply_text("❌")

async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not context.args: return
    try:
        ban_user(int(context.args[0]), update.effective_user.id)
        await update.message.reply_text("✅")
    except Exception:
        await update.message.reply_text("❌")

async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not context.args: return
    try:
        unban_user(int(context.args[0]))
        await update.message.reply_text("✅")
    except Exception:
        await update.message.reply_text("❌")

async def genkey_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not context.args: return
    try:
        key = generate_redeem_key(int(context.args[0]))
        await update.message.reply_text(f"✅ `{key}`", parse_mode="HTML")
    except Exception:
        await update.message.reply_text("❌")

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    await update.message.reply_text("🛑")
    await context.application.stop()
    os._exit(0)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"⚠️ Exception: {context.error}", exc_info=context.error)

async def post_init(application: Application):
    try:
        await application.bot.set_my_commands([
            ("start", "sᴛᴀʀᴛ ʙᴏᴛ"),
            ("cancel", "ᴄᴀɴᴄᴇʟ ᴄᴜʀʀᴇɴᴛ"),
        ])
    except Exception as e:
        logger.warning(f"post_init error: {e}")

# ============================
# MAIN (auto-restart loop)
# ============================
def run_bot_once():
    application = (
        Application.builder()
        .token(TOKEN)
        .concurrent_updates(True)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("addcredits", add_credits_cmd))
    application.add_handler(CommandHandler("removecredits", remove_credits_cmd))
    application.add_handler(CommandHandler("ban", ban_cmd))
    application.add_handler(CommandHandler("unban", unban_cmd))
    application.add_handler(CommandHandler("genkey", genkey_cmd))
    application.add_handler(CommandHandler("shutdown", shutdown))

    application.add_handler(CallbackQueryHandler(handle_callbacks))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_text))

    application.add_error_handler(error_handler)

    logger.info("🚀 Bot starting polling...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False,
    )

def main():
    print("""
╔════════════════════════════════════════════════╗
║  🚀 sᴍs ʙʟᴀsᴛ ʙᴏᴛ - ᴜʟᴛɪᴍᴀᴛᴇ ᴇᴅɪᴛɪᴏɴ          ║
║  ✅ ʟɪᴠᴇ ᴘʀᴏɢʀᴇss ᴡɪᴛʜ ᴇᴍᴏᴊɪs                  ║
║  ✅ 1000+ ᴜsᴇʀ sᴄᴀʟᴇ                          ║
║  ✅ 🎁 2 FREE CREDITS DAILY                     ║
╚════════════════════════════════════════════════╝
    """)
    while True:
        try:
            run_bot_once()
        except KeyboardInterrupt:
            logger.info("Stopped by user")
            break
        except Exception as e:
            logger.exception(f"Bot crashed: {e} — restarting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    main()