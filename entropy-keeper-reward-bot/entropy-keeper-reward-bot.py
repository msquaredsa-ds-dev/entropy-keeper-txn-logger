#!/usr/bin/python3

from audioop import add
import os
import discord
from discord.ext import commands
import pandas as pd


TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='rewards')
async def show_keeper_rewards(ctx, entropy_keeper_address):
	
    # get current cumulative rewards for the entropy keepers program
    df = pd.read_parquet('gs://entropy-rewards/cumulative/current-total-rewards.parquet')

    # extract variables to return in the bot message
    user_rewards = df[df['entropy_keeper_address'] == entropy_keeper_address].iloc[0]['total_keeper_reward']
    as_of_date = df[df['entropy_keeper_address'] == entropy_keeper_address].iloc[0]['as_of_date']

    await ctx.channel.send("Your wallet has earned {:,.2f} entropy tokens as of {} 23:59:59 UTC".format(user_rewards, as_of_date))

@bot.command(name='stats')
async def show_keeper_stats(ctx, entropy_keeper_address):

    # get current keeper stats for a given keeper address
    df = pd.read_parquet('gs://entropy-rewards/cumulative/current-keeper-stats.parquet')
    address_df = df[df['entropy_keeper_address'] == entropy_keeper_address]


    # write message
    response = """
 
    :zap: **GENERAL** :zap:
    * __First Keeper Day__: {}
    * __Number of Days Keeping__: {}

    :moneybag: **REWARDS** :moneybag:
    *Consume Events*
    * __Average Daily Rewards__: {:,.2f}
    * __Highest Single Day Earning__s: {:,.2f}
    * __Lowest Single Day Earnigns__: {:,.2f}

    *Other Events*
    * __Average Daily Rewards__: {:,.2f}
    * __Highest Single Day Earnings__: {:,.2f}
    * __Lowest Single Day Earnigns__: {:,.2f}

    **PERCENTAGE OF TIME**

    """.format(
        address_df['first_keeper_day'].iloc[0],
        address_df['number_of_days_keeping'].iloc[0],
        address_df['avg_daily_consume_events_reward'].iloc[0],
        address_df['best_consume_events_reward'].iloc[0],
        address_df['worst_consume_events_reward'].iloc[0],
        address_df['avg_daily_other_events_reward'].iloc[0],
        address_df['best_other_events_reward'].iloc[0],
        address_df['worst_other_events_reward'].iloc[0]
    )

    await ctx.channel.send(response)

bot.run(TOKEN)