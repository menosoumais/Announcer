import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

TOKEN = "MTQ4MTQ3MzgwODU4MDg3NDMwMQ.GBzX6D.RiMUivxmqyjn5uexhkPBAegJzL_xLD-AkSpYK0""

CANAL_BOSS = 1481485483619123281
CANAL_SHOP = 1481485503609045105

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def proximo_boss():
    agora = datetime.now()
    proximo = agora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return proximo


def proximo_shop():
    agora = datetime.now()

    horas_shop = [1,5,9,13,17,21]

    for h in horas_shop:
        proximo = agora.replace(hour=h, minute=0, second=0, microsecond=0)
        if proximo > agora:
            return proximo

    return agora.replace(day=agora.day+1, hour=1, minute=0, second=0, microsecond=0)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    checar_tempo.start()


@tasks.loop(seconds=30)
async def checar_tempo():

    agora = datetime.now()

    boss = proximo_boss()
    shop = proximo_shop()

    if (boss - agora).total_seconds() <= 30:
        canal = bot.get_channel(CANAL_BOSS)
        if canal:
            await canal.send("🔔 The Spirit boss is active!!")

    if (shop - agora).total_seconds() <= 30:
        canal = bot.get_channel(CANAL_SHOP)
        if canal:
            await canal.send("🔔 The Trial Shop is up!! Run for it")


@bot.command()
async def time_boss(ctx):

    agora = datetime.now()
    boss = proximo_boss()

    restante = boss - agora

    minutos = restante.seconds // 60
    segundos = restante.seconds % 60

    await ctx.send(f"Next spirit in {minutos}m {segundos}s")


@bot.command()
async def time_shop(ctx):

    agora = datetime.now()
    shop = proximo_shop()

    restante = shop - agora

    horas = restante.seconds // 3600
    minutos = (restante.seconds % 3600) // 60

    await ctx.send(f"Next shop update in {horas}h {minutos}m")


bot.run(TOKEN)