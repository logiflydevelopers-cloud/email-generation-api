def normalize_closing(text: str) -> str:
    """
    Ensures exactly ONE proper closing.

    Behavior:
    - Detects existing full closing:
        Best regards,
        <ANY NAME>
    - Keeps the LAST valid closing
    - Removes partial closings (Best, Regards, Thanks, etc.)
    - Appends closing ONLY if missing
    """

    lines = [line.rstrip() for line in text.rstrip().splitlines()]
    lower = [line.lower().strip() for line in lines]

    last_valid_closing_index = None

    # Detect valid full closing: "Best regards," + non-empty next line
    for i in range(len(lines) - 1):
        if lower[i] == "best regards," and lines[i + 1].strip():
            last_valid_closing_index = i

    # If found, keep only the last valid closing
    if last_valid_closing_index is not None:
        return "\n".join(lines[: last_valid_closing_index + 2])

    # Remove partial closings at the end
    partial_closings = {
        "best",
        "regards",
        "thanks",
        "thank you",
        "sincerely",
        "kind regards"
    }

    while lines:
        if lines[-1].strip().lower() in partial_closings:
            lines.pop()
        else:
            break

    cleaned_text = "\n".join(lines).rstrip()
    return cleaned_text + "\n\nBest regards,\n{NAME}"
