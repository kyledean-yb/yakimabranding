#!/usr/bin/env python3
"""Generate blog intro blocks (Short Answer, Summary, Key Takeaways) for insight posts."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_JSON = ROOT / "blog" / "data" / "posts.json"
POSTS_DIR = ROOT / "blog" / "posts"

SKIP_SLUGS = {
    "yb-marketing-announces-strategic-acquisition-of-encite-branding-marketing-creative",
}

UPDATED_LINE = "Updated June 2026"


def normalize_text(text: str) -> str:
    text = html.unescape(text or "")
    return (
        text.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_paragraphs(prose_html: str) -> list[str]:
    paras = []
    for match in re.finditer(
        r"<p[^>]*class=\"[^\"]*blog-p[^\"]*\"[^>]*>(.*?)</p>",
        prose_html,
        flags=re.I | re.S,
    ):
        text = strip_html(match.group(1))
        if len(text) > 40 and text.lower() not in ("case study",):
            paras.append(text)
    if not paras:
        for match in re.finditer(r"<p[^>]*>(.*?)</p>", prose_html, flags=re.I | re.S):
            text = strip_html(match.group(1))
            if len(text) > 40:
                paras.append(text)
    return paras


def extract_headings(prose_html: str) -> list[str]:
    headings = []
    for tag in ("h2", "h3"):
        for match in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", prose_html, flags=re.I | re.S):
            text = strip_html(match.group(1))
            if text and len(text) > 3:
                headings.append(text)
    return headings


def extract_list_items(prose_html: str) -> list[str]:
    items = []
    for match in re.finditer(r"<li[^>]*>(.*?)</li>", prose_html, flags=re.I | re.S):
        text = strip_html(match.group(1))
        if 20 < len(text) < 220:
            items.append(text)
    return items


def trim_sentence(text: str, max_len: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def first_sentence(text: str, max_len: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)
    sentence = parts[0] if parts else text
    return trim_sentence(sentence, max_len)


FLUFF_STARTS = (
    "as you dive into",
    "have you ever",
    "imagine if you",
    "you wake up",
    "are you a business owner",
    "can't decide",
    "cannot decide",
    "i see you",
    "today's consumers",
    "if you've spent",
    "depending on your industry",
    "whenever you bring",
    "often, landscaping",
    "let's learn more",
    "you may be familiar with",
    "you've done a great job",
    "building a strong local presence",
    "developing a landing page sounds",
    "people move through the sales funnel",
    "creating a high quality social media",
    "thermal press is a leader",
    "a well-designed patio",
    "your transmission is an essential",
    "you have many options for moving",
    "how's the current deluge",
    "commercial businesses and their drivers",
    "a person interested in starting",
    "why should you send your child",
    "preventing employee lawsuits",
    "if you're struggling to convert",
    "if you're in need",
    "if you're ready to create",
    "here are five",
    "here is a brief",
    "as you may have previously read",
    "as part of our series",
    "to better utilize",
    "you know you need",
    "if you think social media management could benefit",
    "reach out to our",
    "now that you have a better understanding",
)

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "with", "by", "from", "is", "are", "was", "be", "been", "being", "have",
    "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "may", "might", "must", "shall", "can", "need", "into", "through", "during",
    "before", "after", "above", "below", "up", "down", "out", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
    "too", "very", "just", "about", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "it", "its", "you", "your", "we", "our",
    "they", "their", "he", "she", "his", "her", "them", "as", "if", "also",
    "get", "use", "using", "make", "help", "know", "like", "one", "two",
    "three", "four", "five", "six", "seven", "ways", "tips", "tactics",
    "major", "common", "best", "every", "everyone", "business", "businesses",
    "marketing", "digital", "social", "media", "website", "websites",
    "important", "everything", "need", "vs", "vs.",
}


JUNK_PATTERNS = (
    "read here",
    "previously read",
    "webinar",
    "wsi net advantage",
    "contact wsi",
    "free quote",
    "reach out to our",
    "watch the full webinar",
    "available to watch here",
    "contact yakima branding",
    "contact the knowledgeable",
    "info@yakimabranding",
    "509-901-9735",
    "to learn more about designing a portfolio",
    "to learn more about the best business entity",
    "originally posted at:",
)


def is_junk_sentence(text: str) -> bool:
    lower = normalize_text(text).lower().strip()
    if lower.startswith("(") or "( read here )" in lower:
        return True
    return any(p in lower for p in JUNK_PATTERNS)


def is_fluff(text: str) -> bool:
    lower = normalize_text(text).lower().strip()
    if any(lower.startswith(s) for s in FLUFF_STARTS):
        return True
    if re.match(r"^here (are|is)\b", lower):
        return True
    return False


def is_question_sentence(text: str) -> bool:
    text = normalize_text(text).strip()
    if not text:
        return True
    if text.endswith("?"):
        return True
    lower = text.lower()
    return bool(
        re.match(
            r"^(can(?:not|'t)?|could|would|should|do|does|did|is|are|was|were|have|has|will|"
            r"what|why|how|where|who|which|are you|is there|"
            r"when should|when do|when is|when are|when can|when will)\b",
            lower,
        )
    )


def is_valid_short_answer(text: str) -> bool:
    text = normalize_text(text).strip()
    if len(text) < 50:
        return False
    if text.endswith(":"):
        return False
    if is_question_sentence(text):
        return False
    if is_fluff(text):
        return False
    if is_junk_sentence(text):
        return False
    if re.search(r"this article shares \d+ practical strategies to help you improve results related to", text, re.I):
        return False
    if re.search(r"this article explains \d+ ways .+ and how it applies to growing your business", text, re.I):
        return False
    return True


def first_substantive_sentence(text: str, max_len: int = 220) -> str:
    for sentence in split_sentences(text):
        candidate = trim_sentence(sentence, max_len)
        if is_valid_short_answer(candidate):
            return candidate
    return ""


def title_is_comparison(title: str) -> bool:
    return bool(re.search(r"\bvs\.?\b", title, re.I))


def title_topic_words(title: str) -> set[str]:
    words = re.findall(r"[a-z0-9']+", title.lower())
    return {w for w in words if w not in STOP_WORDS and len(w) > 2}


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def score_sentence(sentence: str, title_words: set[str], *, want_definition: bool = False, want_why: bool = False) -> int:
    if is_fluff(sentence) or is_question_sentence(sentence) or is_junk_sentence(sentence):
        return -100
    lower = sentence.lower()
    score = 0
    overlap = sum(1 for w in title_words if w in lower)
    score += overlap * 5
    if want_why and overlap == 0:
        score -= 12
    if want_definition and re.search(r"\b(is|are|means|refers to|defined as)\b", sentence, re.I):
        score += 10
    if want_why and re.search(r"\b(important|because|essential|critical|helps|benefit|need|effective|valuable|worth|roi|return on investment)\b", lower):
        score += 5
    if re.search(r"^(they|it|this trend|these)\b", lower):
        score -= 4
    if len(sentence) < 40:
        score -= 3
    if len(sentence) > 260:
        score -= 2
    return score


def pick_best_sentence(candidates: list[str], title_words: set[str], **kwargs) -> str:
    best = ""
    best_score = -999
    for text in candidates:
        for sentence in split_sentences(text):
            s = score_sentence(sentence, title_words, **kwargs)
            if s > best_score:
                best_score = s
                best = sentence
    return trim_sentence(best, 220) if best and is_valid_short_answer(best) else ""


def find_comparison_answer(
    title: str,
    paragraphs: list[str],
    title_words: set[str],
    sections: list[tuple[str, str]] | None = None,
) -> str:
    title_l = normalize_text(title).lower()

    if sections:
        ans = find_conclusion_answer(sections, title_words)
        if ans:
            return ans

    if "social media" in title_l and re.search(r"\bvs\.?\b", title_l):
        return (
            "Social media management keeps your profiles active, consistent, and on-brand, "
            "while social media growth focuses on expanding reach and attracting new followers—"
            "most businesses need both, but at different stages."
        )

    for para in reversed(paragraphs):
        if is_fluff(para):
            continue
        pl = normalize_text(para).lower()
        if title_is_comparison(title) and ("agency" in pl or "in-house" in pl or "outsourc" in pl):
            ans = pick_best_sentence([para], title_words)
            if ans:
                return ans

    if "in-house" in title_l and "agency" in title_l:
        return (
            "The choice between in-house and agency marketing depends entirely on your situation—"
            "weigh factors like cost, expertise, culture fit, and speed. "
            "Many businesses also combine both when needs are split evenly."
        )

    sides = re.split(r"\bvs\.?\b", normalize_text(title), maxsplit=1, flags=re.I)
    if len(sides) == 2:
        left, right = (s.strip() for s in sides)
        if "|" in right:
            right = right.split("|", 1)[0].strip()
        if len(left) <= 40 and len(right) <= 40:
            return (
                f"When choosing between {left.lower()} and {right.lower().rstrip('?')}, "
                f"weigh cost, expertise, speed, and how much day-to-day control your team needs."
            )
    return ""


def extract_sections(prose_html: str) -> list[tuple[str, str]]:
    """Return (heading, body text) pairs for h2–h4 sections."""
    sections = []
    parts = re.split(r"(<h[234][^>]*>.*?</h[234]>)", prose_html, flags=re.I | re.S)
    for i in range(1, len(parts), 2):
        heading = strip_html(parts[i])
        body_html = parts[i + 1] if i + 1 < len(parts) else ""
        paras = []
        for match in re.finditer(r"<p[^>]*>(.*?)</p>", body_html, flags=re.I | re.S):
            text = strip_html(match.group(1))
            if len(text) > 25:
                paras.append(text)
        body = " ".join(paras)
        if heading:
            sections.append((heading, body))
    return sections


def section_paragraphs(prose_html: str) -> list[tuple[str, list[str]]]:
    sections = []
    parts = re.split(r"(<h[234][^>]*>.*?</h[234]>)", prose_html, flags=re.I | re.S)
    for i in range(1, len(parts), 2):
        heading = strip_html(parts[i])
        body_html = parts[i + 1] if i + 1 < len(parts) else ""
        paras = []
        for match in re.finditer(r"<p[^>]*>(.*?)</p>", body_html, flags=re.I | re.S):
            text = strip_html(match.group(1))
            if len(text) > 25 and not is_fluff(text):
                paras.append(text)
        if heading:
            sections.append((heading, paras))
    return sections


def heading_is_definition(heading: str) -> bool:
    h = heading.lower().strip("? ")
    return bool(re.search(r"^what (is|are)\b", h)) or "what is" in h or "what are" in h


def heading_is_why(heading: str) -> bool:
    h = heading.lower().strip("? ")
    return bool(re.search(r"^why\b", h)) or h.startswith("why use") or "why should" in h


def heading_is_how(heading: str) -> bool:
    h = heading.lower().strip("? ")
    return bool(re.search(r"^how (to|do|can|should|often)\b", h))


def heading_is_conclusion(heading: str) -> bool:
    h = normalize_text(heading).lower().strip("? ")
    return h in {"conclusion", "summary", "final thoughts", "the bottom line", "in summary"}


def find_conclusion_answer(sections: list[tuple[str, str]], title_words: set[str]) -> str:
    for heading, body in sections:
        if not heading_is_conclusion(heading) or not body:
            continue

        valid = [s for s in split_sentences(body) if is_valid_short_answer(s)]
        if not valid:
            ans = first_substantive_sentence(body)
            if ans:
                return trim_sentence(ans, 240)
            continue

        lead = trim_sentence(valid[0], 220)
        for follow in valid[1:3]:
            fl = normalize_text(follow).lower()
            if any(k in fl for k in ("both", "hybrid", "do both", "either", "can be the correct")):
                extra = first_sentence(follow, 130)
                combined = trim_sentence(f"{lead} {extra}", 260)
                if is_valid_short_answer(first_sentence(combined, 220)):
                    return combined
        return lead
    return ""


def topic_from_title(title: str) -> str:
    patterns = [
        r"what is (?:a|an)?\s*(.+?)(?:\?|&|$)",
        r"what are\s*(.+?)(?:\?|&|$)",
        r"thinking about\s*(.+?)\?",
        r"everything businesses need to know about\s*(.+?)(?:\?|$)",
    ]
    for pat in patterns:
        m = re.search(pat, title, re.I)
        if m:
            return m.group(1).strip(" ?.&")
    return ""


def synthesize_definition(title: str, paragraphs: list[str]) -> str:
    topic = topic_from_title(title)
    topic_l = topic.lower()
    if not topic:
        return ""

    if "hashtag" in topic_l:
        return (
            "A hashtag is a keyword or phrase prefixed with # that labels social media posts "
            "and helps users discover content on a specific topic."
        )

    if "social media management" in topic_l:
        return (
            "Social media management means having a dedicated team handle your brand's content, "
            "posting schedule, and engagement so your profiles stay active and professional."
        )

    return ""


def find_thinking_about_answer(title: str, paragraphs: list[str]) -> str:
    topic = topic_from_title(title)
    if not topic:
        return ""
    topic_words = [w for w in topic.lower().split() if len(w) > 3]
    for para in reversed(paragraphs):
        if is_fluff(para):
            continue
        lower = para.lower()
        if sum(1 for w in topic_words if w in lower) >= max(1, len(topic_words) // 2):
            sentence = pick_best_sentence([para], set(topic_words))
            if sentence:
                return sentence
    return ""


def find_definition_answer(title: str, paragraphs: list[str], sections: list[tuple[str, str]], title_words: set[str]) -> str:
    synthesized = synthesize_definition(title, paragraphs)
    if synthesized:
        return synthesized

    for heading, body in sections:
        if heading_is_definition(heading) and body:
            ans = pick_best_sentence([body], title_words, want_definition=True)
            if ans:
                return ans

    definitional = [
        p for p in paragraphs
        if not is_fluff(p)
        and re.search(r"\b(\w+\s+is|\w+\s+are|is a|is an|means|refers to|defined as)\b", p, re.I)
    ]
    ans = pick_best_sentence(definitional or [p for p in paragraphs if not is_fluff(p)], title_words, want_definition=True)
    if ans:
        return ans

    for para in paragraphs:
        if not is_fluff(para):
            return first_sentence(para, 220)
    return first_sentence(paragraphs[0], 220) if paragraphs else ""


def find_why_answer(title: str, paragraphs: list[str], sections: list[tuple[str, str]], title_words: set[str]) -> str:
    synthesized = synthesize_title_fallback(title)
    if synthesized and "customer satisfaction survey" in title.lower():
        return synthesized

    for para in paragraphs[:3]:
        if is_fluff(para) or is_junk_sentence(para):
            continue
        overlap = sum(1 for w in title_words if w in para.lower())
        if overlap >= 2:
            ans = first_substantive_sentence(para)
            if ans:
                return ans

    anchors = [w for w in ("seo", "hashtag", "landing", "ppc", "ads", "branding", "survey") if w in title_words]

    for heading, body in sections:
        if heading_is_why(heading) and body:
            ans = pick_best_sentence([body], title_words, want_why=True)
            if ans:
                return ans

    if anchors:
        for para in paragraphs:
            if is_fluff(para):
                continue
            pl = para.lower()
            if all(a in pl for a in anchors[:1]):
                ans = pick_best_sentence([para], title_words, want_why=True)
                if ans:
                    return ans

    why_paras = [
        p for p in paragraphs
        if re.search(r"\b(important|because|essential|helps|benefit|critical|worth|effective|roi|return on investment)\b", p, re.I)
        and not is_fluff(p)
    ]
    ans = pick_best_sentence(why_paras, title_words, want_why=True)
    if ans:
        return ans

    for para in paragraphs[1:5]:
        if not is_fluff(para):
            ans = pick_best_sentence([para], title_words, want_why=True)
            if ans and score_sentence(ans, title_words, want_why=True) > 4:
                return ans
    return ""


def find_how_answer(title: str, paragraphs: list[str], sections: list[tuple[str, str]], title_words: set[str]) -> str:
    for heading, body in sections:
        if heading_is_how(heading) and body:
            ans = pick_best_sentence([body], title_words)
            if ans:
                return ans

    for para in paragraphs:
        if is_fluff(para):
            continue
        if re.search(r"\b(start by|begin by|first,|step|should|can)\b", para, re.I):
            ans = first_sentence(para, 220)
            if ans:
                return ans
    return ""


def extract_numbered_headings(prose_html: str) -> list[str]:
    """Numbered h4/h5 list section titles (e.g. '1) Myth name' or '1. Mistake name')."""
    items = []
    for tag in ("h4", "h5"):
        for match in re.finditer(rf"<{tag}[^>]*>(.*?)</{tag}>", prose_html, flags=re.I | re.S):
            heading = strip_html(match.group(1))
            hc = normalize_text(heading).strip()
            m = re.match(r"^\d+[\)\.]\s*(.+)", hc)
            if m:
                items.append(m.group(1).strip())
    return items


def list_section_titles(sections: list[tuple[str, str]]) -> list[str]:
    skip_keywords = (
        "conclusion", "summary", "ready to grow", "explore our services",
        "grow your social", "navigation", "services", "locations", "webinar",
        "wsi can help", "steps to creating",
    )
    titles = []
    for heading, body in sections:
        raw = normalize_text(heading).strip()
        hc = raw.rstrip(":")
        hl = hc.lower()
        if any(k in hl for k in skip_keywords):
            continue
        if "?" in hc and len(hc) > 80:
            continue
        if is_fluff(hc):
            continue
        m = re.match(r"^\d+[\)\.]\s*(.+)", raw)
        if m:
            titles.append(m.group(1).strip())
            continue
        if re.match(r"^(Facebook|Instagram|Twitter|Snapchat|LinkedIn|TikTok|YouTube)\b", hc, re.I):
            titles.append(hc)
            continue
        if 8 < len(hc) < 55 and (body or raw.endswith(":")):
            if not hl.startswith("today") and not hl.startswith("what is"):
                titles.append(hc)
    return titles


def listicle_subject(title: str) -> str:
    subject = re.sub(r"^(\d+|five|six|seven)\s+", "", title.strip(), flags=re.I)
    subject = re.sub(r"^(creative\s+)?ways\s+(to|for)\s+", "", subject, flags=re.I)
    return subject.rstrip("?.")


def extract_listicle_topic(title: str) -> str:
    topic = re.sub(
        r"^\d+\s+(ways|tips|tactics|major|creative|signs|steps)\s+(to|for|about|your|of)?\s*",
        "",
        title.lower(),
    )
    topic = re.sub(r"^five\s+(social media )?(post )?(ideas|ways)\s+(for|to|when)\s*", "", topic)
    return topic.strip(" ?.&|")


def is_listicle_title(title: str) -> bool:
    title_l = title.lower()
    if re.match(r"^\d+\s", title_l):
        return True
    return bool(
        re.search(r"\b(myths|mistakes|signs|tips|tactics|ways|ideas|types of)\b", title_l)
    )


def synthesize_listicle_from_sections(title: str, sections: list[tuple[str, str]], prose_html: str = "") -> str:
    title_l = title.lower()
    titles = extract_numbered_headings(prose_html) if prose_html else []
    if not titles:
        titles = list_section_titles(sections)
    if not titles:
        return ""

    count_match = re.search(r"^(\d+)\b", title_l) or re.search(r"^five\b", title_l, re.I)
    count = (
        "5" if title_l.startswith("five")
        else count_match.group(1) if count_match
        else str(len(titles))
    )
    subject = listicle_subject(title).lower()
    preview = ", ".join(t.lower().rstrip(":") for t in titles[:3])

    if "myth" in title_l:
        lead = titles[0].lower()
        return (
            f"This article debunks {count} common social media myths—including \"{lead}\"—"
            f"and explains what to focus on instead."
        )
    if "mistake" in title_l:
        lead = titles[0].lower()
        return (
            f"Common social media mistakes include {lead}, inconsistent or irrelevant posting, "
            f"and failing to engage followers—this article explains how to avoid them."
        )
    if "sign" in title_l:
        return (
            f"This article highlights {count} warning signs—such as {titles[0].lower()}—"
            f"that indicate you may need professional help."
        )
    if "ideas" in title_l or "post ideas" in title_l:
        return (
            f"When you're stuck for content, try ideas like {preview}—"
            f"these formats help humanize your brand and drive engagement."
        )
    if re.search(r"\b(ways|tips|tactics|creative)\b", title_l):
        subject = listicle_subject(title).lower()
        if re.match(r"^(paid search tactics|creative ways)\b", subject):
            return f"This article outlines {count} {subject}, including {preview}."
        return f"This article shares {count} ways to {subject}, including {preview}."
    return f"This article covers {count} key points about {subject}, including {preview}."


def find_choice_answer(title: str, excerpt: str, sections: list[tuple[str, str]]) -> str:
    clean = clean_excerpt(excerpt)
    if clean and is_valid_short_answer(clean):
        return trim_sentence(clean, 220)

    platforms = list_section_titles(sections)
    if platforms:
        names = ", ".join(p.rstrip(":") for p in platforms[:3])
        return (
            f"Focus on the one or two platforms that best fit your audience and content—"
            f"such as {names}—rather than trying to be active on every network."
        )
    return (
        "Focus on the one or two social platforms where your target audience is most active "
        "and that fit your content strengths—not every network at once."
    )


def find_mistakes_answer(title: str, sections: list[tuple[str, str]], prose_html: str) -> str:
    if "mistake" not in title.lower():
        return ""
    return synthesize_listicle_from_sections(title, sections, prose_html)


def find_types_answer(title: str, list_items: list[str], paragraphs: list[str]) -> str:
    if "types of" not in title.lower():
        return ""
    if "facebook" in title.lower():
        for para in paragraphs:
            if is_fluff(para) or is_junk_sentence(para):
                continue
            for sentence in split_sentences(para):
                sl = sentence.lower()
                if "facebook" in sl and any(w in sl for w in ("format", "type", "video", "photo", "event", "carousel")):
                    if is_valid_short_answer(trim_sentence(sentence, 220)):
                        return trim_sentence(sentence, 220)
        return (
            "Facebook ads come in several formats—including video, photo, and event ads—"
            "and the best type depends on your campaign goal, audience, and creative quality."
        )
    return ""


def synthesize_title_fallback(title: str) -> str:
    title_l = title.lower().rstrip("?")
    if "customer satisfaction survey" in title_l:
        return (
            "Customer satisfaction surveys give you direct feedback on what buyers value, "
            "where you fall short, and how to improve retention—often at lower cost than other research."
        )
    if "content audit" in title_l:
        return (
            "Run a full content audit at least once a year, with more frequent reviews "
            "for high-traffic or time-sensitive pages so your site stays accurate and competitive."
        )
    if "portfolio website" in title_l:
        return (
            "A portfolio website showcases your best work, builds credibility with prospects, "
            "and gives you a professional hub beyond social profiles alone."
        )
    if "introvert" in title_l and "social media" in title_l:
        return (
            "Introverts can succeed on social media by choosing lower-pressure platforms, "
            "batching content, and focusing on thoughtful written posts rather than constant live visibility."
        )
    if "business entity" in title_l and "franchise" in title_l:
        return (
            "The best business entity for a franchise depends on liability protection, tax treatment, "
            "and how much operational control you want—LLC, S-corp, and C-corp each trade off differently."
        )
    return f"This article explains {title_l} and how it applies to growing your business."


def find_listicle_answer(
    title: str,
    paragraphs: list[str],
    title_words: set[str],
    sections: list[tuple[str, str]] | None = None,
    prose_html: str = "",
) -> str:
    if sections is not None:
        ans = synthesize_listicle_from_sections(title, sections, prose_html)
        if ans and is_valid_short_answer(ans):
            return ans

    m = re.search(r"^(\d+)\s", title.lower())
    if m:
        topic = extract_listicle_topic(title)
        for para in paragraphs:
            if is_fluff(para) or is_junk_sentence(para):
                continue
            if topic and any(w in para.lower() for w in topic.split() if len(w) > 3):
                ans = first_substantive_sentence(para)
                if ans:
                    return ans
    return ""


def make_short_answer(title: str, paragraphs: list[str], excerpt: str, prose_html: str = "") -> str:
    title_clean = html.unescape(title).strip()
    title_l = title_clean.lower()
    title_words = title_topic_words(title_clean)
    sections = extract_sections(prose_html) if prose_html else []
    list_items = extract_list_items(prose_html) if prose_html else []

    parts: list[str] = []

    wants_choice = bool(re.search(r"\bwhich\b", title_l) or "should you focus" in title_l)
    wants_definition = bool(
        re.search(r"\bwhat (is|are)\b", title_l)
        or title_l.startswith("what ")
        or ("everything" in title_l and "know about" in title_l)
        or "thinking about" in title_l
    )
    wants_how = bool(
        re.search(r"\bhow (to|do|can|should|often)\b", title_l) or title_l.startswith("how ")
    )
    wants_why = bool(
        re.search(r"\bwhy\b", title_l)
        or ("important" in title_l and not wants_definition)
        or ("should you" in title_l and not wants_choice and not wants_how)
    )

    if wants_choice:
        ans = find_choice_answer(title_clean, excerpt, sections)
        if ans:
            parts.append(ans)

    if is_listicle_title(title_clean) and not parts:
        ans = find_listicle_answer(title_clean, paragraphs, title_words, sections, prose_html)
        if ans:
            parts.append(ans)

    if "mistake" in title_l and not parts:
        ans = find_mistakes_answer(title_clean, sections, prose_html)
        if ans:
            parts.append(ans)

    if "types of" in title_l and not parts:
        ans = find_types_answer(title_clean, list_items, paragraphs)
        if ans:
            parts.append(ans)

    if not parts and (
        ("guide" in title_l and "social media" in title_l)
        or ("business entity" in title_l and "franchise" in title_l)
    ):
        ans = synthesize_title_fallback(title_clean)
        if ans and is_valid_short_answer(ans):
            parts.append(ans)

    if wants_definition and not parts:
        if "thinking about" in title_l:
            ans = synthesize_definition(title_clean, paragraphs) or find_thinking_about_answer(title_clean, paragraphs)
        else:
            ans = find_definition_answer(title_clean, paragraphs, sections, title_words)
        if ans:
            parts.append(ans)

    if wants_why and not parts:
        ans = find_why_answer(title_clean, paragraphs, sections, title_words)
        if ans and ans not in parts:
            if not parts or ans[:40] not in parts[0]:
                parts.append(ans)

    if wants_how and not parts:
        if "portfolio" in title_l:
            ans = synthesize_title_fallback(title_clean)
            if ans and is_valid_short_answer(ans):
                parts.append(ans)
        if not parts:
            ans = find_how_answer(title_clean, paragraphs, sections, title_words)
            if ans and is_valid_short_answer(ans) and ans not in parts and len(parts) < 2:
                parts.append(ans)

    if not parts:
        if title_is_comparison(title_clean):
            ans = find_comparison_answer(title_clean, paragraphs, title_words, sections)
            if ans:
                parts.append(ans)

    if not parts:
        ans = find_conclusion_answer(sections, title_words)
        if ans:
            parts.append(ans)

    if not parts and is_listicle_title(title_clean):
        ans = find_listicle_answer(title_clean, paragraphs, title_words, sections, prose_html)
        if ans and is_valid_short_answer(ans):
            parts.append(ans)

    if not parts:
        for para in paragraphs:
            if is_fluff(para) or is_junk_sentence(para):
                continue
            ans = first_substantive_sentence(para)
            if ans:
                parts.append(ans)
                break

    if not parts:
        for para in paragraphs:
            if is_fluff(para):
                continue
            ans = pick_best_sentence([para], title_words)
            if ans and is_valid_short_answer(ans):
                parts.append(ans)
                break

    excerpt_clean = clean_excerpt(excerpt)
    if not parts and excerpt_clean:
        if is_valid_short_answer(excerpt_clean):
            parts.append(trim_sentence(excerpt_clean, 220))
        else:
            ans = first_substantive_sentence(excerpt_clean)
            if ans:
                parts.append(ans)

    if not parts:
        fallback = synthesize_title_fallback(title_clean)
        if is_valid_short_answer(fallback):
            parts.append(fallback)

    parts = [p for p in parts if is_valid_short_answer(p)] or parts[:1]

    if not parts:
        parts.append(
            f"This article explains what you need to know about {title_clean.rstrip('?').lower()}."
        )

    if len(parts) == 1:
        return parts[0]

    lead = first_sentence(parts[0], 200) if len(parts[0]) > 200 else parts[0]
    combined = f"{lead} {parts[1]}"
    return trim_sentence(combined, 260)


def clean_excerpt(excerpt: str) -> str:
    excerpt = re.sub(r"\s+", " ", normalize_text(excerpt)).strip()
    if not excerpt:
        return ""
    if excerpt.lower() in ("case study",):
        return ""
    if is_question_sentence(excerpt.split("?")[0] + "?") and "?" in excerpt[:120]:
        # Excerpt opens with a rhetorical question — prefer body content instead.
        after = excerpt.split("?", 1)[-1].strip()
        if len(after) > 60 and not after[0].islower():
            excerpt = after
        else:
            return ""
    # posts.json excerpts are often truncated mid-word
    if len(excerpt) > 180 and not excerpt.endswith((".", "!", "?", "…")):
        return ""
    return excerpt


def make_summary(excerpt: str, paragraphs: list[str]) -> str:
    clean = clean_excerpt(excerpt)
    parts = []
    if clean:
        parts.append(trim_sentence(clean, 300))
    for para in paragraphs[:2]:
        candidate = trim_sentence(para, 300)
        if not candidate:
            continue
        if parts and candidate.startswith(parts[0][:60]):
            continue
        parts.append(candidate)
        if len(parts) >= 2:
            break
    if not parts and paragraphs:
        parts.append(trim_sentence(paragraphs[0], 320))
    return " ".join(parts[:2])


def make_takeaways(
    title: str,
    headings: list[str],
    list_items: list[str],
    paragraphs: list[str],
    sections: list[tuple[str, str]],
) -> list[str]:
    takeaways: list[str] = []

    for item in list_items:
        if item not in takeaways:
            takeaways.append(trim_sentence(item, 160))
        if len(takeaways) >= 4:
            return takeaways[:4]

    skip = {
        "introduction",
        "conclusion",
        "summary",
        "in summary",
        "final thoughts",
        "learn more",
        "contact us",
    }
    skip_prefixes = ("the main reasons", "main reasons why", "in this article", "overview")
    for heading, para in sections:
        lower = heading.lower()
        if lower in skip or any(lower.startswith(p) for p in skip_prefixes):
            continue
        if para:
            takeaways.append(trim_sentence(first_sentence(para, 150), 160))
        elif re.match(r"^\d+\.", heading) or re.match(r"^\d+\s", heading):
            takeaways.append(trim_sentence(heading, 160))
        else:
            takeaways.append(trim_sentence(heading_to_takeaway(heading), 160))
        if len(takeaways) >= 4:
            return takeaways[:4]

    for heading in headings:
        if heading.lower() in skip:
            continue
        takeaways.append(trim_sentence(heading_to_takeaway(heading), 160))
        if len(takeaways) >= 4:
            return takeaways[:4]

    if paragraphs:
        for para in paragraphs[1:4]:
            takeaways.append(trim_sentence(first_sentence(para, 140), 160))
            if len(takeaways) >= 4:
                break

    if len(takeaways) < 3:
        takeaways.append(f"This article covers practical guidance related to {title.lower()}.")
    if len(takeaways) < 3:
        takeaways.append("Apply these ideas consistently to improve results over time.")

    return takeaways[:4]


def heading_to_takeaway(heading: str) -> str:
    heading = heading.strip().rstrip("?")
    if re.match(r"^\d+\s", heading):
        return heading
    return heading + "."


def intro_html(short_answer: str, summary: str, takeaways: list[str]) -> str:
    bullets = "\n".join(
        f'          <li>{html.escape(t)}</li>' for t in takeaways
    )
    return f"""      <div class="blog-intro">
        <div class="blog-short-answer">
          <span class="blog-short-answer__label">Short Answer</span>
          <p class="blog-short-answer__text">{html.escape(short_answer)}</p>
        </div>
        <div class="blog-summary">
          <h2 class="blog-summary__title">Summary</h2>
          <p class="blog-summary__text">{html.escape(summary)}</p>
        </div>
        <div class="blog-takeaways">
          <h2 class="blog-takeaways__title">Key Takeaways</h2>
          <ul class="blog-takeaways__list">
{bullets}
          </ul>
        </div>
      </div>"""


def updated_meta_html() -> str:
    return f'<span class="post-updated">{UPDATED_LINE}</span>'


def generate_intro(prose_html: str, title: str, excerpt: str) -> str:
    paragraphs = extract_paragraphs(prose_html)
    headings = extract_headings(prose_html)
    list_items = extract_list_items(prose_html)
    sections = extract_sections(prose_html)
    short_answer = make_short_answer(title, paragraphs, excerpt, prose_html)
    summary = make_summary(excerpt, paragraphs)
    takeaways = make_takeaways(title, headings, list_items, paragraphs, sections)
    return intro_html(short_answer, summary, takeaways)


def load_posts_meta() -> dict[str, dict]:
    data = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    return {p["slug"]: p for p in data}


def patch_post_html(file_path: Path, meta: dict) -> bool:
    slug = file_path.stem
    if slug in SKIP_SLUGS:
        return False

    text = file_path.read_text(encoding="utf-8")
    changed = False

    # Remove existing intro if re-running
    text = re.sub(
        r'\s*<div class="blog-intro">[\s\S]*?(?=<div class="blog-prose">)',
        "\n",
        text,
        count=1,
    )

    prose_match = re.search(r'(<div class="blog-prose">)(.*?)(</div>\s*\n\s*</article>)', text, flags=re.S)
    if not prose_match:
        return False

    prose_html = prose_match.group(2)
    title = html.unescape(meta.get("title", slug.replace("-", " ").title()))
    excerpt = meta.get("excerpt", "")
    intro_block = generate_intro(prose_html, title, excerpt)
    text = text.replace(
        prose_match.group(1),
        intro_block + "\n      " + prose_match.group(1),
        1,
    )
    changed = True

    updated_tag = updated_meta_html()
    if updated_tag not in text:
        text = re.sub(
            r'(<div class="post-meta">.*?)(</div>)',
            lambda m: m.group(1) + updated_tag + m.group(2),
            text,
            count=1,
            flags=re.S,
        )
        changed = True

    if changed:
        file_path.write_text(text, encoding="utf-8")
        return True
    return False


def intro_block_for_build(prose_html: str, title: str, excerpt: str, slug: str) -> str:
    if slug in SKIP_SLUGS:
        return ""
    return generate_intro(prose_html, title, excerpt)


def updated_meta_for_build(slug: str) -> str:
    if slug in SKIP_SLUGS:
        return ""
    return updated_meta_html()
