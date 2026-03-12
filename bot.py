import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import os

TOKEN = os.getenv("TOKEN")
GUILD_ID = 123456789012345678

CANAL_BOSS = 1481485483619123281
CANAL_SHOP = 1481485503609045105

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def agora():
    return datetime.utcnow() - timedelta(hours=3)

def proximo_boss():
    tempo = agora()
    return tempo.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

def proximo_shop():
    tempo = agora()
    horarios = [1, 5, 9, 13, 17, 21]

    for h in horarios:
        proximo = tempo.replace(hour=h, minute=0, second=0, microsecond=0)
        if tempo < proximo:
            return proximo

    amanha = tempo + timedelta(days=1)
    return amanha.replace(hour=1, minute=0, second=0, microsecond=0)

async def loop_boss():
    await bot.wait_until_ready()

    while not bot.is_closed():

        tempo = agora()
        boss = proximo_boss()

        espera = (boss - tempo).total_seconds()
        await asyncio.sleep(espera)

        canal = bot.get_channel(CANAL_BOSS)

        if canal:
            await canal.send("<@1481015294477733983>\n🔔 The Spirit Trials is up!! Run for it")

async def loop_shop():
    await bot.wait_until_ready()

    while not bot.is_closed():

        tempo = agora()
        shop = proximo_shop()

        espera = (shop - tempo).total_seconds()
        await asyncio.sleep(espera)

        canal = bot.get_channel(CANAL_SHOP)

        if canal:
            await canal.send("<@1481015294477733983>\n🔔 The Trial Shop is up!! Run for it")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    bot.loop.create_task(loop_boss())
    bot.loop.create_task(loop_shop())

    print("Comandos sincronizados no servidor")

@bot.tree.command(name="timetrial")
async def timetrial(interaction: discord.Interaction):

    tempo = agora()
    boss = proximo_boss()

    restante = boss - tempo
    total = int(restante.total_seconds())

    minutos = total // 60
    segundos = total % 60

    await interaction.response.send_message(f"⚔️ Next spirit in {minutos}m {segundos}s")

@bot.tree.command(name="timeshop")
async def timeshop(interaction: discord.Interaction):

    tempo = agora()
    shop = proximo_shop()

    restante = shop - tempo
    total = int(restante.total_seconds())

    horas = total // 3600
    minutos = (total % 3600) // 60

    await interaction.response.send_message(f"🛒 Next shop update in {horas}h {minutos}m")

@bot.tree.command(name="next")
async def next_event(interaction: discord.Interaction):

    tempo = agora()

    boss = proximo_boss()
    shop = proximo_shop()

    restante_boss = boss - tempo
    restante_shop = shop - tempo

    total_boss = int(restante_boss.total_seconds())
    total_shop = int(restante_shop.total_seconds())

    boss_min = total_boss // 60
    boss_sec = total_boss % 60

    shop_h = total_shop // 3600
    shop_m = (total_shop % 3600) // 60

    await interaction.response.send_message(
        f"⚔️ Spirit Trial: {boss_min}m {boss_sec}s\n🛒 Trial Shop: {shop_h}h {shop_m}m"
    )

bot.run(TOKEN)