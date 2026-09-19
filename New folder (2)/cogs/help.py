
import discord
from discord.ext import commands
import asyncio


class Help(commands.Cog):
    """📖 أمر المساعدة"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="cmds")
    async def cmds(self, ctx):
        """!cmds → عرض كل الأوامر"""
        try:
            await ctx.message.delete()
        except:
            pass

        text = """
# 📖 **Cherry Selfbot — كل الأوامر**

## 🎮 **الحالة** (`status.py`)
- `!setstatus play <لعبة>` — Playing
- `!setstatus listen <شي>` — Listening to
- `!setstatus watch <شي>` — Watching
- `!setstatus compete <شي>` — Competing in
- `!setstatus stream <عنوان>` — Streaming
- `!setstatus clear` — مسح
- `!setstream <url> [عنوان]` — Streaming مع رابط
- `!mystatus` — حالتك الحالية
- `!statustest` — اختبار كل الحالات

## 👤 **الحضور** (`status.py`)
- `!setonline` — 🟢 Online
- `!setidle` — 🌙 Idle
- `!setdnd` — ⛔ DND
- `!setinvisible` — 👻 Invisible

## 🗑️ **حذف الرسائل** (`purge.py`)
- `!purge` — حذف رسائلك في الروم الحالي
- `!purge <id> [limit]` — روم محدد
- `!purgeall [limit]` — من كل الرومات
- `!purgeeveryone <id> <limit> yes` — كل الرسائل ⚠️
- `!dms` — قائمة DMs
- `!chinfo [id]` — معلومات روم

## 🚫 **الحظر** (`block.py`)
- `!blockall` — عرض معلومات سيرفر
- `!blockall <guild_id> yes` — حظر الكل
- `!blockuser <user_id>` — عضو واحد
- `!blockids <id1> <id2>` — قائمة IDs
- `!unblockuser <user_id>` — فك حظر
- `!unblockall yes` — فك الكل
- `!blocklist [limit]` — عرض المحظورين
- `!blockcheck <user_id>` — هل محظور؟
- `!blockstats` — إحصائيات

## 📁 **الرومات** (`rooms.py`)
- `!mass_rooms <عدد> [اسم]` — إنشاء رومات كثيرة
- `!nuke_channels yes` — حذف كل الرومات ⚠️
- `!cleanup [prefix]` — حذف room-/chat-/temp-
- `!roomlist [prefix]` — عرض الرومات
- `!serverinfo` — معلومات السيرفر
- `!mkchannels <اسم1 | اسم2>` — إنشاء بأسماء
- `!clonech <عدد>` — نسخ الروم

## 💬 **mespam** (`spam.py`)
- `!mespam <وقت> <id> <رسالة>` — إرسال بحسابك
- `!mestop [id]` — إيقاف
- `!mestatus` — حالة الإرسالات
- `!mechange <id> <وقت>` — تغيير الوقت
- `!medel <id>/all yes` — حذف إعداد

## 🪝 **الويبوكات** (`webhooks.py`)
- `!hooks <عدد> [اسم]` — إنشاء ويبوكات
- `!rooms <عدد> [اسم] [رسالة]` — رومات + ربط + إرسال
- `!fire <وقت> <رسالة>` — إرسال متكرر
- `!stop` — إيقاف
- `!send <رسالة>` — إرسال مرة
- `!whlist [limit]` — عرض
- `!whstatus` — حالة
- `!whtest [رسالة]` — اختبار
- `!whdel <id>/all yes` — حذف
- `!whclear yes` — مسح القائمة

## 📝 **المراقبة** (`logger.py`)
- `!deleted [limit]` — الرسائل المحذوفة في DM
- `!requests [limit]` — طلبات الصداقة
- `!finddel <user_id>` — رسائل شخص محذوفة
- `!logstats` — إحصائيات
- `!cache [limit]` — الكاش
- `!clearlogs <deleted|requests|all> yes` — مسح

## 🤖 **الردود التلقائية** (`autoreply.py`)
- `!welcome set #ch <رسالة>` — ترحيب
- `!welcome off/status`
- `!trigger add <كلمة> | <رد1> | <رد2>`
- `!trigger react <كلمة> <emoji>`
- `!trigger del/list/clear`
- `!stalk add <user_id> | <رد>`
- `!stalk react/on/off/del/list`

## 🧠 **AI** (`ai.py`)
- `@حسابك ai <سؤال>` — اسأل AI
- (رد على البوت) `ai <سؤال>`
- `!ai <سؤال>` — مباشر
- `!aiset status/on/off/word/clear`
- `!aitest` — اختبار

## ⏱️ **صيغ الوقت**
`s` = ثانية | `m` = دقيقة | `h` = ساعة
`ث` | `د` | `س`

---

💡 **للتفاصيل:** `!help <أمر>`
"""

        # ─── لو طويل، نقسمه ───
        if len(text) > 1900:
            parts = [text[i:i+1900] for i in range(0, len(text), 1900)]
            for part in parts:
                await ctx.send(part)
                await asyncio.sleep(0.3)
        else:
            await ctx.send(text)

    # ═════════════════════════════════════════
    # 📖 help — مساعدة مفصلة
    # ═════════════════════════════════════════
    @commands.command(name="help")
    async def help_cmd(self, ctx, *, cmd: str = ""):
        """
        !help → قائمة الأقسام
        !help <قسم> → تفاصيل قسم
        """
        try:
            await ctx.message.delete()
        except:
            pass

        # ─── أقسام ───
        sections = {
            "status": """
