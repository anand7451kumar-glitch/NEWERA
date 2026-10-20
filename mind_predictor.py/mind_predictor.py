#!/usr/bin/env python3
"""
mind_predictor.py - guess what you're thinking about right now, from your own history.

It cannot read minds. It learns patterns from what you've written before:
  1. Similar-moment matching : finds past messages like what you just wrote (TF-IDF + cosine)
                               and looks at what you wrote NEXT each time.
  2. Time-of-day habits      : what you tend to think about at this hour.
  3. Style generation        : a Markov chain that writes a likely thought in your voice.
  4. Feedback loop           : tell it what you were really thinking and it learns.

Supported history files (everything stays on your machine):
  .txt   one message per line, or WhatsApp export lines
         ("[12/03/2026, 21:14] Name: text" or "12/03/2026, 9:14 pm - Name: text")
  .json  ["msg", ...]  or  [{"text": "...", "timestamp": "2026-03-12T21:14:00"}, ...]
  .jsonl one JSON object per line, same fields as above

Usage:
  python mind_predictor.py chat.txt                 # interactive
  python mind_predictor.py chat.txt --me "Rahul"    # keep only your messages (WhatsApp)
  python mind_predictor.py chat.txt -q "need to finish the report"   # one-shot
  python mind_predictor.py --demo                   # try it with fake data
"""
import argparse
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

STOP = set("""a an the and or but if so of to in on at for with from by is are was were be been am i me my
mine you your we our it its this that these those there here do does did have has had not no yes just
very really can could will would should shall may might as than then too also about into over out up
down what when where who why how all any some more most im ive dont didnt cant wont ok okay lol""".split())

WORD = re.compile(r"[a-zA-Z\u0900-\u097F']+")  # latin + devanagari (Hindi) letters


def tokenize(text):
    return [w for w in (t.lower().strip("'") for t in WORD.findall(text)) if len(w) > 2 and w not in STOP]


@dataclass
class Msg:
    text: str
    hour: Optional[int] = None


# ----------------------------------------------------------------------------- loading
WA = re.compile(
    r"^\[?(?P<d>\d{1,4}[/.\-]\d{1,2}[/.\-]\d{1,4}),?\s+(?P<h>\d{1,2}):(?P<m>\d{2})(?::\d{2})?\s*(?P<ap>[APap]\.?[Mm]\.?)?\]?"
    r"\s*[-\u2013]?\s*(?P<who>[^:]{1,40}):\s*(?P<text>.*)$")


def _hour_from_iso(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "")).hour
    except ValueError:
        return None


def load_history(path, me=None):
    p = Path(path)
    msgs = []
    if not p.exists():
        return msgs
    raw = p.read_text(encoding="utf-8", errors="ignore")
    if p.suffix == ".json":
        for item in json.loads(raw):
            if isinstance(item, str):
                msgs.append(Msg(item))
            elif isinstance(item, dict) and item.get("text"):
                msgs.append(Msg(item["text"], _hour_from_iso(item.get("timestamp"))))
    elif p.suffix == ".jsonl":
        for line in raw.splitlines():
            if line.strip():
                item = json.loads(line)
                msgs.append(Msg(item["text"], item.get("hour")))
    else:
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            m = WA.match(line)
            if m:
                if me and me.lower() not in m["who"].lower():
                    continue
                hour = int(m["h"]) % 12 + (12 if (m["ap"] or "").lower().startswith("p") else 0) \
                    if m["ap"] else int(m["h"])
                msgs.append(Msg(m["text"], hour))
            elif not me:
                msgs.append(Msg(line))
    return [m for m in msgs if m.text and "omitted" not in m.text.lower()]


# ----------------------------------------------------------------------------- model
def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


