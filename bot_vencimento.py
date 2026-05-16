import requests
import asyncio
from datetime import datetime
from telegram import Bot

# ===== CONFIG =====
API_KEY = "wz_9ac217bf88f72ac28ff2db4dd765aeac"

API_URL = "https://mcapi.knewcms.com:2087/lines"

TELEGRAM_TOKEN = "7725265862:AAG8zabzLDNOHf7WcUdkp5KqeECKObxDIiU"

CHAT_ID = "810476850"

DIAS_ALERTA = 5

# ===== BOT =====
bot = Bot(token=TELEGRAM_TOKEN)

# ===== HEADERS =====
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

async def verificar_clientes():

    response = requests.get(API_URL, headers=headers)

    print("STATUS:", response.status_code)

    dados = response.json()

    clientes = dados.get("items", [])

    hoje = datetime.now()

    for cliente in clientes:

        nome = cliente.get("notes", "Cliente")
        usuario = cliente.get("username", "")
        expira = cliente.get("exp_date", "")

        try:

            data_expira = datetime.fromisoformat(
                expira.replace("Z", "+00:00")
            )

            dias_restantes = (
                data_expira.replace(tzinfo=None) - hoje
            ).days

            if dias_restantes == 0:

                mensagem = f"""
⚠️ CLIENTE PRÓXIMO DO VENCIMENTO

👤 Cliente: {nome}
🔑 Usuário: {usuario}
📅 Vence em: {dias_restantes} dias
"""

                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=mensagem
                )

                print(f"Mensagem enviada para {nome}")

        except Exception as erro:
            print("Erro:", erro)

asyncio.run(verificar_clientes())