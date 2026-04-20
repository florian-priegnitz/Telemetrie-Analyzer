"""One-shot fixture generator for PAN-OS URL-Filtering mock logs.

Wird einmal ausgeführt, um `testdata/paloalto_sample.log` zu erzeugen.
Nicht Teil des Produktiv-Codes — steht hier zur Nachvollziehbarkeit/Reproduzier-
barkeit der Testdaten.
"""

ROWS = [
    ("08:15:32", "10.0.1.42", "54321", "alice@acme.corp", "ssl", "alert", "chat.openai.com/backend-api/conversation", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:15:45", "10.0.1.42", "54322", "alice@acme.corp", "ssl", "alert", "chat.openai.com/", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:16:02", "10.0.1.50", "41233", "bob@acme.corp", "ssl", "alert", "claude.ai/chats", "Computers-and-Internet", "Mozilla/5.0 Firefox/125"),
    ("08:16:44", "10.0.1.50", "41234", "bob@acme.corp", "ssl", "alert", "api.anthropic.com/v1/messages", "Computers-and-Internet", "anthropic-sdk-python/0.30"),
    ("08:17:11", "10.0.1.33", "39110", "", "ssl", "alert", "copilot.microsoft.com/", "Computers-and-Internet", "Mozilla/5.0 Edge/125"),
    ("08:18:05", "10.0.1.44", "55001", "carol@acme.corp", "ssl", "alert", "gemini.google.com/app", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:18:22", "10.0.1.55", "55002", "dave@acme.corp", "ssl", "alert", "huggingface.co/models/gpt2", "Computers-and-Internet", "Mozilla/5.0 Firefox/125"),
    ("08:19:13", "10.0.1.66", "55003", "eve@acme.corp", "ssl", "block-url", "character.ai/chat/abc", "Unknown", "Mozilla/5.0 Chrome/124"),
    ("08:20:17", "10.0.1.42", "54330", "alice@acme.corp", "ssl", "alert", "chat.openai.com/api/auth/session", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:22:41", "10.0.1.77", "40210", "", "ssl", "alert", "perplexity.ai/search", "Computers-and-Internet", "Mozilla/5.0 Safari/17"),
    ("08:23:00", "10.0.1.88", "40211", "frank@acme.corp", "ssl", "alert", "replicate.com/account/api-tokens", "Developer-Tools", "Mozilla/5.0 Chrome/124"),
    ("08:25:18", "10.0.1.99", "40212", "grace@acme.corp", "ssl", "alert", "api.openai.com/v1/chat/completions", "Computers-and-Internet", "openai-python/1.35"),
    ("08:26:29", "10.0.2.10", "40213", "heidi@acme.corp", "ssl", "alert", "api.mistral.ai/v1/chat/completions", "Computers-and-Internet", "curl/8.4"),
    ("08:27:55", "10.0.1.50", "41240", "bob@acme.corp", "ssl", "alert", "claude.ai/api/organizations/123/chats", "Computers-and-Internet", "Mozilla/5.0 Firefox/125"),
    ("08:29:02", "10.0.2.21", "40214", "ivan@acme.corp", "ssl", "alert", "cohere.ai/chat", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:30:11", "10.0.2.32", "40215", "", "ssl", "block-url", "poe.com/", "Unknown", "Mozilla/5.0 Chrome/124"),
    ("08:31:48", "10.0.1.42", "54340", "alice@acme.corp", "ssl", "alert", "chat.openai.com/g/g-BhDPQhWuS/mentor", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:33:27", "10.0.2.43", "40216", "judy@acme.corp", "ssl", "alert", "you.com/search", "Computers-and-Internet", "Mozilla/5.0 Chrome/124"),
    ("08:34:15", "10.0.2.54", "40217", "mallory@acme.corp", "ssl", "block-url", "openrouter.ai/api/v1/chat/completions", "Developer-Tools", "openrouter/1.0"),
    ("08:40:11", "10.0.1.50", "41250", "bob@acme.corp", "ssl", "alert", "api.anthropic.com/v1/complete", "Computers-and-Internet", "anthropic-sdk-python/0.30"),
]

N_FIELDS = 45


def _base_record():
    return [""] * N_FIELDS


def _fill_url_record(i, time, ip, sp, user, proto, action, url, cat, ua):
    fields = _base_record()
    fields[0] = "1"
    fields[1] = f"2024/06/23 {time}"
    fields[2] = "012345000001"
    fields[3] = "THREAT"
    fields[4] = "url"
    fields[5] = "0"
    fields[6] = f"2024/06/23 {time}"
    fields[7] = ip
    fields[8] = f"203.0.113.{i}"
    fields[9] = "0.0.0.0"
    fields[10] = "0.0.0.0"
    fields[11] = "allow-ai"
    fields[12] = user
    fields[14] = "web-browsing"
    fields[15] = "vsys1"
    fields[16] = "trust"
    fields[17] = "untrust"
    fields[18] = "ethernet1/1"
    fields[19] = "ethernet1/2"
    fields[20] = "0"
    fields[22] = f"1234567{i}"
    fields[23] = "1"
    fields[24] = sp
    fields[25] = "443"
    fields[26] = "0"
    fields[27] = "0"
    fields[28] = "0x00"
    fields[29] = proto
    fields[30] = action
    fields[31] = url
    fields[33] = cat
    fields[34] = "informational"
    fields[35] = "client-to-server"
    fields[36] = f"{i}0123"
    fields[37] = "0x00"
    fields[38] = "DE"
    fields[39] = "US"
    fields[44] = ua
    return fields


def main():
    lines = []
    for i, args in enumerate(ROWS, 1):
        fields = _fill_url_record(i, *args)
        lines.append(",".join(fields))

    # virus subtype (should be skipped by parser)
    virus = _fill_url_record(
        99, "08:45:00", "10.0.1.42", "55555", "alice@acme.corp",
        "tcp", "block-url", "evil.example/payload.exe", "malware", "Mozilla/5.0",
    )
    virus[4] = "virus"  # subtype override
    lines.append(",".join(virus))

    # Syslog prefix (valid URL line, prefixed)
    prefix = _fill_url_record(
        77, "08:50:00", "10.0.1.77", "55077", "niaj@acme.corp",
        "ssl", "alert", "gemini.google.com/app/chat", "Computers-and-Internet", "Mozilla/5.0 Chrome/124",
    )
    lines.append("<14>Jun 23 08:50:00 PA-FW-01 " + ",".join(prefix))

    with open("testdata/paloalto_sample.log", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} lines")


if __name__ == "__main__":
    main()
