import argparse
import hashlib
import json
import os
import re
import time

CONFIG_PATH = "config/document_compactor_config.json"
DEFAULT_OUTPUT_ROOT = "docs/canonical"
DEFAULT_RECEIPTS_ROOT = "payload/receipts/document_compaction"

DEFAULT_CONFIG = {
    "scan_roots": ["."],
    "include_filename_patterns": [
        r"BUILD_NOTES_.*\.md$",
        r"EVAL_NOTES_.*\.md$",
        r"CLAIMS.*\.md$",
        r".*DEFINITIONS.*\.(md|json)$"
    ],
    "exclude_prefixes": [
        ".git/",
        "incoming_bundles/",
        "installed_bundles/",
        "failed_bundles/",
        "_tmp_bundle_",
        "docs/canonical/",
        "payload/receipts/document_compaction/"
    ],
    "max_files": 500,
    "max_excerpt_chars_per_file": 4000,
    "top_claims_limit": 25,
    "top_definitions_limit": 25,
    "top_findings_limit": 25
}

def _norm(path):
    return path.replace("\\", "/")

def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()

def _sha256_obj(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()

def _ensure_dirs(output_root, receipts_root):
    os.makedirs(output_root, exist_ok=True)
    os.makedirs(receipts_root, exist_ok=True)

def _load_config():
    if not os.path.exists(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_CONFIG.copy()
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        return merged
    except Exception:
        return DEFAULT_CONFIG.copy()

def _is_excluded(rel_path, exclude_prefixes):
    p = _norm(rel_path)
    for prefix in exclude_prefixes:
        if p.startswith(prefix):
            return True
    return False

def _matches(rel_path, patterns):
    p = _norm(rel_path)
    return any(re.search(pattern, p) for pattern in patterns)

def _collect_candidate_files(config):
    out = []
    seen = set()
    for root in config.get("scan_roots", ["."]):
        if not os.path.exists(root):
            continue
        for r, _, files in os.walk(root):
            for fn in files:
                full = os.path.join(r, fn)
                rel = _norm(os.path.relpath(full, "."))
                if rel in seen:
                    continue
                if _is_excluded(rel, config.get("exclude_prefixes", [])):
                    continue
                if _matches(rel, config.get("include_filename_patterns", [])):
                    out.append(rel)
                    seen.add(rel)
    out.sort()
    return out[: int(config.get("max_files", 500))]

def _read_text(path, max_chars):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()[:max_chars]
    except Exception:
        return ""

def _read_json_if_possible(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return None

def _extract_bullets(text):
    bullets = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*]\s+\S+", stripped):
            bullets.append(re.sub(r"^[-*]\s+", "", stripped))
        elif re.match(r"^\d+\.\s+\S+", stripped):
            bullets.append(re.sub(r"^\d+\.\s+", "", stripped))
    return bullets

def _extract_sentences(text):
    rough = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    cleaned = []
    for s in rough:
        s = " ".join(s.split()).strip()
        if len(s) >= 40:
            cleaned.append(s)
    return cleaned

def _dedupe_preserve_order(items):
    seen = set()
    out = []
    for item in items:
        key = " ".join(item.lower().split())
        if key in seen:
            continue
        seen.add(key)
        out.append(item.strip())
    return out

def _score_claim(s):
    score = 0
    sl = s.lower()
    for token in ["must", "should", "proves", "claim", "invariant", "deterministic", "receipt", "policy"]:
        if token in sl:
            score += 2
    score += min(len(s) // 60, 4)
    return score

def _score_definition(s):
    score = 0
    sl = s.lower()
    for token in [" is ", " means ", " defined ", "definition", "model", "system", "invariant", "receipt"]:
        if token in sl:
            score += 2
    score += min(len(s) // 70, 4)
    return score

def _score_finding(s):
    score = 0
    sl = s.lower()
    for token in ["result", "failure", "success", "issue", "works", "broke", "fixed", "generated"]:
        if token in sl:
            score += 2
    score += min(len(s) // 70, 4)
    return score

def _classify_text(text):
    bullets = _extract_bullets(text)
    sentences = _extract_sentences(text)
    material = _dedupe_preserve_order(bullets + sentences)
    claims, definitions, findings = [], [], []
    for item in material:
        sl = item.lower()
        if any(k in sl for k in ["must", "should", "therefore", "proves", "claim", "invariant", "execution", "policy"]):
            claims.append(item)
        if any(k in sl for k in [" is ", " means ", "defined", "definition", "model", "framework", "system"]):
            definitions.append(item)
        if any(k in sl for k in ["result", "failure", "success", "issue", "fixed", "generated", "output", "worked"]):
            findings.append(item)
    claims = sorted(_dedupe_preserve_order(claims), key=_score_claim, reverse=True)
    definitions = sorted(_dedupe_preserve_order(definitions), key=_score_definition, reverse=True)
    findings = sorted(_dedupe_preserve_order(findings), key=_score_finding, reverse=True)
    return claims, definitions, findings

def _parse_file(path, max_chars):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        data = _read_json_if_possible(path)
        text = json.dumps(data, indent=2, ensure_ascii=False)[:max_chars] if data is not None else _read_text(path, max_chars)
    else:
        text = _read_text(path, max_chars)
    claims, definitions, findings = _classify_text(text)
    return {
        "path": path,
        "hash": _sha256_text(text),
        "claims": claims,
        "definitions": definitions,
        "findings": findings,
        "excerpt": text[:500]
    }

def _write_markdown_list(title, items, sources, path):
    lines = [f"# {title}", ""]
    if not items:
        lines.append("_No items extracted._")
    else:
        for idx, item in enumerate(items, 1):
            lines.append(f"{idx}. {item}")
            srcs = sources.get(item, [])
            if srcs:
                lines.append(f"   - sources: {', '.join(srcs[:5])}")
    lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def compact(output_root=DEFAULT_OUTPUT_ROOT, receipts_root=DEFAULT_RECEIPTS_ROOT):
    config = _load_config()
    _ensure_dirs(output_root, receipts_root)
    candidate_files = _collect_candidate_files(config)
    parsed = [_parse_file(p, int(config.get("max_excerpt_chars_per_file", 4000))) for p in candidate_files]
    claim_sources, def_sources, finding_sources = {}, {}, {}
    claims_all, defs_all, findings_all = [], [], []
    for entry in parsed:
        for item in entry["claims"]:
            claims_all.append(item)
            claim_sources.setdefault(item, []).append(entry["path"])
        for item in entry["definitions"]:
            defs_all.append(item)
            def_sources.setdefault(item, []).append(entry["path"])
        for item in entry["findings"]:
            findings_all.append(item)
            finding_sources.setdefault(item, []).append(entry["path"])
    claims_ranked = sorted(_dedupe_preserve_order(claims_all), key=_score_claim, reverse=True)[: int(config.get("top_claims_limit", 25))]
    defs_ranked = sorted(_dedupe_preserve_order(defs_all), key=_score_definition, reverse=True)[: int(config.get("top_definitions_limit", 25))]
    findings_ranked = sorted(_dedupe_preserve_order(findings_all), key=_score_finding, reverse=True)[: int(config.get("top_findings_limit", 25))]
    summary = {
        "timestamp": time.time(),
        "scanned_files_count": len(candidate_files),
        "scanned_files": candidate_files,
        "claims_count": len(claims_ranked),
        "definitions_count": len(defs_ranked),
        "findings_count": len(findings_ranked),
        "parsed_files": parsed
    }
    summary["summary_hash"] = _sha256_obj({
        "scanned_files": candidate_files,
        "claims": claims_ranked,
        "definitions": defs_ranked,
        "findings": findings_ranked
    })
    with open(os.path.join(output_root, "compaction_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    _write_markdown_list("Canonical Claims", claims_ranked, claim_sources, os.path.join(output_root, "claims_canonical.md"))
    _write_markdown_list("Canonical Definitions", defs_ranked, def_sources, os.path.join(output_root, "definitions_canonical.md"))
    _write_markdown_list("Canonical Findings", findings_ranked, finding_sources, os.path.join(output_root, "findings_canonical.md"))
    lines = [
        "# System Summary", "",
        f"- scanned_files_count: {len(candidate_files)}",
        f"- claims_count: {len(claims_ranked)}",
        f"- definitions_count: {len(defs_ranked)}",
        f"- findings_count: {len(findings_ranked)}",
        f"- summary_hash: {summary['summary_hash']}", "",
        "## Top Claims"
    ]
    for item in claims_ranked[:10]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Top Definitions")
    for item in defs_ranked[:10]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Top Findings")
    for item in findings_ranked[:10]:
        lines.append(f"- {item}")
    with open(os.path.join(output_root, "system_summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    receipt = {
        "type": "document_compaction",
        "timestamp": summary["timestamp"],
        "summary_hash": summary["summary_hash"],
        "scanned_files": candidate_files,
        "outputs": [
            _norm(os.path.join(output_root, "compaction_summary.json")),
            _norm(os.path.join(output_root, "claims_canonical.md")),
            _norm(os.path.join(output_root, "definitions_canonical.md")),
            _norm(os.path.join(output_root, "findings_canonical.md")),
            _norm(os.path.join(output_root, "system_summary.md"))
        ]
    }
    receipt["hash"] = _sha256_obj(receipt)
    existing = sorted(f for f in os.listdir(receipts_root) if f.startswith("document_compaction_") and f.endswith(".json"))
    receipt_path = os.path.join(receipts_root, f"document_compaction_{len(existing)+1:04d}.json")
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)
    result = {"status": "ok", "summary_hash": summary["summary_hash"], "receipt_path": _norm(receipt_path), "output_root": _norm(output_root)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

def main():
    parser = argparse.ArgumentParser(description="Compact generated research and build notes into canonical documents.")
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--receipts-root", default=DEFAULT_RECEIPTS_ROOT)
    args = parser.parse_args()
    compact(output_root=args.output_root, receipts_root=args.receipts_root)

if __name__ == "__main__":
    main()
