import discord
from discord.ext import commands
from config import DATABASE, TOKEN
from logic import DatabaseManager

# Ganti "YOUR_BOT_TOKEN" dengan token botmu
manager = DatabaseManager(DATABASE)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Prefix perintah
bot = commands.Bot(command_prefix='!', intents=intents)

# Event yang terpicu ketika bot siap
@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} siap bekerja!')

# Event yang terpicu ketika anggota baru bergabung
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='umum')
    if channel:
        await channel.send(f'Selamat datang di server, {member.mention}!')

# Respon sederhana untuk perintah !ping
@bot.command()
async def get_random_games(ctx):
    data = manager.get_random_games()
    for name in data:
        await ctx.send(name[0])

# Perintah !hello yang merespon dengan mention pengguna
@bot.command()
async def get_good_games(ctx):
    data = manager.get_good_games(10)
    for row in data:
        await ctx.send(f'{row[0]} : {row[1]}')

# Perintah !echo yang mengulangi pesan pengguna
@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

# Penanganan kesalahan perintah
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Harap tentukan semua argumen yang diperlukan.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Perintah tidak ditemukan.')
    else:
        await ctx.send('Terjadi kesalahan saat menjalankan perintah.')

# Jalankan bot
bot.run(TOKEN)