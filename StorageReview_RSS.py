import feedparser
import discord
from discord import app_commands
from discord.ext import commands, tasks

# Making the bot
#intents = discord.Intents.all()
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# Storage
lasttitle = "none"

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Storage Review"))
    #await bot.change_presence(activity=discord.CustomActivity(name="Flight Restrictions"))
    rss_feed.start()
    print(f"Logged in as {bot.user}")
    status_ch = bot.get_channel(1124134650227474483)
    await status_ch.send(f"***{bot.user} has Started***")

@tasks.loop(seconds=60)
async def rss_feed():
    global lasttitle
    status_ch = bot.get_channel(1124134650227474483)
    post_ch = bot.get_channel(915058337333276705)

    NewsFeed = feedparser.parse("https://www.storagereview.com/rss.xml")
    #NewsFeed = feedparser.parse("https://moxie.foxnews.com/google-publisher/latest.xml")
    # print("Number of RSS posts :", len(NewsFeed.entries))
    entry = NewsFeed.entries[0]

    if lasttitle == "none":
        lasttitle = entry.title
        message = f"""***{entry.title}***
{entry.link}"""
        await status_ch.send(message)
        
    elif entry.title != lasttitle:
        lasttitle = entry.title
        #print('Post Title :',entry.title)
        message = f"""***{entry.title}***
{entry.link}"""
        await post_ch.send(message)
#    else:
#       print("No Change")

bot.run("TOKEN")
