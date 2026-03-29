from datetime import datetime, timezone


POSITIVE = [
    "excellent", "amazing", "fantastic", "great", "helpful", "outstanding",
    "brilliant", "perfect", "wonderful", "superb", "good", "nice", "kind",
    "fast", "efficient", "clear", "patient", "knowledgeable", "professional", "thorough",
]

NEGATIVE = [
    "bad", "terrible", "awful", "useless", "unhelpful", "slow", "rude",
    "wrong", "poor", "disappointing", "confusing", "unclear", "late", "incompetent", "lazy",
]

TIERS = [
    (85, "Diamond", "💎"),
    (70, "Platinum", "🏅"),
    (55, "Gold", "🥇"),
    (40, "Silver", "🥈"),
    (0, "Bronze", "🥉"),
]


def parse_timestamp(ts: str) -> datetime:
    if not ts or not isinstance(ts, str):
        raise ValueError("timestamp is required, for example '2026-03-29T02:30:00Z'")

    try:
        dt = datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(
            f"Invalid timestamp '{ts}'. Use ISO 8601 UTC, for example '2026-03-29T02:30:00Z'"
        ) from exc

    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone info. Add 'Z' at the end.")

    return dt.astimezone(timezone.utc)


def calculate_points(stars, task_title, task_description, timestamp, location) -> dict:
    stars = round(float(stars))
    if not (1 <= stars <= 5):
        raise ValueError("stars must be between 1 and 5")
    if not task_title or not str(task_title).strip():
        raise ValueError("task_title is required")
    if not task_description or not str(task_description).strip():
        raise ValueError("task_description is required")
    if not location or not str(location).strip():
        raise ValueError("location is required")

    dt = parse_timestamp(timestamp)

    star_pts = stars * 10

    text = str(task_description).strip().lower()
    raw = sum(3 for kw in POSITIVE if kw in text) - sum(3 for kw in NEGATIVE if kw in text)
    clamped = max(-20, min(20, raw))
    sentiment_pts = round(((clamped + 20) / 40) * 20)

    char_count = len(str(task_description).strip())
    if char_count >= 200:
        length_pts = 10
    elif char_count >= 100:
        length_pts = 7
    elif char_count >= 50:
        length_pts = 5
    elif char_count >= 20:
        length_pts = 2
    else:
        length_pts = 0

    desc_pts = sentiment_pts + length_pts

    hour = dt.hour
    is_night = hour >= 22 or hour < 6
    is_weekend = dt.weekday() in (5, 6)
    urgency_pts = (10 if is_night else 0) + (10 if is_weekend else 0)

    total = star_pts + desc_pts + urgency_pts
    tier, badge = next((tier, badge) for threshold, tier, badge in TIERS if total >= threshold)

    return {
        "submission": {
            "stars": stars,
            "task_title": str(task_title).strip(),
            "task_description": str(task_description).strip(),
            "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "location": str(location).strip(),
        },
        "breakdown": {
            "starPoints": star_pts,
            "descriptionPoints": {
                "sentimentPoints": sentiment_pts,
                "lengthPoints": length_pts,
                "charCount": char_count,
                "total": desc_pts,
            },
            "urgencyPoints": {
                "isNight": is_night,
                "isWeekend": is_weekend,
                "total": urgency_pts,
            },
        },
        "totalPoints": total,
        "tier": tier,
        "badge": badge,
    }
