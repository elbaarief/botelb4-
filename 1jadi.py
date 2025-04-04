import asyncio
import aiohttp
from telegram import Bot


# API key untuk Telegram bot
telegram_token = '7772885670:AAH2euuxLaE_xgfLOqnfM6613h3v3xPyLNQ'
chat_id = '8064298466'  # ID chat pribadi atau grup

# URL API CoinGecko
url = 'https://api.coingecko.com/api/v3/coins/markets'
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',  # Urutkan berdasarkan kapitalisasi pasar
    'per_page': 100,  # Maksimal 100 koin
    'page': 1,
}

# Fungsi untuk mengirim pesan ke Telegram (gunakan async)
async def send_to_telegram(message):
    bot = Bot(token=telegram_token)
    await bot.send_message(chat_id=chat_id, text=message)

# Fungsi untuk menilai potensi koin dan menghitung skor
def evaluate_coin_potential(coin):
    price_change_24h = coin.get('price_change_percentage_24h', 0)  # Default 0 jika tidak ada data
    total_volume = coin.get('total_volume', 0)
    market_cap = coin.get('market_cap', 1)  # Default 1 untuk menghindari pembagian nol

    # **Hitung skor dengan formula sederhana**
    score = abs(price_change_24h) * (total_volume / market_cap)

    return {
        "name": coin["name"],
        "symbol": coin["symbol"],
        "price_change_24h": price_change_24h,
        "total_volume": total_volume,
        "market_cap": market_cap,
        "score": score
    }

# Fungsi utama untuk mendapatkan data koin dan mengirim hasil terbaik ke Telegram
async def get_coin_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

            # Evaluasi semua koin dan hitung skor
            evaluated_coins = [evaluate_coin_potential(coin) for coin in data]

            # Pilih koin dengan skor tertinggi
            best_coin = max(evaluated_coins, key=lambda x: x["score"], default=None)

            if best_coin:
                # Format pesan untuk Telegram
                message = (
                    "?? *Rekomendasi Beli:*\n"
                    f"?? *Koin:* {best_coin['name']} ({best_coin['symbol']})\n"
                    f"?? *Perubahan Harga 24 Jam:* {best_coin['price_change_24h']:.2f}%\n"
                    f"?? *Volume:* {best_coin['total_volume']:,}\n"
                    f"?? *Market Cap:* {best_coin['market_cap']:,}\n"
                    f"? *Score:* {best_coin['score']:.6f}"
                )
                
                await send_to_telegram(message)

# Memanggil fungsi untuk mendapatkan data koin dan mengirim rekomendasi ke Telegram
if __name__ == "__main__":
    asyncio.run(get_coin_data())
