"""One-shot Generator für Cloudflare Gateway NDJSON-Fixture (DNS + HTTP gemischt)."""

import json

# DNS-Events (12)
DNS_ROWS = [
    ("2024-06-23T08:15:32Z", "alice@acme.com",   "10.0.1.42", "chat.openai.com",       "A",    ["Generative AI"],                "allowed"),
    ("2024-06-23T08:15:33Z", "alice@acme.com",   "10.0.1.42", "chat.openai.com",       "AAAA", ["Generative AI"],                "allowed"),
    ("2024-06-23T08:16:02Z", "bob@acme.com",     "10.0.1.50", "claude.ai",             "A",    ["Generative AI"],                "allowed"),
    ("2024-06-23T08:16:44Z", "bob@acme.com",     "10.0.1.50", "api.anthropic.com",     "A",    ["Generative AI", "Technology"],  "allowed"),
    ("2024-06-23T08:17:11Z", "",                 "10.0.1.33", "copilot.microsoft.com", "A",    ["Generative AI", "Productivity"],"allowed"),
    ("2024-06-23T08:18:05Z", "carol@acme.com",   "10.0.1.44", "gemini.google.com",     "A",    ["Generative AI"],                "allowed"),
    ("2024-06-23T08:19:13Z", "eve@acme.com",     "10.0.1.66", "character.ai",          "A",    ["Generative AI", "Unrated"],     "blocked"),
    ("2024-06-23T08:22:41Z", "",                 "10.0.1.77", "perplexity.ai",         "A",    ["Generative AI"],                "allowed"),
    ("2024-06-23T08:25:18Z", "grace@acme.com",   "10.0.1.99", "api.openai.com",        "A",    ["Generative AI"],                "allowed"),
    ("2024-06-23T08:30:11Z", "",                 "10.0.2.32", "poe.com",               "A",    ["Generative AI", "Unrated"],     "blocked"),
    ("2024-06-23T08:33:27Z", "judy@acme.com",    "10.0.2.43", "you.com",               "A",    ["Generative AI", "Search"],      "allowed"),
    ("2024-06-23T08:34:15Z", "mallory@acme.com", "10.0.2.54", "openrouter.ai",         "A",    ["Generative AI"],                "blocked"),
]

# HTTP-Events (10)
HTTP_ROWS = [
    ("2024-06-23T08:15:35Z", "alice@acme.com",   "10.0.1.42", "https://chat.openai.com/backend-api/conversation", "POST", 200, 2048,  10240, ["Generative AI"],      "allow",   "Mozilla/5.0 Chrome/124"),
    ("2024-06-23T08:16:07Z", "bob@acme.com",     "10.0.1.50", "https://claude.ai/chats",                          "GET",  200, 512,   4096,  ["Generative AI"],      "allow",   "Mozilla/5.0 Firefox/125"),
    ("2024-06-23T08:16:48Z", "bob@acme.com",     "10.0.1.50", "https://api.anthropic.com/v1/messages",            "POST", 200, 2560,  8192,  ["Generative AI"],      "allow",   "anthropic-sdk-python/0.30"),
    ("2024-06-23T08:19:20Z", "eve@acme.com",     "10.0.1.66", "https://character.ai/chat/abc",                    "GET",  403, 256,   128,   ["Generative AI"],      "block",   "Mozilla/5.0 Chrome/124"),
    ("2024-06-23T08:25:25Z", "grace@acme.com",   "10.0.1.99", "https://api.openai.com/v1/chat/completions",       "POST", 200, 890512,2048,  ["Generative AI"],      "allow",   "openai-python/1.35"),
    ("2024-06-23T08:31:55Z", "alice@acme.com",   "10.0.1.42", "https://chat.openai.com/g/g-BhDPQhWuS/mentor",     "GET",  200, 612,   9216,  ["Generative AI"],      "allow",   "Mozilla/5.0 Chrome/124"),
    ("2024-06-23T08:34:20Z", "mallory@acme.com", "10.0.2.54", "https://openrouter.ai/api/v1/chat/completions",    "POST", 403, 2048,  0,     ["Generative AI"],      "block",   "openrouter/1.0"),
    ("2024-06-23T08:37:09Z", "niaj@acme.com",    "10.0.2.65", "https://gemini.google.com/app/chat",               "GET",  200, 410,   5120,  ["Generative AI"],      "allow",   "Mozilla/5.0 Chrome/124"),
    ("2024-06-23T08:40:11Z", "bob@acme.com",     "10.0.1.50", "https://api.anthropic.com/v1/complete",            "POST", 200, 12480, 0,     ["Generative AI"],      "allow",   "anthropic-sdk-python/0.30"),
    ("2024-06-23T08:45:00Z", "trent@acme.com",   "10.0.2.87", "https://huggingface.co/models/gpt2",               "GET",  200, 600,   10240, ["Generative AI", "Dev"],"isolate","Mozilla/5.0 Chrome/124"),
]


def main():
    events = []
    for i, row in enumerate(DNS_ROWS, 1):
        ts, email, src, qname, qtype, cats, decision = row
        events.append({
            "Datetime": ts,
            "Email": email,
            "DeviceID": f"dev-{i:03d}",
            "DeviceName": f"laptop-{i:03d}",
            "SrcIP": src,
            "QueryName": qname,
            "QueryType": qtype,
            "QueryCategoryNames": cats,
            "ResolverDecision": decision,
            "PolicyName": "ai-filter",
            "Location": "DE",
            "RCode": "NOERROR" if decision == "allowed" else "NXDOMAIN",
        })
    for i, row in enumerate(HTTP_ROWS, 1):
        ts, email, src, url, method, status, upload, download, cats, action, ua = row
        events.append({
            "Datetime": ts,
            "Email": email,
            "DeviceID": f"dev-{i+100:03d}",
            "SrcIP": src,
            "DestinationIP": "203.0.113.42",
            "DestinationPort": 443,
            "URL": url,
            "HTTPMethod": method,
            "HTTPStatusCode": status,
            "UploadBytes": upload,
            "DownloadBytes": download,
            "CategoryNames": cats,
            "Action": action,
            "UserAgent": ua,
            "PolicyName": "ai-http-filter",
        })
    with open("testdata/cloudflare_gateway_sample.log", "w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"Wrote {len(DNS_ROWS)} DNS + {len(HTTP_ROWS)} HTTP = {len(events)} NDJSON events")


if __name__ == "__main__":
    main()
