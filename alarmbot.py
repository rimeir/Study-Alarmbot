import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv()

# 인텐트 설정
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler()

# .env 파일에서 토큰과 채널 ID 불러오기
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
CHANNEL_ID_TODO = int(os.getenv('DISCORD_CHANNEL_ID_TODO'))
CHANNEL_ID_TEST = int(os.getenv('DISCORD_CHANNEL_ID_TODO'))

DAYS_OF_WEEK = ['월', '화', '수', '목', '금', '토', '일']

# 메시지 전송 함수
async def send_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

# 스터디 알람 메시지
STUDY_MESSAGES = {
    "mon": "@everyone \n📅 스터디 마감 D-1! \n이번 주도 화이팅!",
    "tue_am": "@everyone \n📅 스터디 마감 D-0! \n모두 스터디 화이팅!",
    "tue_pm": "@everyone \n📅 스터디 마감 2시간 전! \n잘 제출되었는지 확인하세요!"
}

async def study_alarm(day):
    if day in STUDY_MESSAGES:
        await send_message(CHANNEL_ID, STUDY_MESSAGES[day])

async def test_alarm(day):
    if day in STUDY_MESSAGES:
        await send_message(CHANNEL_ID, STUDY_MESSAGES[day])

# 오늘 할 일 알람
async def todo_mes():
    now = datetime.now()
    month_day = now.strftime('%m/%d')
    weekday = DAYS_OF_WEEK[now.weekday()]
    message = f"👍 {month_day}({weekday}) 오늘의 할 일! @everyone\n해당 메시지 스레드로 오늘 할 일을 작성해주세요!"
    await send_message(CHANNEL_ID_TODO, message)

@bot.event
async def on_ready():
    print(f'{bot.user}로 로그인되었습니다.')
    loop = asyncio.get_event_loop()

    # 스터디 알람 스케줄 추가
    scheduler.add_job(lambda: loop.create_task(study_alarm("mon")), CronTrigger(day_of_week="mon", hour=10, minute=0))
    scheduler.add_job(lambda: loop.create_task(study_alarm("tue_am")), CronTrigger(day_of_week="tue", hour=10, minute=0))
    scheduler.add_job(lambda: loop.create_task(study_alarm("tue_pm")), CronTrigger(day_of_week="tue", hour=22, minute=0))

    scheduler.add_job(lambda: loop.create_task(test_alarm("tue_pm")), CronTrigger(day_of_week="tue", hour=11, minute=59))

    # 오늘 할 일 알람 매일 오전 9시
    scheduler.add_job(lambda: loop.create_task(todo_mes()), CronTrigger(hour=9, minute=0))

    scheduler.start()

bot.run(BOT_TOKEN)
