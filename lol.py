import discord
import requests
import time

cooldown_alerta = 43200  # 5 minutos
ultima_alerta = 0

TOKEN = "lol"
WEBHOOK_URL = "https://discord.com/api/webhooks/1463358857261744283/bY4QlYX3E__S0-GFSm1xY6IAZuig_znXKmnMyXs7hs15vTPl7Dl0KY71Wa59zgFzF35K"

ROL_ADMIN = 1374518001490989168
ROL_ALERTA = 1459203442634526873
ROL_OWNER = 1229789255874772994

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_message(message):
    global ultima_alerta

    if message.author.bot:
        return

    roles_usuario = [r.id for r in message.author.roles]

    if message.content == "!alerta":
        if ROL_ADMIN not in roles_usuario:
            await message.channel.send("❌ LOOOOL naco no tiene rol de ejecutivo o superior, chat tirenle tomates por gil ❌ :rofl: matate lowkey ")
            return

        if not isinstance(message.channel, discord.Thread):
            await message.channel.send("❌ Che pibardo este comando solo se puede usar en <#1372424131106050048> ❌")
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
    if message.content == "!dormir":
        if ROL_OWNER not in roles_usuario:
            await message.channel.send("❌ LOOOOL naco no eres lesya god o un admin jefe, no puedes usar este comando")
            return

        await message.channel.send("😴 Chau pibes me fui a ver one piezzZe")
        await bot.close()
bot.run(TOKEN)