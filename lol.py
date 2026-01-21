import discord
import requests
import time
import os

cooldown_alerta = 43200  # 12 horas
cooldown_gg = 300        # 5 minutos

ultima_alerta = 0
ultimo_gg = 0

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

ROL_ADMIN = 1374518001490989168
ROL_ALERTA = 1380536099818176615
ROL_OWNER = 1229789255874772994

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    global ultima_alerta, ultimo_gg

    if message.author.bot:
        return

    roles_usuario = [r.id for r in message.author.roles]

    # ---------- COMANDO !alerta ----------
    if message.content == "!alerta":
        if ROL_ADMIN not in roles_usuario or ROL_ALERTA not in roles_usuario:
            await message.channel.send(
                "❌ LOOOOL naco no cumple los requisitos, necesitás **ROL_ADMIN Y ROL_ALERTA** ❌"
            )
            return

        if not isinstance(message.channel, discord.Thread):
            await message.channel.send(
                "❌ Che pibardo este comando solo se puede usar en <#1372424131106050048> ❌"
            )
            return

        ahora = int(time.time())
        restante = cooldown_alerta - (ahora - ultima_alerta)

        if restante > 0:
            await message.channel.send(
                f"Pará bro, recién hicieron ping hace **{restante} segundos**, aveces eres medio down."
            )
            return

        payload = {
            "content": f"<@&{ROL_ALERTA}> hoal pibes, I NEED THIS SO BAD ",
            "allowed_mentions": {
                "roles": [str(ROL_ALERTA)]
            }
        }

        requests.post(
            WEBHOOK_URL,
            params={"thread_id": message.channel.id},
            json=payload
        )

        ultima_alerta = ahora
        return

    # ---------- COMANDO !GG ----------
    if message.content == "!GG":
        ahora = int(time.time())
        restante = cooldown_gg - (ahora - ultimo_gg)

        if restante > 0:
            await message.channel.send(
                f"⏳ Calmado crack, esperá **{restante} segundos** antes de volver a humillar."
            )
            return

        texto_gg = (
            "GG EZ , cuando se le sube la dificulta a los bots? , fácil el tutorial , "
            "casi prendo el monitor , casi uso las manos , cuando empieza la pelea? , "
            "estuvo buena la orca referencia , porqué sigo peleando contra sandbag? , "
            "mi primo recien nacido juega mejor , git gud L + ratio + u have no bitches , "
            "ni al principito le dí tal leída , vato da más pelea , mejor me salgo del server "
            "sino voy a empeorar , si quieres te enseño como usar un teclado , me avisas "
            "cuando empieces a jugar enserio , mejor me voy a los hilos de r1muru que están "
            "más interesantes , voy a llamar al soporte, creo que el bot se rompió , "
            "ya no me hagan ping para jugar con muñecos de entrenamiento , saben cual es "
            "un temón? ESTE , me dormi a mitad de partida y aun asi gané , "
            "Thiago ni estando enfermo juega tan mal como tu , "
            "papunutria estaria decepcionado de lo inutil que eres🗿"
        )

        await message.channel.send(texto_gg)
        ultimo_gg = ahora
        return

    # ---------- COMANDO !dormir ----------
    if message.content == "!dormir":
        if ROL_OWNER not in roles_usuario:
            await message.channel.send(
                "❌ LOOOOL naco no eres lesya god o un admin jefe, no puedes usar este comando"
            )
            return

        await message.channel.send("😴 Chau pibes me fui a ver one piezzZe")
        await bot.close()

bot.run(TOKEN)
