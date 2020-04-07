import discord
from discord.ext import commands, tasks
from discord.utils import get, asyncio
import youtube_dl
import random
from itertools import cycle
import os
import shutil
 

client = commands.Bot(command_prefix='.')
status = cycle(['Doom Eternal', 'Smash Ultimate', 'Animal Crossing', 'Duck Game'])
players = {}

@client.event 
async def on_ready():
    #await client.change_presence(status=discord.Status.online, activity=discord.Game('Sup bitch'))
    print("Hi! I´m NutCracker")
    change_status.start()

@client.event 
async def on_member_join(member):
    print(f"Hi {member}, welcome to the server!")

@client.event 
async def on_member_remove(member):
    print(f"{member} has left the server ")


#?Tasks
@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
    

#?Commands
@client.command(aliases=['Marco'])
async def marco(ctx):
    await ctx.send(f'Polo!')
@client.command(aliases=['quien es Marselo?', 'quien es marselo?', 'Marselo'])
async def marselo(ctx):
    await ctx.send('Agachate y conocelo')
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms ')

@client.command(aliases=['multi'])
async def multiply(ctx, n1, n2):
    await ctx.send(f'Eso es: {n1 * n2} ')

@client.command(aliases=['divi'])
async def divide(ctx, n1, n2):
    await ctx.send(f'Eso es: {n1 / n2} ')

@client.command(aliases=['pred', 'Predict', 'Pred'])
async def predict(ctx, *, question):
    respuestas=['Si', 'No', 'Ni de pedo', 'Ahuevo que si', 
    'Jaja lo dudo', 'Puede ser...', 'La verdad no creo', 
    'Yo digo que simon', 'No se jaja']
    await ctx.send(f'Pregunta-> {question}\nRespuesta: {random.choice(respuestas)}')

@predict.error
async def predict_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in a question')

@client.command()
async def join(ctx):
    print('joined voice channel')
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
        print('joined voice channel')
    else:
        voice = await channel.connect()
        print('joined voice channel')
    await ctx.send('NutCracker is in the house bitchzz')


@client.command()
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'left the voice channel {channel}')
        await ctx.send(f'NutCracker left the voice channel')
    else:
        await ctx.send('Not in a voice channel')

@client.command(aliases=['plei', 'dj', 'ponestarolawe'])
async def play(ctx, url : str):
    def check_queue():
        Queue_infile = os.path.isdir('./Queue')
        if Queue_infile:
            Dir = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(Dir))
            still_g = length - 1
            try:
                first_file = os.listdir(Dir)[0]
            except:
                print('No more songs in queue')
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                print('Playing next song in queue')
                print(f'Songs in queue {still_g} ')
                song_there = os.path.isfile('song.mp3')
                if song_there:
                    os.remove('song.mp3')
                shutil.move(song_path, main_location)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.value = 0.08
            else:
                queues.clear()
                return
        else:
            queues.clear()
            print('No more songs were queued')              

    song = os.path.isfile('song.mp3')
    try:
        if song:
            os.remove('song.mp3')
            queues.clear()
            print('Old song removed')
    except PermissionError:
        print('Failed try of song deletion')
        await ctx.send('Error in music player')
        return

    Queue_infile = os.path.isdir('./Queue')
    try:
        Queue_folder = './Queue'
        if Queue_infile is True:
            print('Removed old Queue folder')
            shutil.rmtree(Queue_folder)
    except:
        print('No old Queue folder')

    await ctx.send('Ahí va')

    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec":"mp3",
            "preferredquality":"192"
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio')
        ydl.download([url])
    
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print('Renamed file: ', file)
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.08

    Nn = name.rsplit('-', 2)
    await ctx.send(f'{Nn}')
    print('playing')
    
@client.command(aliases=['pausa'])
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print('Music paused')
        voice.pause()
        await ctx.send('Pausa')
    else:
        print('No music playing')
        await ctx.send('No hay nada que pausar')

