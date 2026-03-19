import os, json, time, hashlib

DEFAULT_CONFIG = {
    "canonical_summary_path": "docs/canonical/system_summary.md",
    "feedback_path": "payload/feedback/canonical_feedback.json",
    "state_score_path": "payload/state_scoring/state_score.json",
    "marketing_root": "marketing",
    "receipts_root": "payload/receipts/marketing_system",
    "max_priority_items": 8,
    "platforms": ["linkedin", "x", "substack", "github"]
}

def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""

def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()

def _ensure_dirs(root):
    for rel in [
        "post_templates",
        "scheduled_posts",
        "published_posts",
        "performance"
    ]:
        os.makedirs(os.path.join(root, rel), exist_ok=True)

def main():
    cfg = _load_json("config/marketing_system_config.json", DEFAULT_CONFIG)
    merged = DEFAULT_CONFIG.copy()
    if isinstance(cfg, dict):
        merged.update(cfg)

    root = merged["marketing_root"]
    receipts_root = merged["receipts_root"]
    os.makedirs(receipts_root, exist_ok=True)
    _ensure_dirs(root)

    summary = _read_text(merged["canonical_summary_path"])
    feedback = _load_json(merged["feedback_path"], {})
    state_score = _load_json(merged["state_score_path"], {})

    priority_items = feedback.get("priority_items", [])[: int(merged.get("max_priority_items", 8))]
    invariant_candidates = feedback.get("invariant_candidates", [])[: int(merged.get("max_priority_items", 8))]
    contradictions = feedback.get("contradictions", [])[: int(merged.get("max_priority_items", 8))]

    strategy_md = os.path.join(root, "strategy.md")
    with open(strategy_md, "w", encoding="utf-8") as f:
        f.write(
            "# Marketing Strategy\n\n"
            "## Positioning\n"
            "- Governed execution systems\n"
            "- Deterministic AI infrastructure\n"
            "- Receipts over opaque logs\n\n"
            "## Core content types\n"
            "- system insight posts\n"
            "- build in public updates\n"
            "- category creation posts\n\n"
            "## Current signals\n"
            f"- state_score_band: {state_score.get('band')}\n"
            f"- state_score: {state_score.get('score')}\n"
            f"- priority_items: {len(priority_items)}\n"
            f"- invariant_candidates: {len(invariant_candidates)}\n"
            f"- contradictions: {len(contradictions)}\n"
        )

    templates = {
        "linkedin_system_insight.md": (
            "# LinkedIn System Insight Template\n\n"
            "Hook:\n"
            "AI governance fails because execution is probabilistic.\n\n"
            "Body:\n"
            "Share one system insight, one concrete example from the repo, and one category-defining takeaway.\n"
        ),
        "x_thread_template.md": (
            "# X Thread Template\n\n"
            "1. Core claim\n"
            "2. Why current systems fail\n"
            "3. What governed execution changes\n"
            "4. Concrete repo proof point\n"
            "5. Closing line\n"
        ),
        "substack_longform_template.md": (
            "# Substack Longform Template\n\n"
            "Opening problem\n"
            "Why this matters\n"
            "System architecture\n"
            "Evidence from current build\n"
            "Next implications\n"
        )
    }

    for name, content in templates.items():
        with open(os.path.join(root, "post_templates", name), "w", encoding="utf-8") as f:
            f.write(content)

    post_seed = {
        "timestamp": time.time(),
        "platforms": merged.get("platforms", []),
        "priority_items": priority_items,
        "invariant_candidates": invariant_candidates,
        "contradictions": contradictions,
        "state_score": state_score,
        "summary_excerpt": summary[:2000]
    }
    with open(os.path.join(root, "content_log.json"), "w", encoding="utf-8") as f:
        json.dump(post_seed, f, indent=2, ensure_ascii=False)

    draft_md = os.path.join(root, "scheduled_posts", "next_posts.md")
    with open(draft_md, "w", encoding="utf-8") as f:
        f.write(
            "# Next Posts\n\n"
            "## Post 1 — System Insight\n"
            "We don't need smarter models. We need systems that can prove what they did.\n\n"
            "## Post 2 — Build in Public\n"
            "This system refuses to execute if state is invalid.\n\n"
            "## Post 3 — Category Creation\n"
            "Receipts are to AI execution what version control is to software.\n"
        )

    receipt = {
        "type": "marketing_system",
        "timestamp": time.time(),
        "marketing_root": root,
        "strategy_path": strategy_md,
        "content_log_path": os.path.join(root, "content_log.json"),
        "scheduled_posts_path": draft_md
    }
    receipt["hash"] = _sha256_obj(receipt)

    existing = sorted(f for f in os.listdir(receipts_root) if f.startswith("marketing_system_") and f.endswith(".json"))
    receipt_path = os.path.join(receipts_root, f"marketing_system_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "status": "ok",
        "marketing_root": root,
        "receipt_path": receipt_path
    }, indent=2))

if __name__ == "__main__":
    main()
