import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler()

# .env 파일에서 토큰과 채널 ID 불러오기
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# 월요일 오전 10시에 보내는 메시지
def monday_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send("@everyone \n📅 스터디 마감 D-1! \n이번 주도 화이팅!"))

# 화요일 오전 10시에 보내는 메시지
def tuesday_am_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send("@everyone \n📅 스터디 마감 D-0! \n모두 스터디 화이팅!"))

# 화요일 오후 10시에 보내는 메시지
def tuesday_pm_message():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send("@everyone \n📅 스터디 마감 2시간 전! \n잘 제출되었는지 확인하세요!"))

@bot.event
async def on_ready():
    print(f'{bot.user}로 로그인되었습니다.')

    # 매주 월요일 오전 10시에 메시지 보내기
    scheduler.add_job(monday_message, CronTrigger(day_of_week="mon", hour=10, minute=0))

    # 매주 화요일 오전 10시에 메시지 보내기
    scheduler.add_job(tuesday_am_message, CronTrigger(day_of_week="tue", hour=10, minute=0))

    # 매주 화요일 오후 10시에 메시지 보내기
    scheduler.add_job(tuesday_pm_message, CronTrigger(day_of_week="tue", hour=22, minute=0))

    scheduler.start()

bot.run(BOT_TOKEN)