@client.command(aliases=['r'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print('Retomando musica')
        voice.resume()
        await ctx.send('Ahi va de nuevo')
    else:
        print('No hay nada pausado')
        await ctx.send('No hay nada pausado')

@client.command(aliases=['para', 'quitalarolawe'])
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print('Music stopped')
        voice.stop()
        await ctx.send('Quitada')
    else:
        print('No music playing')
        await ctx.send('No hay nada que parar')

queues = {}
@client.command(aliases=['q'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir('./Queue')
    if Queue_infile is False:
        os.mkdir('Queue')
    Dir = os.path.abspath(os.path.realpath('Queue'))
    q_num = len(os.listdir(Dir))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num +=1
        else:
            add_queue = False
            queues[q_num] = q_num
    queue_path = os.path.abspath(os.path.realpath('Queue') + f"\song{q_num}.%(ext)s ")
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "outtmpl": queue_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec":"mp3",
            "preferredquality":"192"
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio')
        ydl.download([url])

    await ctx.send('Added '+ str(q_num) + ' to queue')
    print('Added to queue')



@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banneado {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Desbanneado {user.mention}')
            return

@client.command(aliases=['dharma', 'aniversario'])
async def Dharma(ctx):
    await ctx.send('Puedes creer que llevamos ya un año? Mas el tiempo anterior, son ya prácticamente 5 años conociendonos y compartiendo.')
    await asyncio.sleep(3)
    await ctx.send('Hemos crecido, hemos cambiado y aquí seguimos, no sonaré pretencioso diciendo que si ya pudimos con esto podemos con todo sin problema, pero si que es prueba de que somos buen equipo, y me has enseñado a trabajar contigo, quiero que trabajes tambien bien conmigo, y quiero seguir en este equipo, empiezo a entender que el amor no es solo compartir tiempo con alguien, ni siquiera es entenderlos, es aceptarlos, ayudarlos, apoyarlos y colaborar en.. la vida.')
    await asyncio.sleep(5)
    await ctx.send('Amar no es solo querer, porque querer es egoísta, es querer que la otra persona esté bien y ver por ella, y bueno es fácil decirlo, estoy sentado en mi cuarto mientras lo escribo, pero antes mi percepción de amor era más egoísta y sin embargo creía que era más apasionada, veía por mi placer final, hacer esto para que esa persona este conmigo, como una presa y trampas, ahora lo veo como alguien que quiero que suba en las escaleras de la vida jaja y ponerle escalones, tampoco quiero que pienses que siempre fue así mi manera de amar, puramente egoísta, y nunca tuve tintes de este amor no egoísta, pero lo que sí es que no era tan consciente, ahora lo soy más.')
    await asyncio.sleep(5)
    await ctx.send('Tambien quiero decirte que estoy muy agradecido por que me escuchas y estas para mi, quiero ser recíproco.')
    await asyncio.sleep(3)
    await ctx.send('Y con esto, espero sigamos funcionando como pareja por un largo tiempo, hasta que otra pandemia nos exterminé o hasta que nuestras consciencias trasciendan ya sea fuera del mundo físico o dentro de una supercomputadora donde podramos disfrutar de una existencia desmaterializada, jajaja te amo Dharma, quiero seguir haciendolo y quiero divertirme y ser feliz a tu lado, y quiero que tu lo estés y lo seas también, quiero que cumplas todas tus metas, te apoyaré y ayudaré en lo que pueda, aquí estoy. ~Diego\n')
    await asyncio.sleep(3)
    await ctx.send('Y si, lo último son puras peticiones de mi ego, no he podido desprender el amor de mi ego, pero poco a poco, y mientras no hagan daño y vean por tu bien, se lo concedo.')

client.run('NjkxMDkwNDA0MTcwNTMwOTEy.Xna65g.bP9QqVYyduykJX6pg2DWrm1wNWY')