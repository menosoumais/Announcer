import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import os

TOKEN = os.getenv("TOKEN")

CANAL_BOSS = 1481485483619123281
CANAL_SHOP = 1481485503609045105

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


def proximo_boss():
    agora = datetime.now()
    return agora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)


def proximo_shop():
    agora = datetime.now()
    horarios = [1, 5, 9, 13, 17, 21]

    for h in horarios:
        proximo = agora.replace(hour=h, minute=0, second=0, microsecond=0)
        if agora < proximo:
            return proximo

    amanha = agora + timedelta(days=1)
    return amanha.replace(hour=1, minute=0, second=0, microsecond=0)


async def loop_boss():
    await bot.wait_until_ready()
    while not bot.is_closed():

        agora = datetime.now()
        boss = proximo_boss()

        espera = (boss - agora).total_seconds()
        await asyncio.sleep(espera)

        canal = bot.get_channel(CANAL_BOSS)
        if canal:
            await canal.send(
                "<@1481015294477733983>\n⚔️ The Spirit is up!"
            )


async def loop_shop():
    await bot.wait_until_ready()
    while not bot.is_closed():

        agora = datetime.now()
        shop = proximo_shop()

        espera = (shop - agora).total_seconds()
        await asyncio.sleep(espera)

        canal = bot.get_channel(CANAL_SHOP)
        if canal:
            await canal.send(
                "<@1481015294477733983>\n🛒 The Trial Shop is up!! Run for it"
            )


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(loop_boss())
    bot.loop.create_task(loop_shop())


@bot.command()
async def timeboss(ctx):

    agora = datetime.now()
    boss = proximo_boss()

    restante = boss - agora
    total = int(restante.total_seconds())

    minutos = total // 60
    segundos = total % 60

    await ctx.send(f"Next spirit in {minutos}m {segundos}s")


@bot.command()
async def timeshop(ctx):

    agora = datetime.now()
    shop = proximo_shop()

    restante = shop - agora
    total = int(restante.total_seconds())

    horas = total // 3600
    minutos = (total % 3600) // 60

    await ctx.send(f"Next shop update in {horas}h {minutos}m")


bot.run(TOKEN)