🎮 **status.py — حالة الحساب**
- `!setstatus play <لعبة>` — Playing
- `!setstatus listen <شي>` — Listening
- `!setstatus watch <شي>` — Watching
- `!setstatus compete <شي>` — Competing
- `!setstatus stream <عنوان>` — Streaming
- `!setstatus clear` — مسح
- `!setstream <url> [عنوان]` — Streaming مع رابط
- `!mystatus` / `!statustest`
- `!setonline` / `!setidle` / `!setdnd` / `!setinvisible`
""",
            "purge": """
🗑️ **purge.py — حذف الرسائل**
- `!purge` — رسائلك في الروم
- `!purge <id> [limit]` — روم محدد
- `!purge <id> 0` — كل رسائلك
- `!purgeall [limit]` — كل الرومات
- `!purgeeveryone <id> <limit> yes` — ⚠️ كل الرسائل
- `!dms` — قائمة DMs
- `!chinfo [id]` — معلومات روم
""",
            "block": """
🚫 **block.py — الحظر**
- `!blockall` → عرض معلومات
- `!blockall <guild_id> yes` → حظر الكل
- `!blockuser <id>` → واحد
- `!blockids <id1> <id2>` → قائمة
- `!unblockall yes` → فك الكل
- `!blocklist` → عرض
- `!blockcheck <id>` → هل محظور؟
- `!blockstats` → إحصائيات
""",
            "rooms": """
📁 **rooms.py — الرومات**
- `!mass_rooms <عدد> [اسم]` — إنشاء كثير
- `!nuke_channels yes` — ⚠️ حذف الكل
- `!cleanup [prefix]` — حذف رومات
- `!roomlist [prefix]` — عرض
- `!serverinfo` — معلومات السيرفر
- `!mkchannels <اسم1 | اسم2>`
- `!clonech <عدد>`
""",
            "spam": """
💬 **spam.py — mespam**
- `!mespam <وقت> <channel_id> <رسالة>`
- `!mestop [channel_id]`
- `!mestatus`
- `!mechange <id> <وقت>`
- `!medel <id>/all yes`

**الأنسب:** `30s` أو أكثر
""",
            "webhooks": """
🪝 **webhooks.py — الويبوكات**
- `!hooks <عدد> [اسم]`
- `!rooms <عدد> [اسم] [رسالة]`
- `!fire <وقت> <رسالة>` 🔥
- `!stop`
- `!send <رسالة>`
- `!whlist` / `!whstatus` / `!whtest`
- `!whdel <id>/all yes`
- `!whclear yes`
""",
            "logger": """
📝 **logger.py — مراقبة DM**
- `!deleted [limit]` — الرسائل المحذوفة
- `!requests [limit]` — طلبات الصداقة
- `!finddel <user_id>` — رسائل شخص
- `!logstats` — إحصائيات
- `!cache [limit]` — الكاش
- `!clearlogs <deleted|requests|all> yes`
""",
            "autoreply": """
🤖 **autoreply.py — ردود تلقائية**
- `!welcome set #ch <رسالة>` — ترحيب
- `!welcome off/status`
- `!trigger add <كلمة> | <رد1> | <رد2>`
- `!trigger react <كلمة> <emoji>`
- `!trigger del/list/clear`
- `!stalk add <user_id> | <رد>`
- `!stalk on/off/del/list/react`
""",
            "ai": """
🧠 **ai.py — الذكاء الاصطناعي**
- `@حسابك ai <سؤال>` — منشن
- (رد على البوت) `ai <سؤال>`
- `!ai <سؤال>` — مباشر
- `!aiset status` — الحالة
- `!aiset on/off` — تشغيل/إيقاف
- `!aiset word <كلمة>` — تغيير
- `!aiset clear` — مسح السجل
- `!aitest` — اختبار
""",
        }

        if cmd:
            cmd_lower = cmd.lower().strip()
            if cmd_lower in sections:
                text = sections[cmd_lower]
                return await ctx.send(text)
            else:
                return await ctx.send(
                    f"❌ قسم غير معروف: `{cmd}`\n"
                    f"**الأقسام:**\n"
                    f"`status`, `purge`, `block`, `rooms`, `spam`,\n"
                    f"`webhooks`, `logger`, `autoreply`, `ai`"
                )

        
        text = """
**📖 Cherry Selfbot — الأقسام**

اكتب `!help <قسم>` للتفاصيل:

🎮 `status` — حالة الحساب
🗑️ `purge` — حذف الرسائل
🚫 `block` — الحظر
📁 `rooms` — الرومات
💬 `spam` — mespam
🪝 `webhooks` — الويبوكات
📝 `logger` — مراقبة DM
🤖 `autoreply` — ردود تلقائية
🧠 `ai` — ذكاء اصطناعي

💡 **لكل الأوامر:** `!cmds`
"""
        await ctx.send(text)


async def setup(bot):
    await bot.add_cog(Help(bot))