import re
import difflib

# Suspicious keywords
SUSPICIOUS_KEYWORDS = [
    "password", "verify", "account", "ssn", "bank",
    "urgent", "click", "login", "update", "secure", "transfer"
]

# Suspicious domains (rút gọn / fake)
SUSPICIOUS_DOMAINS = ["bit.ly", "tinyurl", "phish", "verify", "secure"]

# Trusted whitelist (giảm false positive)
TRUSTED_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "hdbank.vn"]

def extract_domain(url: str) -> str:
    """Lấy domain từ URL (simple regex)."""
    match = re.search(r"(https?://|www\.)?([^/\s]+)", url)
    if match:
        return match.group(2).lower()
    return ""

def is_lookalike(domain: str) -> str:
    """Check lookalike domain bằng difflib."""
    for trusted in TRUSTED_DOMAINS:
        ratio = difflib.SequenceMatcher(None, domain, trusted).ratio()
        if ratio > 0.75 and domain != trusted:
            return f"lookalike:{trusted}"
    return ""

def check_phishing_rule(text: str, threshold: int = 2):
    # --- Chuẩn hoá input ---
    if not text or not text.strip():
        return {
            "label": "invalid",
            "score": 0,
            "reasons": ["empty_input"],
            "example_url": []
        }

    t = text.strip().lower()
    score = 0
    reasons = []
    urls = []

    # --- Check keywords ---
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in t:
            score += 1
            reasons.append(f"keyword:{kw}")

    # --- Check suspicious domain patterns ---
    for dom in SUSPICIOUS_DOMAINS:
        if dom in t:
            score += 2
            reasons.append(f"suspicious_domain:{dom}")

    # --- Check URLs (http + www) ---
    urls = re.findall(r'(https?://[^\s]+|www\.[^\s]+)', t)
    if urls:
        score += 2
        reasons.append("contains_url")

        for u in urls:
            d = extract_domain(u)
            if d:
                # Lookalike check
                look = is_lookalike(d)
                if look:
                    score += 2
                    reasons.append(look)
                # Trusted whitelist check
                elif any(d.endswith(td) for td in TRUSTED_DOMAINS):
                    reasons.append(f"trusted:{d}")

    # --- Check nếu input chỉ là email ---
    EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    if EMAIL_RE.match(t) and len(t.split()) == 1:
        local, domain = t.split("@", 1)
        domain = domain.lower()

        if domain in TRUSTED_DOMAINS:
            reasons.append("single_email:trusted_domain")
        else:
            look = is_lookalike(domain)
            if look:
                score += 2
                reasons.append(look)
            if re.search(r"[0-9]|--|__", domain):
                score += 1
                reasons.append("weird_chars_in_domain")
        reasons.append("note:input_is_single_email")

    # --- Phân loại ---
    label = "phishing" if score >= threshold else "safe"

    return {
        "label": label,
        "score": score,
        "reasons": reasons,
        "example_url": urls[:1]
    }
