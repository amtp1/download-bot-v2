from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramEntityTooLarge, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy.orm import sessionmaker

from bot.db import Role, SQLDownload
from bot.filters import ChatTypeFilter, RoleCheckFilter, check_url
from bot.keyboards import IKB_SELECT_TYPE, convert_to_content_types
from bot.utils.callback_data_factories import BasicAction, BasicCallback
from bot.youtube import YouTube

# from bot.keyboards.basic import IKB_PROFILE, IKB_START

# Создание маршрутизатора
router = Router(name="Command download")

# Регистрация фильтров
router.message.filter(RoleCheckFilter(Role.USER))
router.message.filter(ChatTypeFilter(["private"]))


# Регистрация обработчиков
@router.message(F.text, flags={"delay": 2})
async def download(
    m: Message, bot: Bot, session: sessionmaker, state: FSMContext
) -> None:
    """
    Обработчик, который реагирует на команду /start
    """

    url = check_url(m.text)
    if not url:
        return await m.answer("❌Incorrect link")
    else:
        await state.update_data(url=m.text)
        return await m.answer("Select the type👇", reply_markup=IKB_SELECT_TYPE)


@router.callback_query(BasicCallback.filter(F.action == BasicAction.SELECT_AUDIO))
async def select_audio(c: CallbackQuery, state: FSMContext) -> CallbackQuery | None:
    state_data = await state.get_data()
    url = state_data["url"]
    youtube = YouTube(url)
    streams = youtube.get_streams(is_audio=True)
    streams, markup = convert_to_content_types(
        title=streams["title"], streams=streams["audios"], is_audio=True
    )
    await state.update_data(streams=streams)
    return await c.message.edit_text("Select👇", reply_markup=markup.as_markup())


@router.callback_query(BasicCallback.filter(F.action == BasicAction.SELECT_VIDEO))
async def select_video(c: CallbackQuery, state: FSMContext) -> CallbackQuery | None:
    state_data = await state.get_data()
    url = state_data["url"]
    youtube = YouTube(url)
    streams = youtube.get_streams(is_video=True)
    streams, markup = convert_to_content_types(
        title=streams["title"], streams=streams["videos"], is_video=True
    )
    await state.update_data(streams=streams)
    return await c.message.edit_text("Select👇", reply_markup=markup.as_markup())


@router.callback_query(lambda query: query.data.startswith(("audio")))
async def download_audio(
    c: CallbackQuery, state: FSMContext, session: sessionmaker
) -> Message | bool:
    await c.message.edit_text("Downloading... Please, wait!")
    audio_id = c.data.replace("audio#", "")
    state_data = await state.get_data()
    streams = state_data["streams"]
    audio_url = streams[audio_id]
    audio_title = streams["title"]
    youtube = YouTube()
    audio = youtube.download(audio_url)
    sql_download = SQLDownload(session)

    try:
        await c.message.answer_audio(
            audio=BufferedInputFile(audio, filename=audio_title),
            title=audio_title,
            caption="🔗Channel: @downloader_video",
        )
        return await sql_download.add(
            user_id=c.from_user.id, link=audio_url, content_type="audio", service="youtube"
        )
    except (TelegramEntityTooLarge, TelegramBadRequest) as e:
        return await c.message.edit_text(e.message)


@router.callback_query(lambda query: query.data.startswith(("video")))
async def download_video(
    c: CallbackQuery, state: FSMContext, session: sessionmaker
) -> Message | bool:
    await c.message.edit_text("Downloading... Please, wait!")
    video_id = c.data.replace("video#", "")
    state_data = await state.get_data()
    streams = state_data["streams"]
    video_url = streams[video_id]
    video_title = streams["title"]
    youtube = YouTube()
    video = youtube.download(video_url)
    sql_download = SQLDownload(session)

    try:
        await c.message.answer_video(
            video=BufferedInputFile(video, filename=video_title),
            title=video_title,
            caption=video_title,
        )
        return await sql_download.add(
            user_id=c.from_user.id, link=video_url, content_type="video", service="youtube"
        )
    except (TelegramEntityTooLarge, TelegramBadRequest) as e:
        return await c.message.edit_text(e.message)


# Псевдоним
router_download = router
