import os
import platform
import socket
import time
import psutil
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8772560384:AAEGRgYpRPPaKKKO87sGTg0vC6Plm3qWNpc")

start_time = time.time()

def get_server_info():
    hostname = socket.gethostname()

    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except:
        ip = "Unavailable"

    try:
        location = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        country = location.get("country", "Unknown")
        city = location.get("city", "Unknown")
    except:
        country = "Unknown"
        city = "Unknown"

    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count()

    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024**3), 2)
    ram_used = round(ram.used / (1024**3), 2)

    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024**3), 2)
    disk_used = round(disk.used / (1024**3), 2)

    uptime_seconds = int(time.time() - start_time)

    return {
        "hostname": hostname,
        "ip": ip,
        "country": country,
        "city": city,
        "cpu_percent": cpu_percent,
        "cpu_cores": cpu_cores,
        "ram_total": ram_total,
        "ram_used": ram_used,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "uptime": uptime_seconds
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    info = get_server_info()

    start_ping = time.time()
    await context.bot.get_me()
    latency = round((time.time() - start_ping) * 1000)

    bot = await context.bot.get_me()

    message = f"""
🚀 BOT CONTROL PANEL

🤖 Bot Name: {bot.first_name}
👤 Username: @{bot.username}
🆔 Bot ID: {bot.id}

🟢 Status: ONLINE

🐍 Python: {platform.python_version()}
💻 OS: {platform.system()} {platform.release()}
🏗 Architecture: {platform.machine()}

🏷 Hostname: {info['hostname']}

🌐 Public IP: {info['ip']}

📍 Location
Country: {info['country']}
City: {info['city']}

🧠 CPU Cores: {info['cpu_cores']}
📊 CPU Usage: {info['cpu_percent']} %

💾 RAM
Total: {info['ram_total']} GB
Used: {info['ram_used']} GB

💽 Disk
Total: {info['disk_total']} GB
Used: {info['disk_used']} GB

⚡ Ping: {latency} ms
⏱ Uptime: {info['uptime']} seconds

📡 Server Status: Running Smoothly
"""

    await update.message.reply_text(message)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    start_ping = time.time()
    await context.bot.get_me()
    latency = round((time.time() - start_ping) * 1000)

    await update.message.reply_text(f"🏓 Pong\nLatency: {latency} ms")


async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uptime_seconds = int(time.time() - start_time)
    await update.message.reply_text(f"⏱ Bot Uptime: {uptime_seconds} seconds")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    await update.message.reply_text(
        f"""
📊 LIVE SERVER STATS

CPU Usage: {cpu} %
RAM Usage: {ram} %
Disk Usage: {disk} %
"""
    )


def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("uptime", uptime))
    app.add_handler(CommandHandler("stats", stats))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()