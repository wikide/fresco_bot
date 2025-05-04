import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from telegram import Update, Message, Chat, Voice
from telegram.ext import ContextTypes
import os
import json
import asyncio
import speech_recognition as sr
from run import (
    help_command,
    quote,
    ask,
    img,
    handle_message,
    ask_openrouter,
    translate_text,
    voice_to_text_handler,
    convert_voice_to_text,
    donate,
    play_music,
    download_youtube,
    download_twitter,
    download_vk_clip,
    download_tiktok,
    send_voice_message,
    text_to_speech,
    find_music,
    get_tracks_from_llm,
    start_game,
    handle_webapp_data
)


# Fixtures
@pytest.fixture
def update():
    upd = MagicMock(spec=Update)
    upd.message = MagicMock(spec=Message)
    upd.message.chat_id = 123
    upd.message.reply_text = AsyncMock()
    upd.message.reply_audio = AsyncMock()
    upd.message.reply_video = AsyncMock()
    upd.message.reply_voice = AsyncMock()
    upd.message.reply_photo = AsyncMock()
    upd.message.edit_text = AsyncMock()
    upd.message.delete = AsyncMock()
    upd.message.text = "/command"
    upd.message.voice = MagicMock(spec=Voice)
    upd.message.voice.file_id = "voice123"
    upd.effective_chat = MagicMock(spec=Chat)
    upd.effective_chat.id = 123
    return upd


@pytest.fixture
def context():
    ctx = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    ctx.args = []
    ctx.bot = MagicMock()
    ctx.bot.send_message = AsyncMock()
    ctx.bot.send_photo = AsyncMock()
    ctx.bot.send_audio = AsyncMock()
    ctx.bot.send_video = AsyncMock()
    ctx.bot.send_voice = AsyncMock()
    ctx.bot.get_file = AsyncMock()
    return ctx


# Tests
@pytest.mark.asyncio
async def test_help_command(update, context):
    await help_command(update, context)
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_quote(update, context):
    with patch("builtins.open", mock_open(read_data="Quote 1\nQuote 2\n")):
        await quote(update, context)
    context.bot.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_ask_with_args(update, context):
    context.args = ["What", "is", "Venus", "Project?"]
    with patch("run.ask_openrouter", AsyncMock(return_value="Test response")):
        await ask(update, context)
    context.bot.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_img_default_prompt(update, context):
    await img(update, context)
    update.message.reply_text.assert_called_with("🔄 Изображение генерируется... Я пришлю его, как только будет готово!")


@pytest.mark.asyncio
async def test_img_with_prompt(update, context):
    context.args = ["футуристический город"]
    with patch("run.ask_openrouter", AsyncMock(return_value="futuristic city")):
        await img(update, context)
    update.message.reply_text.assert_called_with("🔄 Изображение генерируется... Я пришлю его, как только будет готово!")


@pytest.mark.asyncio
async def test_handle_message_youtube_link(update, context):
    update.message.text = "https://youtube.com/watch?v=test"
    with patch("run.download_youtube", AsyncMock()):
        await handle_message(update, context)
    assert len(context.args) == 1

@pytest.mark.asyncio
async def test_translate_text(update, context):
    context.args = ["Привет"]
    with patch("run.ask_openrouter", AsyncMock(return_value="Hello")):
        await translate_text(update, context)
    update.message.reply_text.assert_called_with("🌍 Перевод:\nHello")


@pytest.mark.asyncio
async def test_voice_to_text_handler(update, context):
    with patch("run.convert_voice_to_text", AsyncMock(return_value="распознанный текст")):
        await voice_to_text_handler(update, context)
    update.message.reply_text.assert_called()

@pytest.mark.asyncio
async def test_convert_voice_to_text_file_error():
    with patch('pydub.AudioSegment.from_ogg', side_effect=Exception("File error")):
        result = await convert_voice_to_text("test.ogg")
        assert "Ошибка распознавания: File error" in result


@pytest.mark.asyncio
async def test_donate(update, context):
    await donate(update, context)
    update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_play_music_no_args(update, context):
    await play_music(update, context)
    update.message.reply_text.assert_called_with("Укажите название трека: /play <название>")


@pytest.mark.asyncio
async def test_play_music_success(update, context):
    context.args = ["test song"]
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.extract_info.return_value = {
            'entries': [{'title': 'Test Song', 'uploader': 'Test Artist'}]
        }
        mock_ydl.return_value.prepare_filename.return_value = "test.webm"

        with patch("builtins.open", mock_open()), \
                patch("os.path.exists", return_value=True), \
                patch("os.path.getsize", return_value=5000), \
                patch("os.remove"):
            await play_music(update, context)

    update.message.reply_audio.assert_called_once()


@pytest.mark.asyncio
async def test_download_youtube(update, context):
    context.args = ["https://youtube.com/watch?v=test"]
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.extract_info.return_value = {
            'title': 'Test Video',
            'duration': 100
        }
        mock_ydl.return_value.prepare_filename.return_value = "test.mp4"

        with patch("builtins.open", mock_open()), \
                patch("os.path.exists", return_value=True), \
                patch("os.path.getsize", return_value=5000), \
                patch("os.remove"):
            await download_youtube(update, context)

    update.message.reply_video.assert_called_once()


@pytest.mark.asyncio
async def test_download_twitter(update, context):
    context.args = ["https://twitter.com/test/status/123"]
    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        mock_ydl.return_value.extract_info.return_value = {
            'title': 'Test Video',
            'uploader': 'test_user'
        }
        mock_ydl.return_value.prepare_filename.return_value = "test.mp4"

        with patch("builtins.open", mock_open()), \
                patch("os.path.exists", return_value=True), \
                patch("os.remove"):
            await download_twitter(update, context)

    update.message.reply_video.assert_called_once()


@pytest.mark.asyncio
async def test_send_voice_message(update, context):
    context.args = ["test text"]
    with patch("run.ask_openrouter", AsyncMock(return_value="test response")), \
            patch("run.text_to_speech", AsyncMock(return_value="test.mp3")), \
            patch("builtins.open", mock_open()), \
            patch("os.path.exists", return_value=True), \
            patch("os.remove"):
        await send_voice_message(update, context)

    context.bot.send_voice.assert_called_once()


@pytest.mark.asyncio
async def test_text_to_speech():
    with patch("edge_tts.Communicate.save", AsyncMock()), \
            patch("uuid.uuid4", return_value="test123"):
        result = await text_to_speech("test text")
        assert result == "voice_test123.mp3"

@pytest.mark.asyncio
async def test_find_music(update, context):
    context.args = ["jazz"]
    with patch("run.get_tracks_from_llm", AsyncMock(return_value=["Artist - Song"])), \
            patch("run.play_music", AsyncMock()):
        await find_music(update, context)

    update.message.reply_text.assert_called()

@pytest.mark.asyncio
async def test_get_tracks_from_llm():
    test_response = "1. Artist1 - Song1\n2. Artist2 - Song2"
    with patch("run.ask_openrouter", AsyncMock(return_value=test_response)):
        result = await get_tracks_from_llm("jazz")
        assert len(result) == 2
        assert "Artist1 - Song1" in result

@pytest.mark.asyncio
async def test_start_game(update, context):
    await start_game(update, context)
    update.message.reply_text.assert_called_once()
