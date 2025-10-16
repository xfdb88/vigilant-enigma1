from igscraper.parser import parse_profile

def test_parse_profile_minimal():
    html = "<html><head><meta property='og:title' content='Alice • Instagram photos and videos'></head><body><h1>Alice</h1><p>Contact: alice@example.com</p></body></html>"
    row, _ = parse_profile(html, "alice")
    assert row["username"] == "alice"
    assert row["display_name"] in ("Alice", "Alice • Instagram photos and videos".split("•")[0].strip())
    assert "alice@example.com" in (row.get("bio") or "") or row.get("email") == "alice@example.com"
