"""
Extract Confluence images downloaded in the current Claude Code session.

When `confluence_download_attachment` is called in a Claude session, the returned
EmbeddedResource blob is stored in the session's JSONL transcript. This script
reads that transcript, finds all downloaded attachments, and saves them as PNG files.

Usage:
    python3 extract_images.py <slug> [session_id]

    slug        — used to determine the output directory: resources/images/<slug>/
    session_id  — optional; defaults to the most recent session in ~/.claude/projects/

Output: ~/.claude/skills/generate-sds/resources/images/<slug>/<original_filename>

Run this immediately after calling confluence_download_attachment for each image
you want to embed in the SDS.
"""

import sys
import json
import base64
import pathlib
import time
import re


SKILL_DIR   = pathlib.Path(__file__).parent.parent
PROJECTS_DIR = pathlib.Path.home() / '.claude' / 'projects' / '-Users-diya-sharma'


def find_latest_session(projects_dir: pathlib.Path) -> pathlib.Path:
    """Return the most recently modified JSONL session transcript."""
    jsonl_files = sorted(
        projects_dir.glob('*.jsonl'),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not jsonl_files:
        raise FileNotFoundError(f'No session transcripts found in {projects_dir}')
    return jsonl_files[0]


def extract_images_from_transcript(
    transcript_path: pathlib.Path,
    output_dir: pathlib.Path,
    since_mtime: float = None
) -> list[pathlib.Path]:
    """
    Parse the JSONL transcript and save all EmbeddedResource blobs that were
    returned by confluence_download_attachment tool calls.

    Returns list of saved file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []

    with open(transcript_path) as f:
        lines = f.readlines()

    for line in lines:
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Filter to recent entries if requested
        if since_mtime is not None:
            ts = msg.get('timestamp')
            if ts and _parse_ts(ts) < since_mtime:
                continue

        content = msg.get('message', {}).get('content', [])
        if not isinstance(content, list):
            continue

        for block in content:
            if not isinstance(block, dict) or block.get('type') != 'tool_result':
                continue

            # Find the filename from the text part of this tool result
            filename = None
            for part in block.get('content', []):
                if isinstance(part, dict) and part.get('type') == 'text':
                    text = part.get('text', '')
                    # Pattern: [Resource from atlassian at attachment:///attXXX/filename.png]
                    m = re.search(r'attachment:///\w+/(.+?\.(?:png|jpg|jpeg|gif|svg))', text, re.I)
                    if m:
                        filename = pathlib.Path(m.group(1)).name

            # Find the image blob
            for part in block.get('content', []):
                if not isinstance(part, dict) or part.get('type') != 'image':
                    continue
                b64 = part.get('source', {}).get('data', '')
                if not b64:
                    continue

                out_name = filename or f'confluence_image_{len(saved)}.png'
                out_path = output_dir / out_name
                out_path.write_bytes(base64.b64decode(b64))
                saved.append(out_path)
                print(f'  Saved: {out_path.name} ({out_path.stat().st_size:,} bytes)')

    return saved


def _parse_ts(ts_str: str) -> float:
    """Parse ISO timestamp to unix float, best-effort."""
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        return dt.timestamp()
    except Exception:
        return 0.0


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
    session_id = sys.argv[2] if len(sys.argv) > 2 else None

    output_dir = SKILL_DIR / 'resources' / 'images' / slug

    if session_id:
        transcript = PROJECTS_DIR / f'{session_id}.jsonl'
    else:
        transcript = find_latest_session(PROJECTS_DIR)

    print(f'Reading transcript: {transcript.name}')
    print(f'Output directory:   {output_dir}')
    print()

    saved = extract_images_from_transcript(transcript, output_dir)

    if saved:
        print(f'\n{len(saved)} image(s) extracted.')
        print('Reference in content JSON:')
        for p in saved:
            rel = f'~/.claude/skills/generate-sds/resources/images/{slug}/{p.name}'
            print(f'  {{"type": "image", "path": "{rel}", "caption": "...", "width": 5.5}}')
    else:
        print('No Confluence images found in transcript.')
        print('Call confluence_download_attachment() first, then re-run this script.')


if __name__ == '__main__':
    main()
