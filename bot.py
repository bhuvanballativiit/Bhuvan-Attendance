import requests
import base64
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# ==============================
# 🔐 EDIT ONLY THESE
# ==============================

BOT_TOKEN = "8585116374:AAFJGHDW1riRSEMEwvouWYeRL6TDTINPYcc"
USERNAME = "24L31A4608"
PASSWORD = "Bhuvan@123"


# ==============================
# 🔐 AES ENCRYPTION (Same as Website)
# ==============================

def encrypt_password(password):
    key = b'8701661282118308'
    iv = b'8701661282118308'

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(password.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded)

    return base64.b64encode(encrypted).decode()


# ==============================
# 🚀 ATTENDANCE FUNCTION
# ==============================

def get_attendance():
    session = requests.Session()

    # 1️⃣ Get Login Page
    login_url = "https://webprosindia.com/vignanit/"
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")

    viewstate = soup.find(id="__VIEWSTATE")["value"]
    eventvalidation = soup.find(id="__EVENTVALIDATION")["value"]

    encrypted_pwd = encrypt_password(PASSWORD)

    # 2️⃣ Login POST
    payload = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "txtId2": USERNAME,
        "txtPwd2": encrypted_pwd,
        "imgBtn2.x": "0",
        "imgBtn2.y": "0"
    }

    session.post(login_url + "default.aspx", data=payload)

    # 3️⃣ Get Attendance Page
    attendance_url = "https://webprosindia.com/vignanit/Academics/StudentAttendance.aspx?scrid=3&showtype=SA"
    attendance_page = session.get(attendance_url)

    soup = BeautifulSoup(attendance_page.text, "html.parser")

    table = soup.find("table", {"class": "cellBorder"})
    if not table:
        return "Login failed or attendance table not found."

    rows = table.find_all("tr")

    total_line = ""
    subject_lines = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 5:
            subject = cols[1].text.strip()
            held = cols[2].text.strip()
            attend = cols[3].text.strip()
            percent = cols[4].text.strip()

            if subject.upper() == "TOTAL":
                total_line = f"📊 Total: ({attend}/{held}) = {percent}%"
            else:
                subject_lines.append(f"{subject}: {attend}/{held}")

    return f"""
{total_line}

📚 Subject Wise:
{chr(10).join(subject_lines)}
"""


# ==============================
# 🤖 TELEGRAM COMMAND
# ==============================

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fetching attendance... ⏳")
    result = get_attendance()
    await update.message.reply_text(result)


# ==============================
# 🚀 START BOT
# ==============================

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("show", show))

    # Drop any previous update sessions
    app.run_polling(drop_pending_updates=True)