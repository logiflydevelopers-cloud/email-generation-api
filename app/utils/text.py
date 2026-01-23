def wrap_email(
    subject: str,
    body: str,
    closing: str,
) -> str:
    return (
        f"Subject: {subject}\n\n"
        f"Dear {{RECIPIENT}},\n\n"
        f"{body.strip()}\n\n"
        f"{closing.strip()}\n"
        f"{{NAME}}"
    )


def clamp_chars(text: str, max_chars: int) -> str:
    if not text:
        return text

    if len(text) <= max_chars:
        return text

    return text[:max_chars].rstrip()
