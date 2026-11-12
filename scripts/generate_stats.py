#!/usr/bin/env python3
"""Generate a compact dark SVG card using public GitHub profile/repository data."""
import json
import os
import urllib.request
from collections import Counter
from xml.sax.saxutils import escape

USER = os.environ.get("GITHUB_USER", "AnkitaMahajan1")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_json(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "github-profile-readme-generator"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

user = get_json(f"https://api.github.com/users/{USER}")
repos = get_json(f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated&type=owner")
repos = [r for r in repos if not r.get("fork", False)]
stars = sum(r.get("stargazers_count", 0) for r in repos)
forks = sum(r.get("forks_count", 0) for r in repos)
languages = Counter(r.get("language") for r in repos if r.get("language"))
top = languages.most_common(4)
max_count = max([n for _, n in top], default=1)

stats = [("PUBLIC REPOS", str(user.get("public_repos", 0))),
         ("FOLLOWERS", str(user.get("followers", 0))),
         ("STARS EARNED", str(stars)), ("FORKS", str(forks))]
stat_svg = []
for i, (label, value) in enumerate(stats):
    x, y = 38 + (i % 2) * 510, 86 + (i // 2) * 83
    stat_svg.append(f'<g transform="translate({x} {y})"><text fill="#94A3B8" font-size="12" letter-spacing="1.5">{label}</text><text y="39" fill="#F8FAFC" font-size="29" font-weight="700">{escape(value)}</text></g>')

bars = []
for i, (name, count) in enumerate(top):
    y, width = 93 + i * 34, int(250 * count / max_count)
    bars.append(f'<text x="590" y="{y}" fill="#CBD5E1" font-size="13">{escape(name)}</text><rect x="730" y="{y-12}" width="250" height="9" rx="4.5" fill="#263449"/><rect x="730" y="{y-12}" width="{width}" height="9" rx="4.5" fill="url(#grad)"/>')

language_content = ''.join(bars) if bars else '<text x="590" y="100" fill="#94A3B8" font-size="13">Language data will appear as repositories are added.</text>'
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="270" viewBox="0 0 1050 270" role="img" aria-labelledby="title desc">
<title id="title">{escape(USER)} GitHub statistics</title><desc id="desc">Public repositories, followers, stars, forks and most common repository languages.</desc>
<defs><linearGradient id="grad" x1="0" x2="1"><stop stop-color="#A78BFA"/><stop offset="1" stop-color="#22D3EE"/></linearGradient></defs>
<rect width="1050" height="270" rx="20" fill="#0D1424" stroke="#263449"/>
<text x="38" y="42" fill="#F8FAFC" font-size="19" font-family="Arial,sans-serif" font-weight="700">GitHub snapshot</text><text x="1010" y="42" text-anchor="end" fill="#64748B" font-size="11" font-family="monospace">AUTO-UPDATED</text>
{''.join(stat_svg)}<path d="M550 65V235" stroke="#263449"/><text x="590" y="62" fill="#F8FAFC" font-size="15" font-weight="700">Top repository languages</text>
{language_content}
<text x="38" y="249" fill="#64748B" font-size="10">Data from the GitHub public REST API · Excludes forked repositories from star/language totals</text></svg>"""

os.makedirs("dist", exist_ok=True)
with open("dist/stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"Generated stats for {USER}: {len(repos)} non-fork repositories")
