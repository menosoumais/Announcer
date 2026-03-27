# -*- coding: utf-8 -*-import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import os

TOKEN = os.getenv("TOKEN")

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
        await asyncio.sleep(max(espera, 0))

        canal = bot.get_channel(CANAL_BOSS)

        if canal:
            embed = discord.Embed(
                title="⚔️ Spirit Trial Available",
                description="Run for it!",
                color=discord.Color.red()
            )
            embed.set_footer(text="Spirit Tracker")

            await canal.send(
                content="||<@&1481015294477733983>||",
                embed=embed
            )

async def loop_shop():
    await bot.wait_until_ready()

    while not bot.is_closed():
        tempo = agora()
        shop = proximo_shop()

        espera = (shop - tempo).total_seconds()
        await asyncio.sleep(max(espera, 0))

        canal = bot.get_channel(CANAL_SHOP)

        if canal:
            embed = discord.Embed(
                title="🛒 Trial Shop Available",
                description="Run for it!",
                color=discord.Color.gold()
            )
            embed.set_footer(text="Spirit Tracker")

            await canal.send(
                content="||<@&1481015294477733983>||",
                embed=embed
            )

async def setup_hook():
    print("Iniciando setup...")

    await bot.tree.sync()

    bot.loop.create_task(loop_boss())
    bot.loop.create_task(loop_shop())

    print("Tudo sincronizado e loops iniciados ✅")

@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):

    await interaction.response.send_message(
        "🚀 Enviando todas as mensagens de teste...",
        ephemeral=True
    )

    canal_boss = bot.get_channel(CANAL_BOSS)
    canal_shop = bot.get_channel(CANAL_SHOP)

    if canal_boss:
        embed_boss = discord.Embed(
            title="⚔️ Spirit Trial Available",
            description="Run for it!",
            color=discord.Color.red()
        )
        embed_boss.set_footer(text="Spirit Tracker")

        await canal_boss.send(
            content="||<@&1481015294477733983>||",
            embed=embed_boss
        )

    if canal_shop:
        embed_shop = discord.Embed(
            title="🛒 Trial Shop Available",
            description="Run for it!",
            color=discord.Color.gold()
        )
        embed_shop.set_footer(text="Spirit Tracker")

        await canal_shop.send(
            content="||<@&1481015294477733983>||",
            embed=embed_shop
        )
@bot.tree.command(name="timetrial")
async def timetrial(interaction: discord.Interaction):

    tempo = agora()
    boss = proximo_boss()

    restante = boss - tempo
    total = int(restante.total_seconds())

    minutos = total // 60
    segundos = total % 60

    embed = discord.Embed(
        title="⚔️ Spirit Trial",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Next spawn",
        value=f"{minutos}m {segundos}s",
        inline=False
    )

    embed.set_footer(text="Spirit Tracker")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timeshop")
async def timeshop(interaction: discord.Interaction):

    tempo = agora()
    shop = proximo_shop()

    restante = shop - tempo
    total = int(restante.total_seconds())

    horas = total // 3600
    minutos = (total % 3600) // 60

    embed = discord.Embed(
        title="🛒 Trial Shop",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Next update",
        value=f"{horas}h {minutos}m",
        inline=False
    )

    embed.set_footer(text="Spirit Tracker")

    await interaction.response.send_message(embed=embed)

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

    embed = discord.Embed(
        title="📅 Event Tracker",
        description="Current event timers",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="⚔️ Spirit Trial",
        value=f"{boss_min}m {boss_sec}s",
        inline=False
    )

    embed.add_field(
        name="🛒 Trial Shop",
        value=f"{shop_h}h {shop_m}m",
        inline=False
    )

    embed.set_footer(text="Spirit Tracker")

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)