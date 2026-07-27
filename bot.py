import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "5431533133:AAEaGAayY-bB_vp_tliANMaZcNqvk-cNJJk"
WEBHOOK_URL = "https://synapse-bot-sx0w.onrender.com"

bot = Bot(token=TOKEN)
dp = Dispatcher()

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SYNAPSE // Institutional</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/geist/dist/fonts/geist.css">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg: #0a0a0a;
            --surface: #141414;
            --border: #262626;
            --text-primary: #fafafa;
            --text-secondary: #a3a3a3;
            --text-muted: #525252;
            --accent: #3b82f6;
            --success: #22c55e;
            --font-stack: "Geist", -apple-system, sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
        body {
            background-color: var(--bg);
            color: var(--text-primary);
            font-family: var(--font-stack);
            padding: 16px;
            max-width: 600px;
            margin: 0 auto;
            font-size: 15px;
            line-height: 1.5;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--text-primary);
        }
        .logo { font-size: 1.25rem; font-weight: 800; letter-spacing: -1px; text-transform: uppercase; }
        .header-right { display: flex; align-items: center; gap: 10px; }
        .user-id { font-size: 0.8rem; color: var(--text-secondary); font-weight: 500; }
        .status-dot { height: 8px; width: 8px; background-color: var(--success); border-radius: 50%; }
        
        .section-group { margin-bottom: 24px; }
        .section-title { font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 1px; font-weight: 600; margin-bottom: 12px; }
        
        .metrics-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1px;
            background-color: var(--border);
            border: 1px solid var(--border);
            border-radius: 6px;
            overflow: hidden;
        }
        .metric-item { background-color: var(--surface); padding: 12px; }
        .metric-label { font-size: 0.7rem; color: var(--text-secondary); margin-bottom: 4px; }
        .metric-value { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
        .metric-change { font-size: 0.7rem; font-weight: 600; color: var(--success); }

        .deal-list { display: flex; flex-direction: column; gap: 8px; }
        .deal-item {
            background-color: var(--surface);
            padding: 14px;
            border: 1px solid var(--border);
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .deal-name { font-weight: 600; font-size: 0.9rem; }
        .deal-meta { font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px; }
        .deal-pill { font-size: 0.65rem; text-transform: uppercase; color: var(--accent); border: 1px solid var(--border); padding: 1px 5px; border-radius: 3px; background: #0c0c0c; }
        .deal-price { font-weight: 700; font-size: 0.95rem; text-align: right; }

        .form-group { background-color: var(--surface); padding: 16px; border-radius: 6px; border: 1px solid var(--border); }
        .form-label { display: block; font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 6px; font-weight: 500; }
        input, select {
            width: 100%;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 10px;
            color: var(--text-primary);
            font-family: var(--font-stack);
            font-size: 14px;
            margin-bottom: 12px;
            outline: none;
        }
        input:focus, select:focus { border-color: var(--text-secondary); }
        .row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .btn-primary {
            width: 100%;
            background-color: var(--text-primary);
            color: var(--bg);
            border: none;
            border-radius: 4px;
            padding: 12px;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">SYNAPSE</div>
        <div class="header-right">
            <span class="user-id" id="tgUser">ID: AUTH</span>
            <span class="status-dot"></span>
        </div>
    </header>

    <div class="section-group">
        <div class="section-title">Сводка по контуру</div>
        <div class="metrics-row">
            <div class="metric-item">
                <div class="metric-label">Общий P&L</div>
                <div class="metric-value">$142k</div>
                <div class="metric-change">▲ 12.3%</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Связки</div>
                <div class="metric-value" id="dealsCount">4</div>
                <div class="metric-change" style="color:var(--text-muted)">актив</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Ликвидность</div>
                <div class="metric-value">$89.5k</div>
                <div class="metric-change" style="color:var(--text-muted)">баланс</div>
            </div>
        </div>
    </div>

    <div class="section-group">
        <div class="section-title">Приоритетные офферы</div>
        <div class="deal-list" id="feed"></div>
    </div>

    <div class="section-group">
        <div class="section-title">Регистрация новой связки</div>
        <div class="form-group">
            <label class="form-label">Asset / Вертикаль</label>
            <input type="text" id="titleInput" placeholder="Например: Nutra EU Direct">
            <div class="row-2">
                <div>
                    <label class="form-label">Тип</label>
                    <select id="categoryInput">
                        <option>CPA</option>
                        <option>RevShare</option>
                        <option>Direct</option>
                    </select>
                </div>
                <div>
                    <label class="form-label">Price ($)</label>
                    <input type="text" id="priceInput" placeholder="5000">
                </div>
            </div>
            <button class="btn-primary" onclick="publishDeal()">Верифицировать</button>
        </div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            document.getElementById('tgUser').innerText = 'ID: ' + tg.initDataUnsafe.user.id;
        }

        let deals = [
            { title: "EU Nutra Direct", category: "CPA", price: "$2,500", meta: "ROI: 240%" },
            { title: "TikTok Traffic Arbitrage", category: "Direct", price: "$4,000", meta: "Cap: $8k/wk" },
            { title: "Crypto Lead Gen Funnel", category: "RevShare", price: "$1,800", meta: "CR: 18%" }
        ];

        function render() {
            const feed = document.getElementById('feed');
            document.getElementById('dealsCount').innerText = deals.length;
            feed.innerHTML = '';
            deals.forEach(deal => {
                feed.innerHTML += `
                    <div class="deal-item">
                        <div>
                            <div class="deal-name">${deal.title}</div>
                            <div class="deal-meta"><span class="deal-pill">${deal.category}</span> — ${deal.meta}</div>
                        </div>
                        <div class="deal-price">${deal.price}</div>
                    </div>
                `;
            });
        }

        function publishDeal() {
            const title = document.getElementById('titleInput').value.trim();
            const category = document.getElementById('categoryInput').value;
            const price = document.getElementById('priceInput').value.trim();
            if (!title || !price) return;

            deals.unshift({
                title: title,
                category: category,
                price: price.startsWith('$') ? price : '$' + price,
                meta: "В контуре"
            });
            document.getElementById('titleInput').value = '';
            document.getElementById('priceInput').value = '';
            render();
        }
        render();
    </script>
</body>
</html>
"""

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="⚡ Открыть SYNAPSE Terminal", 
        web_app=types.WebAppInfo(url=WEBHOOK_URL)
    )
    await message.answer(
        "<b>SYNAPSE // Institutional Network</b>\n\nЗакрытый контур верифицированных связок. Доступ предоставлен.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

async def handle_index(request):
    return web.Response(text=HTML_CONTENT, content_type='text/html')

async def handle_webhook(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

async def main():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_post(f'/{TOKEN}', handle_webhook)
    
    # Устанавливаем вебхук в Telegram при старте
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"Webhook server started on port {port}...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
