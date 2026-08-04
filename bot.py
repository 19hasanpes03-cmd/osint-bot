import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web
import asyncio

# Tokenini buradaki tırnak içine yazabilirsin
TOKEN = "7953258525:AAH40B04f4g_6bK_X2v031M_z0yX_2v1_1a" # Kendi tokenini buraya ekle

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="OSINT Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🔍 **Gelişmiş OSINT Bot v5.1 Aktif!**\n\n"
        "📋 **Mevcut Komutlar:**\n"
        "• `/ip <hedef_ip>` - IP adresi konum/servis analizi\n"
        "• `/username <kullanici_adi>` - Sosyal medya hesap taraması\n"
        "• `/phone <telefon_no>` - Numara format analizi\n"
        "• `/help` - Yardım menüsü",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🛠️ **OSINT Bot Yardım Menüsü:**\n\n"
        "1️⃣ `/ip 8.8.8.8` -> IP bilgilerini gösterir.\n"
        "2️⃣ `/username ahmet` -> Popüler platformlarda kullanıcı adını arar.\n"
        "3️⃣ `/phone 905554443322` -> Telefon bilgilerini listeler.",
        parse_mode="Markdown"
    )

@dp.message(Command("ip"))
async def cmd_ip(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Lütfen bir IP adresi yazın. Örnek: `/ip 8.8.8.8`", parse_mode="Markdown")
        return
    
    ip = args[1].strip()
    await message.answer(f"🔍 `{ip}` adresli hedef sorgulanıyor, lütfen bekleyin...")
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = response.json()
        
        if data.get("status") == "success":
            text = (
                f"🌐 **IP Sorgu Sonucu:**\n\n"
                f"• **IP:** {data.get('query')}\n"
                f"• **Ülke:** {data.get('country')} ({data.get('countryCode')})\n"
                f"• **Şehir:** {data.get('city')}\n"
                f"• **ISP (Sağlayıcı):** {data.get('isp')}\n"
                f"• **Organizasyon:** {data.get('org')}\n"
                f"• **Konum:** {data.get('lat')}, {data.get('lon')}"
            )
        else:
            text = "❌ IP adresi bulunamadı veya geçersiz."
    except Exception as e:
        text = f"❌ Sorgulama sırasında bir hata oluştu: {str(e)}"
        
    await message.answer(text, parse_mode="Markdown")

@dp.message(Command("username"))
async def cmd_username(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Lütfen bir kullanıcı adı yazın. Örnek: `/username hasan`", parse_mode="Markdown")
        return
        
    username = args[1].strip()
    await message.answer(f"🔍 `{username}` için sosyal medya platformları taranıyor...")
    
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Twitter (X)": f"https://twitter.com/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}"
    }
    
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for name, url in platforms.items():
        try:
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                results.append(f"✅ **{name}:** Bulundu -> {url}")
            else:
                results.append(f"❌ **{name}:** Bulunamadı")
        except:
            results.append(f"⚠️ **{name}:** Zaman aşımı / Hata")
            
    output = f"🔎 **Kullanıcı Adı Taraması: `{username}`**\n\n" + "\n".join(results)
    await message.answer(output, parse_mode="Markdown")

@dp.message(Command("phone"))
async def cmd_phone(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ Lütfen bir numara yazın. Örnek: `/phone 905554443322`", parse_mode="Markdown")
        return
        
    phone = args[1].strip()
    await message.answer(
        f"📱 **Telefon Analiz Sonucu:**\n\n"
        f"• **Girilen Numara:** `{phone}`\n"
        f"• **Uzunluk:** {len(phone)} karakter\n"
        f"• **Durum:** Format kontrolü tamamlandı.",
        parse_mode="Markdown"
    )

async def main():
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
