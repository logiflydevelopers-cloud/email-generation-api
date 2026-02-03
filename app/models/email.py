from pydantic import BaseModel, Field, constr, conint, ConfigDict


# -----------------------------
# Shared Base (WORD-BASED)
# -----------------------------
class BaseEmailRequest(BaseModel):
    user_key: str = Field(
        ...,
        description="Unique user identifier or API key"
    )

    tone: constr(min_length=3, max_length=30) = Field(
        ...,
        description="Tone of the email (e.g. professional, friendly, formal)"
    )

    language_code: constr(min_length=2, max_length=10) = Field(
        ...,
        description="Language code (e.g. en, en-US, fr, hi)"
    )

    # WORD-based length (single source of truth)
    length_words: conint(ge=20, le=2000) = Field(
        150,
        description="Target number of words for the email body"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        extra="forbid",
    )


# -----------------------------
# Write Email
# -----------------------------
class WriteEmailRequest(BaseEmailRequest):
    topic: constr(min_length=1, max_length=500) = Field(
        ...,
        description="Topic or intent of the email"
    )


# -----------------------------
# Reply Email
# -----------------------------
class ReplyEmailRequest(BaseEmailRequest):
    body: constr(min_length=1, max_length=800) = Field(
        ...,
        description="Original email content to reply to"
    )


# -----------------------------
# Template Email
# -----------------------------
class TemplateEmailRequest(BaseEmailRequest):
    body: str = Field(
        ...,
        description="Existing email template content to modify"
    )



# -----------------------------
# Response
# -----------------------------
class EmailResponse(BaseModel):
    email: str = Field(
        ...,
        description="Generated email content"
    )

    input_tokens: int = Field(
        ...,
        description="Estimated input tokens (prompt)"
    )

    output_tokens: int = Field(
        ...,
        description="Estimated output tokens (email content)"
    )

    total_tokens: int = Field(
        ...,
        description="Total estimated tokens (input + output)"
    )

    model_config = ConfigDict(
        extra="forbid"
    )

