import nextcord , json , datetime , discord
from nextcord.ext import commands
from nextcord import Intents, Status, Streaming

bot = commands.Bot(command_prefix = "!", help_command = None, intents = nextcord.Intents.all())

config = json.load(open('./config.json'))

class pok_modal(nextcord.ui.Modal):

   def __init__(self):
      super().__init__("ฝากบอก")
      self.a = nextcord.ui.TextInput(
         label = "คนที่อยากจะบอก",
         placeholder = "การใส่ userid จะเป็นการ @ คนนั้น",
         style = nextcord.TextInputStyle.short,
         required = True
      )
      self.b = nextcord.ui.TextInput(
         label = "ข้อความ",
         placeholder = "",
         style = nextcord.TextInputStyle.paragraph,
         required = True
      )
      self.c = nextcord.ui.TextInput(
         label = "คำใบ้",
         placeholder = "",
         style = nextcord.TextInputStyle.paragraph,
         required = True
      )
      self.add_item(self.a)
      self.add_item(self.b)
      self.add_item(self.c)

   async def callback(self, interaction: nextcord.Interaction):

      a = self.a.value

      a_len = len(a)
      a_cc = 0

      for i in a:
         if i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0':
            a_cc += 1

      if a_len == a_cc:
         user = f"<@{a}>"
      else:
         user = a

      embed = nextcord.Embed(description = f"**ข้อความ\n--->**    {str(self.b.value)}\n**คำใบ้จากผู้ส่ง\n--->**    {str(self.c.value)}", timestamp = datetime.datetime.now(), color = nextcord.Color.from_rgb(255,176,245))

      await bot.get_channel(int(config['channel-log'])).send(content = f'💜 ฝากบอกถึง {user}', embed = embed)

class pok_view(nextcord.ui.View):
   
   def __init__(self):
      super().__init__(timeout=None)

   @nextcord.ui.button(label = 'ฝากบอก', emoji = '💌', custom_id = 'victoria', style = nextcord.ButtonStyle.blurple, disabled = False)
   async def victoria(self, button: nextcord.Button, interaction: nextcord.Interaction):
      await interaction.response.send_modal(pok_modal())

@bot.event
async def on_ready():
    stream_url = "https://www.twitch.tv/phuttwat_pot"  # Replace with your stream URL
    game = discord.Game("Streaming on Twitch")
    await bot.change_presence(activity=discord.Streaming(name="My Stream", url=stream_url, details="บอทฝากบอก"), status=discord.Status.online)


@bot.slash_command(name = 'setup', description = 'phuttawat#0001')
async def setup(interaction: nextcord.Interaction):
   if nextcord.utils.get(interaction.user.guild.roles, id = int(config['role-admin'])) in interaction.user.roles :
      await interaction.response.send_message(content = 'สำเร็จ', ephemeral = True)
      embed = nextcord.Embed(title = 'กดปุ่มด้านล่างเพื่อฝากบอก', color = nextcord.Color.from_rgb(255,176,245))
      embed.set_image(url='')
      await interaction.channel.send(embed = embed, view = pok_view())

bot.run(config['token'])