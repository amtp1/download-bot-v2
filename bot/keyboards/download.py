from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.utils import BasicAction, BasicCallback

IKB_SELECT_TYPE = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Audio",
                callback_data=BasicCallback(action=BasicAction.SELECT_AUDIO).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="Video",
                callback_data=BasicCallback(action=BasicAction.SELECT_VIDEO).pack(),
            )
        ],
    ]
)


def convert_to_content_types(title: str, streams: dict, is_audio=None, is_video=None):
    IKB_CONTENT_TYPES = InlineKeyboardBuilder()
    items = streams["items"]
    streams = {}
    streams["title"] = title
    for i, item in enumerate(items):
        mime_type = item["mimeType"].split(";")[0]
        streams[i] = item["url"]
        if is_audio:
            callback_data = f"audio#{i}"
        elif is_video:
            callback_data = f"video#{i}"
        inline_button = InlineKeyboardButton(
            text=f"{mime_type} - {item['sizeText']}", callback_data=callback_data
        )
        IKB_CONTENT_TYPES.add(inline_button)
    IKB_CONTENT_TYPES.adjust(1)
    return [streams, IKB_CONTENT_TYPES]
