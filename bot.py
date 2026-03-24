import asyncio
from telethon import TelegramClient, events

# بيانات الاعتماد (يجب ملؤها)
api_id = '20876095'
api_hash = '1f4d37b3efcc83e93ef897fde83955c7'

client = TelegramClient('session_name', api_id, api_hash)

# متغيرات التشغيل
target_groups = []
posting_delay = 300 
is_running = False

@client.on(events.NewMessage(pattern=r'\.الاوامر'))
async def show_commands(event):
    if not event.out: return # لضمان أنك فقط من يتحكم بالحساب
    text = (
        "📜 **نظام النشر التلقائي جاهز:**\n\n"
        "1️⃣ `.ف` : إضافة الجروب الحالي للقائمة.\n"
        "2️⃣ `.م` : حذف الجروب الحالي من القائمة.\n"
        "3️⃣ `.تصفير` : مسح كل الجروبات المضافة.\n"
        "4️⃣ `.هيا` : (بالرد) لبدء النشر التلقائي.\n"
        "5️⃣ `.و` + ثواني : ضبط الوقت (مثال: `.و 60`).\n"
        "6️⃣ `.ايقاف` : إيقاف النشر."
    )
    await event.respond(text)

@client.on(events.NewMessage(pattern=r'\.ف'))
async def add_group(event):
    if not event.out: return
    cid = event.chat_id
    if cid not in target_groups:
        target_groups.append(cid)
        await event.respond(f"✅ تمت إضافة الجروب: `{cid}`")

@client.on(events.NewMessage(pattern=r'\.م'))
async def remove_group(event):
    if not event.out: return
    cid = event.chat_id
    if cid in target_groups:
        target_groups.remove(cid)
        await event.respond(f"🗑️ تم حذف الجروب: `{cid}`")

@client.on(events.NewMessage(pattern=r'\.تصفير'))
async def clear_groups(event):
    if not event.out: return
    global target_groups
    target_groups = []
    await event.respond("🗑️ تم مسح القائمة بالكامل.")

@client.on(events.NewMessage(pattern=r'\.و (\d+)'))
async def set_delay(event):
    if not event.out: return
    global posting_delay
    posting_delay = int(event.pattern_match.group(1))
    await event.respond(f"⏳ الفاصل الزمني الحالي: {posting_delay} ثانية.")

@client.on(events.NewMessage(pattern=r'\.هيا'))
async def start_posting(event):
    if not event.out: return
    global is_running
    if not event.is_reply:
        await event.respond("❌ رد على رسالة بأمر `.هيا`")
        return
    if not target_groups:
        await event.respond("❌ القائمة فارغة! استخدم `.ف` أولاً.")
        return

    reply_msg = await event.get_reply_message()
    is_running = True
    await event.respond(f"🚀 بدأ النشر في {len(target_groups)} جروبات.")

    while is_running:
        for group in target_groups:
            if not is_running: break
            try:
                await client.send_message(group, reply_msg)
            except: pass
        await asyncio.sleep(posting_delay)

@client.on(events.NewMessage(pattern=r'\.ايقاف'))
async def stop_posting(event):
    if not event.out: return
    global is_running
    is_running = False
    await event.respond("🛑 توقف النشر.")

print("جاري تشغيل البوت...")
client.start()
client.run_until_disconnected()
