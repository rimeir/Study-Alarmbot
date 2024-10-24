import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio
import schedule

load_dotenv()

# 인텐스 설정
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler()

# .env 파일에서 토큰과 채널 ID 불러오기
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
CHANNEL_ID_TODO = int(os.getenv('DISCORD_CHANNEL_ID_TODO'))

DAYS_OF_WEEK = ['월', '화', '수', '목', '금', '토', '일']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

# 스터디 알람
# 월요일 오전 10시에 보내는 메시지
def ct_mon_mes():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send("@everyone \n📅 스터디 마감 D-1! \n이번 주도 화이팅!"))

# 화요일 오전 10시에 보내는 메시지
def ct_tue_am_mes():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send("@everyone \n📅 스터디 마감 D-0! \n모두 스터디 화이팅!"))

# 화요일 오후 10시에 보내는 메시지
def ct_tue_pm_mes():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        bot.loop.create_task(channel.send("@everyone \n📅 스터디 마감 2시간 전! \n잘 제출되었는지 확인하세요!"))

# 오늘 할 일 알람
async def todo_mes():
    channel = bot.get_channel(CHANNEL_ID_TODO)
    now = datetime.now()
    month_day = now.strftime('%m/%d')
    weekday = DAYS_OF_WEEK[now.weekday()]
    if channel:
        await channel.send(f"👍 {month_day}({weekday}) 오늘의 할 일! @everyone\n해당 메시지 스레드로 오늘 할 일을 12시까지 작성해주세요!")

# 오늘 할 일 매주 월~토요일까지 오전 10시에 알람 설정
def todo_alarm():
    for day in days:
        getattr(schedule.every(), day).at("10:00").do(
            lambda: asyncio.run_coroutine_threadsafe(todo_mes(), bot.loop)
        )

# 스케줄러 백그라운드에서 실행
async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(f'{bot.user}로 로그인되었습니다.')

    # 스터디 알람
    # 매주 월요일 오전 10시에 메시지 보내기
    scheduler.add_job(ct_mon_mes, CronTrigger(day_of_week="mon", hour=10, minute=0))

    # 매주 화요일 오전 10시에 메시지 보내기
    scheduler.add_job(ct_tue_am_mes, CronTrigger(day_of_week="tue", hour=10, minute=0))

    # 매주 화요일 오후 10시에 메시지 보내기
    scheduler.add_job(ct_tue_pm_mes, CronTrigger(day_of_week="wed", hour=22, minute=0))

    # 오늘 할 일 알람 설정
    todo_alarm()
    # 오늘 할 일에 날짜를 계속 업데이트하기 위해 루프
    asyncio.create_task(scheduler_loop())

    scheduler.start()

bot.run(BOT_TOKEN)