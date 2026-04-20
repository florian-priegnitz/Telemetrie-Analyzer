"""One-shot Generator für Netskope CASB NDJSON-Fixture (application events)."""

import json

BASE_EPOCH = 1_719_131_732  # 2024-06-23 08:35:32 UTC

# (offset_sec, user, src_ip, hostname, app, appcategory, activity, action, method, url_path, upload, download)
ROWS = [
    (0,    "alice@acme.com",   "10.0.1.42", "chat.openai.com",      "OpenAI ChatGPT",    "Artificial Intelligence", "Login",       "allow", "GET",  "/",                           128,   512),
    (10,   "alice@acme.com",   "10.0.1.42", "chat.openai.com",      "OpenAI ChatGPT",    "Artificial Intelligence", "Prompt",      "allow", "POST", "/backend-api/conversation",   2048,  10240),
    (35,   "alice@acme.com",   "10.0.1.42", "chat.openai.com",      "OpenAI ChatGPT",    "Artificial Intelligence", "Completion",  "allow", "POST", "/backend-api/conversation",   64,    5120),
    (90,   "bob@acme.com",     "10.0.1.50", "claude.ai",            "Anthropic Claude",  "Artificial Intelligence", "Login",       "allow", "GET",  "/chats",                       512,   4096),
    (120,  "bob@acme.com",     "10.0.1.50", "api.anthropic.com",    "Anthropic Claude",  "Artificial Intelligence", "Prompt",      "allow", "POST", "/v1/messages",                 2560,  8192),
    (245,  "",                 "10.0.1.33", "copilot.microsoft.com","Microsoft Copilot", "Artificial Intelligence", "Login",       "allow", "GET",  "/",                            220,   1024),
    (300,  "carol@acme.com",   "10.0.1.44", "gemini.google.com",    "Google Gemini",     "Artificial Intelligence", "Prompt",      "allow", "POST", "/app/chat",                    410,   5120),
    (360,  "dave@acme.com",    "10.0.1.55", "chat.openai.com",      "OpenAI ChatGPT",    "Artificial Intelligence", "Upload File", "allow", "POST", "/backend-api/files",           890512, 2048),
    (420,  "eve@acme.com",     "10.0.1.66", "character.ai",         "Character.ai",      "Artificial Intelligence", "Login",       "block", "GET",  "/chat/abc",                    256,   0),
    (540,  "",                 "10.0.1.77", "perplexity.ai",        "Perplexity AI",     "Artificial Intelligence", "Prompt",      "allow", "POST", "/search",                      340,   3072),
    (630,  "grace@acme.com",   "10.0.1.99", "api.openai.com",       "OpenAI ChatGPT",    "Artificial Intelligence", "Upload File", "alert", "POST", "/v1/files",                    10485760, 512),
    (780,  "heidi@acme.com",   "10.0.2.10", "api.mistral.ai",       "Mistral",           "Artificial Intelligence", "Prompt",      "allow", "POST", "/v1/chat/completions",         3140,  7168),
    (900,  "mallory@acme.com", "10.0.2.54", "openrouter.ai",        "OpenRouter",        "Artificial Intelligence", "Prompt",      "block", "POST", "/api/v1/chat/completions",     2048,  0),
    (1020, "trent@acme.com",   "10.0.2.87", "huggingface.co",       "Hugging Face",      "Artificial Intelligence", "Download",    "allow", "GET",  "/models/gpt2",                 600,   10240),
    (1200, "ursula@acme.com",  "10.0.2.98", "bard.google.com",      "Google Bard",       "Artificial Intelligence", "Login",       "allow", "GET",  "/",                            410,   5120),
    (1380, "victor@acme.com",  "10.0.3.10", "chat.deepseek.com",    "DeepSeek",          "Artificial Intelligence", "Prompt",      "allow", "POST", "/api/chat",                    1536,  8192),
    (1500, "alice@acme.com",   "10.0.1.42", "notion.so",            "Notion",            "Collaboration",           "Login",       "allow", "GET",  "/workspace",                   420,   6144),
    (1680, "peggy@acme.com",   "10.0.1.101","github.com",           "GitHub",            "Software Development",    "Login",       "allow", "GET",  "/",                            280,   3072),
]


def main():
    with open("testdata/netskope_sample.log", "w", encoding="utf-8") as f:
        for i, row in enumerate(ROWS, 1):
            offset, user, src_ip, hostname, app, appcat, activity, action, method, url_path, upload, download = row
            event = {
                "_insertion_epoch_timestamp": BASE_EPOCH + offset,
                "timestamp": BASE_EPOCH + offset,
                "user": user,
                "userkey": f"key-{i:03d}",
                "src_ip": src_ip,
                "src_country": "DE",
                "src_region": "Berlin",
                "app": app,
                "appcategory": appcat,
                "ccl": "high" if appcat == "Artificial Intelligence" else "medium",
                "cci": 72 if appcat == "Artificial Intelligence" else 55,
                "hostname": hostname,
                "domain": hostname,
                "url": f"https://{hostname}{url_path}",
                "uri_path": url_path,
                "method": method,
                "activity": activity,
                "action": action,
                "reason": "AI-Policy",
                "bytes_uploaded": upload,
                "bytes_downloaded": download,
                "useragent": "Mozilla/5.0 Chrome/124",
                "os": "Windows",
                "device": "Laptop",
                "policy": "AI-Monitoring-v1",
                "policy_id": f"pol-{i:03d}",
                "type": "application",
            }
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"Wrote {len(ROWS)} Netskope application events")


if __name__ == "__main__":
    main()
