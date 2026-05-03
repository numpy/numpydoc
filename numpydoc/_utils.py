import re


def _clean_text_signature(sig):
    if sig is None:
        return None
    start_pattern = re.compile(r"^[^(]*\(")
    start, end = start_pattern.search(sig).span()
    start_sig = sig[start:end]
    sig = sig[end:-1]
    sig = re.sub(r"^\$(self|module|type)(,\s|$)", "", sig, count=1)
    sig = re.sub(r"(^|(?<=,\s))/,\s\*", "*", sig, count=1)
    return start_sig + sig + ")"
