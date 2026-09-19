
import discord
from discord.ext import commands
import asyncio


class Purge(commands.Cog):
    """🗑️ أوامر حذف الرسائل"""

    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="purge")
    async def purge(self, ctx, channel_id: int = None, limit: int = 1000):
        """
        !purge → الروم الحالي
        !purge <channel_id> → روم محدد
        !purge <channel_id> <limit> → بحد معين
        !purge <channel_id> 0 → كل الرسائل
        """
        try:
            await ctx.message.delete()
        except:
            pass

   
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                try:
                    channel = await self.bot.fetch_channel(channel_id)
                except Exception as e:
                    return await ctx.send(f"❌ ما قدرت أجيب الروم:\n```{e}```")

        channel_name = getattr(channel, "name", "DM")

        msg = await ctx.send(
            f"🗑️ جاري الحذف من: `{channel_name}`\n"
            f"الحد: `{limit if limit > 0 else 'الكل'}`"
        )

        deleted = 0
        scanned = 0
        failed = 0
        history_limit = None if limit == 0 else limit

        try:
            async for message in channel.history(limit=history_limit):
                scanned += 1

               
                if message.author.id == self.bot.user.id:
                    try:
                        await message.delete()
                        deleted += 1

                     
                        if deleted % 10 == 0:
                            try:
                                await msg.edit(content=
                                    f"🗑️ `{channel_name}`\n"
                                    f"✅ حُذف: **{deleted}**\n"
                                    f"🔍 فُحص: {scanned}"
                                )
                            except:
                                pass

                        # تأخير بسيط
                        if deleted % 5 == 0:
                            await asyncio.sleep(1.2)

                    except discord.Forbidden:
                        failed += 1
                    except discord.HTTPException as e:
                        failed += 1
                        if e.status == 429:
                            await asyncio.sleep(5)

              
                if scanned % 100 == 0:
                    try:
                        await msg.edit(content=
                            f"🗑️ `{channel_name}`\n"
                            f"✅ حُذف: **{deleted}**\n"
                            f"🔍 فُحص: {scanned}\n"
                            f"❌ فشل: {failed}"
                        )
                    except:
                        pass

        except discord.Forbidden:
            return await msg.edit(content=f"❌ ما عندي صلاحية في `{channel_name}`")
        except Exception as e:
            return await msg.edit(content=f"❌ خطأ:\n```\n{type(e).__name__}: {e}\n```")

        await msg.edit(content=
            f"✅ **انتهى!**\n"
            f"📁 `{channel_name}`\n"
            f"🗑️ حُذف: **{deleted}**\n"
            f"🔍 فُحص: {scanned}\n"
            f"❌ فشل: {failed}"
        )


    @commands.command(name="purgeall")
    async def purgeall(self, ctx, limit_per_channel: int = 500):
        """
        !purgeall [limit]
        يحذف رسائلك من كل الرومات في السيرفر
        """
        try:
            await ctx.message.delete()
        except:
            pass

        msg = await ctx.send(f"🗑️ جاري الحذف من كل الرومات...")

        total_deleted = 0
        channels_done = 0
        channels_skipped = 0
        total_channels = len(ctx.guild.text_channels)

        for channel in ctx.guild.text_channels:

            try:
                perms = channel.permissions_for(ctx.guild.me)
                if not perms.read_message_history or not perms.manage_messages:
                    channels_skipped += 1
                    continue
            except:
                channels_skipped += 1
                continue

            try:
                deleted_here = 0
                async for message in channel.history(limit=limit_per_channel):
                    if message.author.id == self.bot.user.id:
                        try:
                            await message.delete()
                            deleted_here += 1
                            total_deleted += 1

                            if deleted_here % 3 == 0:
                                await asyncio.sleep(1)
                        except:
                            pass

                channels_done += 1

                try:
                    await msg.edit(content=
                        f"🗑️ التقدم: {channels_done}/{total_channels}\n"
                        f"✅ حُذف: **{total_deleted}**\n"
                        f"⏭️ تخطي: {channels_skipped}"
                    )
                except:
                    pass

            except:
                pass

            await asyncio.sleep(2)

        await ctx.send(
            f"✅ **انتهى!**\n"
            f"📊 حُذف: **{total_deleted}** رسالة\n"
            f"📁 رومات: {channels_done}\n"
            f"⏭️ تخطي: {channels_skipped}"
        )

    @commands.command(name="purgeeveryone")
    async def purgeeveryone(self, ctx, channel_id: int = None, limit: int = 1000, confirm: str = ""):
        """
        !purgeeveryone <channel_id> <limit> yes
        يحذف كل الرسائل (مو بس رسائلك)
        ⚠️ خطر — ما فيه تراجع
        """
        if confirm.lower() != "yes":
            return await ctx.send(
                "⚠️ **تحذير:** هذا بيحذف **كل** الرسائل!\n"
                f"**للتأكيد:** `!purgeeveryone {channel_id or ''} {limit} yes`"
            )

        try:
            await ctx.message.delete()
        except:
            pass

  
        if channel_id is None:
            channel = ctx.channel
        else:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                try:
                    channel = await self.bot.fetch_channel(channel_id)
                except Exception as e:
                    return await ctx.send(f"❌ ما قدرت أجيب الروم: `{e}`")

        channel_name = getattr(channel, "name", "DM")
        msg = await ctx.send(f"🗑️ حذف **كل** الرسائل من `{channel_name}`...")

        deleted = 0
        failed = 0
        history_limit = None if limit == 0 else limit

        try:
            async for message in channel.history(limit=history_limit):
                try:
                    await message.delete()
                    deleted += 1

                    if deleted % 5 == 0:
                        try:
                            await msg.edit(content=f"🗑️ حُذف: **{deleted}**")
                        except:
                            pass
                        await asyncio.sleep(1.2)
                except:
                    failed += 1

        except Exception as e:
            return await msg.edit(content=f"❌ خطأ: `{e}`")

        await msg.edit(content=
            f"✅ انتهى!\n"
            f"🗑️ حُذف: **{deleted}**\n"
            f"❌ فشل: {failed}"
        )


    @commands.command(name="dms")
    async def dms(self, ctx):
        """!dms → قائمة DMs + IDs"""
        try:
            await ctx.message.delete()
        except:
            pass

        lines = ["**📋 قائمة DMs:**\n"]
        count = 0

        for channel in self.bot.private_channels:
            if isinstance(channel, discord.DMChannel):
                user = channel.recipient
                lines.append(f"👤 **{user}**\n   🆔 `{channel.id}`\n")
                count += 1
            elif isinstance(channel, discord.GroupChannel):
                lines.append(f"👥 **Group: {channel.name}**\n   🆔 `{channel.id}`\n")
                count += 1

        if count == 0:
            return await ctx.send("❌ ما فيه DMs")

        text = "\n".join(lines)

        if len(text) > 1900:
            parts = [text[i:i+1900] for i in range(0, len(text), 1900)]
            for part in parts:
                await ctx.send(part)
                await asyncio.sleep(0.3)
        else:
            await ctx.send(text)

    @commands.command(name="chinfo")
    async def chinfo(self, ctx, channel_id: int = None):
        """!chinfo [channel_id] → معلومات الروم"""
        try:
            await ctx.message.delete()
        except:
            pass

        if channel_id is None:
            channel = ctx.channel
        else:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                try:
                    channel = await self.bot.fetch_channel(channel_id)
                except:
                    return await ctx.send(f"❌ ما لقيت الروم")

        
        my_msgs = 0
        try:
            async for m in channel.history(limit=500):
                if m.author.id == self.bot.user.id:
                    my_msgs += 1
        except:
            pass

        await ctx.send(
            f"**📁 معلومات الروم:**\n"
            f"📛 الاسم: `{getattr(channel, 'name', 'DM')}`\n"
            f"🆔 ID: `{channel.id}`\n"
            f"📝 رسائلك (آخر 500): `{my_msgs}`"
        )


async def setup(bot):
    await bot.add_cog(Purge(bot))