class MindModel:
    def __init__(self, msgs):
        self.msgs = msgs
        self.toks = [tokenize(m.text) for m in msgs]
        n = len(msgs)
        df = Counter(t for toks in self.toks for t in set(toks))
        self.idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
        self.vecs = [self._vec(t) for t in self.toks]
        # time-of-day habits
        self.by_hour = defaultdict(Counter)
        for m, toks in zip(msgs, self.toks):
            if m.hour is not None:
                for t in set(toks):
                    self.by_hour[m.hour][t] += self.idf[t]
        # bigram Markov chain over raw words, for generating a thought in your style
        self.chain = defaultdict(list)
        for m in msgs:
            w = ["<s>"] + m.text.lower().split() + ["</s>"]
            for a, b in zip(w, w[1:]):
                self.chain[a].append(b)

    def _vec(self, toks):
        tf = Counter(toks)
        v = {t: c * self.idf.get(t, 1.0) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {t: x / norm for t, x in v.items()}

    def predict(self, context, hour=None, k=8):
        ctx = self._vec(tokenize(context))
        sims = sorted(((cosine(ctx, v), i) for i, v in enumerate(self.vecs[:-1])), reverse=True)
        top = [(s, i) for s, i in sims[:k] if s > 0.08]

        score = Counter()
        for s, i in top:                      # what did you think about AFTER similar moments?
            for t in set(self.toks[i + 1]):
                score[t] += s * self.idf[t]
        total = sum(score.values()) or 1.0
        score = Counter({t: v / total for t, v in score.items()})

        if hour is not None and self.by_hour.get(hour):  # blend in time-of-day habits
            h = self.by_hour[hour]
            ht = sum(h.values()) or 1.0
            weight = 0.25 if top else 1.0
            for t, v in h.most_common(15):
                score[t] += weight * v / ht

        followers = [(s, self.msgs[i + 1].text) for s, i in top]
        seen, uniq = set(), []
        for s, text in followers:
            if text not in seen:
                seen.add(text)
                uniq.append((s, text))

        confidence = min(0.95, sum(s for s, _ in top[:3]) / 3) if top else 0.05
        return {
            "topics": score.most_common(5),
            "likely_thoughts": uniq[:3],
            "generated": self.generate(score.most_common(1)[0][0] if score else None),
            "confidence": confidence,
            "matches": len(top),
        }

    def generate(self, seed=None, max_words=14):
        if not self.chain:
            return ""
        starters = [w for w in self.chain if seed and seed in w] if seed else []
        out = []
        cur = random.choice(starters) if starters else random.choice(self.chain["<s>"])
        if cur in ("<s>", "</s>"):
            cur = random.choice(self.chain["<s>"])
        for _ in range(max_words):
            out.append(cur)
            nxt = random.choice(self.chain.get(cur, ["</s>"]))
            if nxt == "</s>":
                break
            cur = nxt
        return " ".join(out)


# ----------------------------------------------------------------------------- display
def show(pred):
    c = pred["confidence"]
    label = "strong pattern" if c > 0.5 else "weak pattern" if c > 0.2 else "guessing (little data like this)"
    print(f"\n  Prediction confidence: {c:.0%}  [{label}, {pred['matches']} similar past moments]")
    if pred["topics"]:
        print("  You're probably thinking about:  " + ", ".join(t for t, _ in pred["topics"]))
    for s, text in pred["likely_thoughts"]:
        print(f"  Last time you went on to say:   \"{text[:110]}\"  (match {s:.0%})")
    if pred["generated"]:
        print(f"  In your voice, maybe:           \"{pred['generated']}\"")
    print()


DEMO = [
    "need to finish the project report before friday", "deadline is stressing me out",
    "should i ask my manager for more time", "going to the gym tonight",
    "legs are sore after workout", "protein shake and sleep early",
    "what should i cook for dinner", "dal rice again maybe", "ordering food, too tired to cook",
    "project report still not done", "need coffee and focus", "manager replied about deadline",
    "weekend plan with friends", "movie or cricket match this weekend", "booking tickets for the movie",
    "need to finish the project report", "gym or rest day today", "feeling tired, sleep early tonight",
]


def main():
    ap = argparse.ArgumentParser(description="Predict what you're thinking from your chat history.")
    ap.add_argument("history", nargs="?", help="path to chat history (.txt/.json/.jsonl)")
    ap.add_argument("--me", help="your name in a WhatsApp-style export (keeps only your lines)")
    ap.add_argument("-q", "--query", help="what you just wrote/said (one-shot mode)")
    ap.add_argument("--demo", action="store_true", help="use built-in fake history")
    args = ap.parse_args()

    learned_path = None
    if args.demo:
        msgs = [Msg(t, 9 + (i % 12)) for i, t in enumerate(DEMO)]
    elif args.history:
        msgs = load_history(args.history, args.me)
        learned_path = Path(args.history).with_suffix(".learned.jsonl")
        msgs += load_history(learned_path)
    else:
        ap.error("give a history file or use --demo")
    if len(msgs) < 5:
        sys.exit("Need at least a few messages of history to learn from.")

    model = MindModel(msgs)
    print(f"Learned from {len(msgs)} messages. Type what you just said/did; Ctrl+C to quit.")

    if args.query:
        show(model.predict(args.query, datetime.now().hour))
        return
    try:
        while True:
            ctx = input("you> ").strip()
            if not ctx:
                continue
            show(model.predict(ctx, datetime.now().hour))
            real = input("what were you actually thinking? (Enter to skip)> ").strip()
            if real:
                msgs.append(Msg(ctx, datetime.now().hour))
                msgs.append(Msg(real, datetime.now().hour))
                if learned_path:
                    with learned_path.open("a", encoding="utf-8") as f:
                        for m in msgs[-2:]:
                            f.write(json.dumps({"text": m.text, "hour": m.hour}) + "\n")
                model = MindModel(msgs)
                print("  (learned)\n")
    except (KeyboardInterrupt, EOFError):
        print("\nbye")


if __name__ == "__main__":
    main()