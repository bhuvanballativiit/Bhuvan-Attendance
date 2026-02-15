import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# ==============================
# 🔐 EDIT ONLY THESE 3 VALUES
# ==============================

BOT_TOKEN = "8533340695:AAHmavCk_xxpL8abkzRca-eY45PorfrLF9A"
USERNAME = "24L31A4608"
PASSWORD = "Bhuvan@123"


# ==============================
# 🚀 ATTENDANCE FUNCTION
# ==============================

def get_attendance():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get("https://webprosindia.com/vignanit/")
        time.sleep(3)

        driver.find_element(By.ID, "txtId2").send_keys(USERNAME)
        driver.find_element(By.ID, "txtPwd2").send_keys(PASSWORD)
        driver.find_element(By.ID, "txtPwd2").submit()

        time.sleep(5)

        driver.get("https://webprosindia.com/vignanit/Academics/StudentAttendance.aspx?scrid=3&showtype=SA")
        time.sleep(5)

        driver.switch_to.frame("capIframe")
        time.sleep(3)

        rows = driver.find_elements(By.CSS_SELECTOR, "table.cellBorder tr")

        total_held = ""
        total_attend = ""
        total_percent = ""

        subject_lines = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            if len(cols) == 5:

                subject = cols[1].text.strip()
                held = cols[2].text.strip()
                attend = cols[3].text.strip()
                percent = cols[4].text.strip()

                if subject.upper() == "TOTAL":
                    total_held = held
                    total_attend = attend
                    total_percent = percent
                else:
                    subject_lines.append(f"{subject} : {attend}/{held}")

        message = f"""
📊 Total Attendance: ({total_attend}/{total_held}) = {total_percent}%

📚 Subject Wise Attendance:
{chr(10).join(subject_lines)}
"""

        return message

    except Exception as e:
        return f"Error occurred:\n{str(e)}"

    finally:
        driver.quit()


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
    app.run_polling()