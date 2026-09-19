
import discord
from discord.ext import commands
import json
import os
import aiohttp
import asyncio



API_PROVIDER = "groq"
API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_MODEL = "openai/gpt-oss-120b"

DATA_DIR = "cherry_data"
AI_FILE = os.path.join(DATA_DIR, "ai_config.json")

SYSTEM_PROMPT = (
    "أنت مساعد ذكي مختصر. "
    "رد بالعربي بإجابات قصيرة ومفيدة. "
    "لو السؤال بالإنجليزي، رد بالإنجليزي."
)

MAX_HISTORY = 10    
MAX_TOKENS = 800    
class AI(commands.Cog):
    """🤖 رد بالذكاء الاصطناعي"""

    def __init__(self, bot):
        self.bot = bot
        self.config = {}
        os.makedirs(DATA_DIR, exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(AI_FILE):
            try:
                with open(AI_FILE, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = {}

        self.config.setdefault("enabled", True)
        self.config.setdefault("trigger_word", "ai")
        self.config.setdefault("history", {})
        self._save()

    def _save(self):
        try:
            with open(AI_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass

    async def ask_ai(self, user_id: str, question: str) -> str:
        """يرسل السؤال للـ API ويرجّع الرد"""

  
        history = self.config.get("history", {}).get(user_id, [])

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history[-MAX_HISTORY:])
        messages.append({"role": "user", "content": question})

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": API_MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7,
        }

      
        try:
            timeout = aiohttp.ClientTimeout(total=45)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(API_URL, headers=headers, json=payload) as resp:

                   
                    if resp.status == 401:
                        return "❌ مفتاح API غلط أو منتهي"
                    if resp.status == 429:
                        return "⏳ تم تجاوز الحد (Rate Limit). جرب بعد شوي"
                    if resp.status != 200:
                        err = await resp.text()
                        return f"❌ خطأ API ({resp.status}):\n```{err[:200]}```"

                   
                    data = await resp.json()
                    reply = data["choices"][0]["message"]["content"].strip()

                    if "history" not in self.config:
                        self.config["history"] = {}
                    if user_id not in self.config["history"]:
                        self.config["history"][user_id] = []

                    self.config["history"][user_id].append(
                        {"role": "user", "content": question}
                    )
                    self.config["history"][user_id].append(
                        {"role": "assistant", "content": reply}
                    )

                    max_msgs = MAX_HISTORY * 2
                    self.config["history"][user_id] = self.config["history"][user_id][-max_msgs:]
                    self._save()

                    return reply

        except asyncio.TimeoutError:
            return "⏳ AI تأخر بالرد. جرب مرة ثانية"
        except aiohttp.ClientError as e:
            return f"❌ خطأ اتصال: `{e}`"
        except Exception as e:
            return f"❌ خطأ: `{type(e).__name__}: {e}`"

    @commands.Cog.listener()
    async def on_message(self, message):

        # تجاهل
        if not self.config.get("enabled", True):
            return
        if message.author.id == self.bot.user.id:
            return
        if message.author.bot:
            return
        if message.content.startswith("!"):
            return

        mentioned_me = self.bot.user in message.mentions

        replied_to_me = False
        if message.reference:
            try:
                ref = await message.channel.fetch_message(message.reference.message_id)
                if ref.author.id == self.bot.user.id:
                    replied_to_me = True
            except:
                pass

        if not (mentioned_me or replied_to_me):
            return

        content = message.content
        content = content.replace(f"<@{self.bot.user.id}>", "")
        content = content.replace(f"<@!{self.bot.user.id}>", "")
        content = content.strip()

        trigger = self.config.get("trigger_word", "ai").lower()

        if not content.lower().startswith(trigger):
            return

        question = content[len(trigger):].strip()

        if not question:
            try:
                await message.reply(
                    f"❌ اكتب سؤال بعد `{trigger}`\n"
                    f"مثال: `{trigger} ايش عاصمة السعودية؟`",
                    mention_author=False
                )
            except:
                pass
            return

        try:
            async with message.channel.typing():
                reply = await self.ask_ai(str(message.author.id), question)
        except:
            reply = await self.ask_ai(str(message.author.id), question)

        await self._send_reply(message, reply)

    async def _send_reply(self, message, reply):
        """يرسل الرد — يقسم لو طويل"""
        if len(reply) > 1900:
            parts = [reply[i:i+1900] for i in range(0, len(reply), 1900)]
            for part in parts:
                try:
                    await message.reply(part, mention_author=False)
                except:
                    try:
                        await message.channel.send(part)
                    except:
                        pass
                await asyncio.sleep(0.3)
        else:
            try:
                await message.reply(reply, mention_author=False)
            except:
                try:
                    await message.channel.send(reply)
                except:
                    pass

    @commands.command(name="ai")
    async def ai_cmd(self, ctx, *, question: str = ""):
        """!ai <سؤال> → اسأل AI"""
        try:
            await ctx.message.delete()
        except:
            pass

        if not question.strip():
            return await ctx.send("❌ اكتب سؤال")

        msg = await ctx.send("🤔 يفكر...")

        reply = await self.ask_ai(str(ctx.author.id), question)

        if len(reply) > 1900:
            try:
                await msg.delete()
            except:
                pass
            parts = [reply[i:i+1900] for i in range(0, len(reply), 1900)]
            for part in parts:
                await ctx.send(part)
                await asyncio.sleep(0.3)
        else:
            try:
                await msg.edit(content=reply)
            except:
                await ctx.send(reply)

    @commands.command(name="aiset")
    async def aiset(self, ctx, action: str = "status", *, value: str = ""):
        """
        !aiset status → عرض الحالة
        !aiset on / off → تفعيل/إيقاف
        !aiset word <كلمة> → تغيير كلمة التشغيل
        !aiset clear → مسح سجل المحادثات
        """
        try:
            await ctx.message.delete()
        except:
            pass

        action = action.lower()

        if action == "status":
            enabled = "🟢 شغال" if self.config.get("enabled") else "🔴 متوقف"
            word = self.config.get("trigger_word", "ai")
            users = len(self.config.get("history", {}))
            total_msgs = sum(len(v) for v in self.config.get("history", {}).values())

            await ctx.send(
                f"**🤖 إعدادات AI:**\n"
                f"الحالة: {enabled}\n"
                f"كلمة التشغيل: `{word}`\n"
                f"المزود: `{API_PROVIDER}`\n"
                f"الموديل: `{API_MODEL}`\n"
                f"مستخدمين: `{users}`\n"
                f"رسائل محفوظة: `{total_msgs}`\n\n"
                f"**كيف تستخدمه؟**\n"
                f"١. منشني واكتب: `{word} <سؤالك>`\n"
                f"٢. أو رد على رسالتي واكتب: `{word} <سؤالك>`\n"
                f"٣. أو مباشر: `!ai <سؤالك>`"
            )
            return

        if action == "on":
            self.config["enabled"] = True
            self._save()
            return await ctx.send("✅ تم تفعيل AI")

        
        if action == "off":
            self.config["enabled"] = False
            self._save()
            return await ctx.send("🛑 تم إيقاف AI")

     
        if action == "word":
            if not value.strip():
                return await ctx.send("❌ اكتب: `!aiset word <كلمة>`")
            self.config["trigger_word"] = value.strip().lower()
            self._save()
            return await ctx.send(f"✅ كلمة التشغيل: `{value.strip()}`")

       
        if action == "clear":
            self.config["history"] = {}
            self._save()
            return await ctx.send("✅ تم مسح سجل المحادثات")

        
        if action == "clearme":
            uid = str(ctx.author.id)
            if uid in self.config.get("history", {}):
                del self.config["history"][uid]
                self._save()
                return await ctx.send("✅ تم مسح سجلك")
            return await ctx.send("❌ ما عندك سجل")

        
        await ctx.send(
            "**الأوامر:**\n"
            "`!aiset status` — الحالة\n"
            "`!aiset on` / `off` — تفعيل/إيقاف\n"
            "`!aiset word <كلمة>` — تغيير الكلمة\n"
            "`!aiset clear` — مسح كل السجل\n"
            "`!aiset clearme` — مسح سجلك فقط"
        )

    @commands.command(name="aitest")
    async def aitest(self, ctx):
        """!aitest → اختبار الاتصال بـ AI API"""
        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send("🧪 يختبر الاتصال...")

        reply = await self.ask_ai("test_user", "قل: مرحبا")

        if "❌" in reply or "⏳" in reply:
            await msg.edit(content=f"❌ فشل الاختبار:\n{reply}")
        else:
            await msg.edit(content=f"✅ الاتصال شغال!\nالرد: `{reply[:100]}`")


async def setup(bot):
    await bot.add_cog(AI(bot))