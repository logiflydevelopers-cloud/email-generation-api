def words_to_tokens(words: int) -> int:
    """
    Rough conversion from words to tokens.
    1 token ≈ 0.75 words (safe estimate for English).
    """
    if words <= 0:
        return 0
    return int(words / 0.75)
