import disnake 
from disnake.ext import commands
                                                                         # id your server in []
bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all(), test_guilds=[])
bot.remove_command("help")

# your id mute role

MUTE_ROLE_ID = ""  




@bot.event
async def on_ready():
    print("Bot {bot.user} is ready to work!")

 
@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, id="id your server")

# И затем, если нужно дать роль:

    await member.add_roles(role)
    channel = bot.get_channel(1422268731484274738) # id welcome channel

    embed = disnake.Embed(
    title="Hello newbie!",
    description=f"{member.name}#{member.discriminator}",
    color=0xffffff
    )

    await member.add_roles(role)
    await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: disnake.Member, *, reason="violation of the rules."):
    await ctx.send(f"Administrator {ctx.author.mention} kicked the user {member.mention}", delete_after=5)
    await member.kick(reason=reason)
    await ctx.message.delete()


@bot.command(name="ban")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: disnake.Member, *, reason="violation of the rules."):
    await ctx.send(f"Administrator {ctx.author.mention} banned the user {member.mention}", delete_after=5)
    await member.ban(reason=reason)
    await ctx.message.delete()





@bot.command(name="mute")
async def mute(ctx, member: disnake.Member):
    mute_role = ctx.guild.get_role(MUTE_ROLE_ID)
    
    if not mute_role:
        await ctx.send("Mute role not found!", delete_after=5)
        return
    
    try:
        # add the mute role (always works)
        await member.add_roles(mute_role)
        
        # we only try to mute the user if they're in the voice channel
        if member.voice and member.voice.channel:
            await member.edit(mute=True)
        
        await ctx.send(f"Administrator {ctx.author.mention} has muted the user {member.mention}", delete_after=5)
    except Exception as e:
        await ctx.send(f"Error: {e}", delete_after=5)
    
    await ctx.message.delete()



    


@bot.command(name="unmute")
async def unmute(ctx, member: disnake.Member):
    mute_role = ctx.guild.get_role(MUTE_ROLE_ID)
    
    if not mute_role:
        await ctx.send("Mute role not found!", delete_after=5)
        return
    
    try:
        # removing the role of the muta
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
        
        # we only try to unmute if the user is in the voice channel
        if member.voice and member.voice.channel:
            await member.edit(mute=False)
        
        await ctx.send(f"Administrator {ctx.author.mention} has unmuted the user {member.mention}", delete_after=5)
    except Exception as e:
        await ctx.send(f"Error: {e}", delete_after=5)
    
    await ctx.message.delete()



@bot.command(name="help")
async def help_command(ctx):
    emb = disnake.Embed(title="List of Commands", color=disnake.Color.blue())
    
    emb.add_field(name=f"{bot.command_prefix}clear", value="Clearing the entire chat")
    emb.add_field(name=f"{bot.command_prefix}ban", value="Ban player")
    emb.add_field(name=f"{bot.command_prefix}kick", value="Kick player")
    emb.add_field(name=f"{bot.command_prefix}help", value="This message")
    emb.add_field(name=f"{bot.command_prefix}mute", value="Mute player")
    emb.add_field(name=f"{bot.command_prefix}unmute", value="Unmute player")
    
    await ctx.send(embed=emb)







@bot.command(pass_context = True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)



bot.run("your token")