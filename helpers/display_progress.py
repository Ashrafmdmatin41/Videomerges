#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

import logging
import math
import os
import time

from pyrogram.errors.exceptions import FloodWait
from __init__ import (
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    EDIT_SLEEP_TIME_OUT,
    gDict,
    LOGGER,
)
from pyrogram import Client

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


class Progress:
    def __init__(self, from_user, client, mess: Message):
        self._from_user = from_user
        self._client = client
        self._mess = mess
        self._cancelled = False

    @property
    def is_cancelled(self):
        chat_id = self._mess.chat.id
        mes_id = self._mess.id
        if gDict[chat_id] and mes_id in gDict[chat_id]:
            self._cancelled = True
        return self._cancelled

        async def progress_for_pyrogram(self, current, total, ud_type, start, count=""):
        chat_id = self._mess.chat.id
        mes_id = self._mess.id
        from_user = self._from_user
        now = time.time()
        diff = now - start
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⛔ Cancel ⛔",
                        callback_data=(
                            f"gUPcancel/{chat_id}/{mes_id}/{from_user}"
                        ).encode("UTF-8"),
                    )
                ]
            ]
        )
        if self.is_cancelled:
            LOGGER.info("stopping ")
            await self._mess.edit(
                f"⛔ **Cancelled** ⛔ \n\n `{ud_type}` ({humanbytes(total)})"
            )
            await self._client.stop_transmission()

        try:
            percentage = current * 100 / total
        except ZeroDivisionError:
            percentage = 0

        if round(diff % float(EDIT_SLEEP_TIME_OUT)) == 0 or current == total:
            speed = current / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((total - current) / speed) * 1000
            estimated_total_time = time_to_completion

            elapsed_time = TimeFormatter(milliseconds=elapsed_time)
            estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

            progress = "\n<code>[{0}{1}] {2}%</code>\n".format(
                "".join(
                    [FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]
                ),
                "".join(
                    [
                        UN_FINISHED_PROGRESS_STR
                        for i in range(20 - math.floor(percentage / 5))
                    ]
                ),
                round(percentage, 2),
            )
            tmp = (
                progress
                + "\n**⌧ Total 🗃:**` 〚{1}〛`\n**⌧ Done ✅ :**` 〚{0}〛`\n**⌧ Speed 📊 :** ` 〚{2}/s〛`\n**⌧ ETA 🔃 :**` 〚{3}〛`\n {4}".format(
                    humanbytes(current),
                    humanbytes(total),
                    humanbytes(speed),
                    estimated_total_time if estimated_total_time != "" else "0 s",
                    count
                )
            )
            try:
                if not self._mess.photo:
                    await self._mess.edit_text(
                        text="{}\n {}".format(ud_type, tmp), reply_markup=reply_markup
                    )
                else:
                    await self._mess.edit_caption(
                        caption="{}\n {}".format(ud_type, tmp)
                    )
            except FloodWait as fd:
                logger.warning(f"{fd}")
                time.sleep(fd.x)
            except Exception as ou:
                logger.info(ou)
