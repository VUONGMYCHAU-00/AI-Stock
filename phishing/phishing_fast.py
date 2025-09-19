import re

suspicious_keywords = [
    "password", "verify", "account", "ssn", "bank", "urgent", "click", "login", "update", "secure", "transfer"
]
suspicious_domains = ["bit.ly", "tinyurl", "phish", "verify", "secure"]

def check_phishing_rule(text: str):
    t = text.lower()
    score = 0
    reasons = []
    for kw in suspicious_keywords:
        if kw in t:
            score += 1
            reasons.append(f"keyword:{kw}")
    for dom in suspicious_domains:
        if dom in t:
            score += 2
            reasons.append(f"suspicious_link:{dom}")
    # URL pattern
    urls = re.findall(r'https?://[^\s]+', t)
    if urls:
        score += 2
        reasons.append("contains_url")
    label = "phishing" if score >= 2 else "safe"
    return {"label": label, "score": score, "reasons": reasons, "example_url": urls[:1]}
