from typing import Optional


def welcome_message(first_name: Optional[str] = None) -> str:
    name = first_name or "there"
    return (
        "<b>Hi, {name}!</b>\n\n"
        "Send a <b>YouTube</b> or <b>TikTok</b> link and I will download it for you.\n\n"
        "<b>How to use</b>\n"
        "1. Paste a link in the chat\n"
        "2. Choose audio or video (for YouTube)\n"
        "3. Wait a few seconds and get the file\n\n"
        "Need help? Tap <b>Help</b> below."
    ).format(name=name)


def help_message() -> str:
    return (
        "<b>Downloader Bot</b>\n\n"
        "I can download media from:\n"
        "• <b>YouTube</b> — video and audio\n"
        "• <b>TikTok</b> — video\n\n"
        "<b>Tips</b>\n"
        "• Send only a direct public link\n"
        "• Large files may fail due to Telegram limits\n"
        "• Do not spam links — flood protection is enabled\n\n"
        "Just paste a link to start."
    )


def statistic_message(
    users_total: int,
    users_blocked: int,
    users_active: int,
    users_week: int,
    downloads_total: int,
) -> str:
    return (
        "<b>Bot statistics</b>\n\n"
        "<b>Users</b>\n"
        "• Total: <code>{users_total}</code>\n"
        "• Active: <code>{users_active}</code>\n"
        "• Blocked: <code>{users_blocked}</code>\n"
        "• New (7 days): <code>{users_week}</code>\n\n"
        "<b>Downloads</b>\n"
        "• Total: <code>{downloads_total}</code>"
    ).format(
        users_total=users_total,
        users_active=users_active,
        users_blocked=users_blocked,
        users_week=users_week,
        downloads_total=downloads_total,
    )


def mailing_prompt() -> str:
    return (
        "<b>Broadcast</b>\n\n"
        "Send the message text for all users.\n"
        "HTML formatting is supported.\n\n"
        "To cancel, send /cancel"
    )


def mailing_cancelled() -> str:
    return "Broadcast cancelled."


def mailing_started(recipients: int) -> str:
    return "Broadcast started for <code>{}</code> users...".format(recipients)


def mailing_report(
    sent: int,
    failed: int,
    blocked: int,
    skipped: int,
    seconds: float,
) -> str:
    return (
        "<b>Broadcast finished</b>\n\n"
        "• Sent: <code>{sent}</code>\n"
        "• Failed: <code>{failed}</code>\n"
        "• Newly blocked: <code>{blocked}</code>\n"
        "• Skipped (already blocked): <code>{skipped}</code>\n"
        "• Time: <code>{seconds:.2f}</code> sec"
    ).format(
        sent=sent,
        failed=failed,
        blocked=blocked,
        skipped=skipped,
        seconds=seconds,
    )
