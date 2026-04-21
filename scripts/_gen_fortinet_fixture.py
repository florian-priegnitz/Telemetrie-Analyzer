"""One-shot Generator für FortiGate webfilter.log Mock-Fixture."""

# (date_HHMMSS, srcip, user, hostname, url, action, catdesc, service, method, sent, rcvd, eventtype)
ROWS = [
    ("08:15:32", "10.0.1.42", "alice@acme.corp",    "chat.openai.com",      "/backend-api/conversation", "passthrough", "Business Services", "HTTPS", "get",    1024,  8192,  "ftgd_allow"),
    ("08:15:40", "10.0.1.42", "alice@acme.corp",    "chat.openai.com",      "/",                         "passthrough", "Business Services", "HTTPS", "domain", 412,   2048,  "ftgd_allow"),
    ("08:16:02", "10.0.1.50", "bob@acme.corp",      "claude.ai",            "/chats",                    "passthrough", "Business Services", "HTTPS", "get",    520,   4096,  "ftgd_allow"),
    ("08:16:44", "10.0.1.50", "bob@acme.corp",      "api.anthropic.com",    "/v1/messages",              "passthrough", "Business Services", "HTTPS", "post",   2560,  8192,  "ftgd_allow"),
    ("08:17:11", "10.0.1.33", "",                   "copilot.microsoft.com","/",                         "passthrough", "Business Services", "HTTPS", "domain", 220,   1024,  "ftgd_allow"),
    ("08:18:05", "10.0.1.44", "carol@acme.corp",    "gemini.google.com",    "/app/chat",                 "passthrough", "Business Services", "HTTPS", "get",    410,   5120,  "ftgd_allow"),
    ("08:18:22", "10.0.1.55", "dave@acme.corp",     "huggingface.co",       "/models/gpt2",              "passthrough", "Software/Technology","HTTPS", "get",    600,   10240, "ftgd_allow"),
    ("08:19:13", "10.0.1.66", "ACME\\eve",          "character.ai",         "/chat/abc",                 "blocked",     "Unrated",           "HTTPS", "domain", 256,   0,     "ftgd_blk"),
    ("08:20:17", "10.0.1.42", "alice@acme.corp",    "chat.openai.com",      "/api/auth/session",         "passthrough", "Business Services", "HTTPS", "get",    128,   512,   "ftgd_allow"),
    ("08:22:41", "10.0.1.77", "",                   "perplexity.ai",        "/search?q=secret",          "passthrough", "Business Services", "HTTPS", "get",    340,   3072,  "ftgd_allow"),
    ("08:23:00", "10.0.1.88", "frank@acme.corp",    "replicate.com",        "/account/api-tokens",       "passthrough", "Developer-Tools",   "HTTPS", "get",    412,   1536,  "ftgd_allow"),
    ("08:25:18", "10.0.1.99", "grace@acme.corp",    "api.openai.com",       "/v1/chat/completions",      "passthrough", "Business Services", "HTTPS", "post",   890512,2048,  "ftgd_allow"),
    ("08:26:29", "10.0.2.10", "heidi@acme.corp",    "api.mistral.ai",       "/v1/chat/completions",      "passthrough", "Business Services", "HTTPS", "post",   3140,  7168,  "ftgd_allow"),
    ("08:27:55", "10.0.1.50", "bob@acme.corp",      "claude.ai",            "/api/organizations/123/chat","passthrough","Business Services", "HTTPS", "post",   5210,  12288, "ftgd_allow"),
    ("08:29:02", "10.0.2.21", "ACME\\ivan",         "cohere.ai",            "/chat",                     "passthrough", "Business Services", "HTTPS", "get",    280,   3584,  "ftgd_allow"),
    ("08:30:11", "10.0.2.32", "",                   "poe.com",              "/",                         "blocked",     "Unrated",           "HTTPS", "domain", 198,   0,     "ftgd_blk"),
    ("08:31:48", "10.0.1.42", "alice@acme.corp",    "chat.openai.com",      "/g/g-BhDPQhWuS/mentor",     "passthrough", "Business Services", "HTTPS", "get",    612,   9216,  "ftgd_allow"),
    ("08:33:27", "10.0.2.43", "judy@acme.corp",     "you.com",              "/search",                   "passthrough", "Search Engines",    "HTTPS", "get",    340,   4096,  "ftgd_allow"),
    ("08:34:15", "10.0.2.54", "mallory@acme.corp",  "openrouter.ai",        "/api/v1/chat/completions",  "blocked",     "Unrated",           "HTTPS", "post",   2048,  0,     "ftgd_blk"),
    ("08:40:11", "10.0.1.50", "bob@acme.corp",      "api.anthropic.com",    "/v1/complete",              "passthrough", "Business Services", "HTTPS", "post",   12480, 0,     "ftgd_allow"),
    ("08:41:44", "10.0.1.42", "alice@acme.corp",    "platform.openai.com",  "/api-keys",                 "passthrough", "Developer-Tools",   "HTTPS", "get",    280,   3072,  "ftgd_allow"),
    ("08:45:00", "10.0.2.60", "ACME\\trent",        "bard.google.com",      "/",                         "passthrough", "Business Services", "HTTPS", "domain", 410,   5120,  "ftgd_allow"),
]


def _format_row(date_str, time_str, eventtime_ns, srcip, user, hostname, url, action, catdesc, service, method, sent, rcvd, eventtype, policy_id, session_id):
    fields = [
        f'date={date_str}',
        f'time={time_str}',
        'logid="0316013056"',
        'type="utm"',
        'subtype="webfilter"',
        f'eventtype="{eventtype}"',
        f'level="{"warning" if eventtype == "ftgd_blk" else "notice"}"',
        'vd="root"',
        f'eventtime={eventtime_ns}',
        f'policyid={policy_id}',
        f'sessionid={session_id}',
    ]
    if user:
        fields.append(f'user="{user}"')
    fields += [
        f'srcip={srcip}',
        'srcport=54321',
        'srcintf="port1"',
        'dstip=203.0.113.50',
        'dstport=443',
        'dstintf="port2"',
        'proto=6',
        f'service="{service}"',
        f'hostname="{hostname}"',
        'profile="default"',
        f'action="{action}"',
        'reqtype="direct"',
        f'url="{url}"',
        f'sentbyte={sent}',
        f'rcvdbyte={rcvd}',
        'direction="outgoing"',
        'msg="Web filter event"',
        f'method="{method}"',
        'cat=52',
        f'catdesc="{catdesc}"',
    ]
    return " ".join(fields)


def main():
    lines = []
    date_str = "2024-06-23"
    for i, row in enumerate(ROWS, 1):
        time_str = row[0]
        eventtime_ns = 1_719_131_732_000_000_000 + i * 1_000_000_000
        session_id = 12000 + i
        policy_id = 1 if row[5] == "passthrough" else 2
        lines.append(_format_row(
            date_str, time_str, eventtime_ns,
            row[1], row[2], row[3], row[4], row[5], row[6],
            row[7], row[8], row[9], row[10], row[11],
            policy_id, session_id,
        ))

    # + 1 non-webfilter subtype (ips) — muss übersprungen werden
    ips_line = 'date=2024-06-23 time=08:46:00 logid="0419016384" type="utm" subtype="ips" eventtype="signature" ' \
               'level="alert" vd="root" eventtime=1719131860000000000 policyid=1 sessionid=99999 user="alice" ' \
               'srcip=10.0.1.42 srcport=54321 srcintf="port1" dstip=203.0.113.99 dstport=443 dstintf="port2" ' \
               'proto=6 service="HTTPS" hostname="evil.example" profile="default" action="dropped" ' \
               'attack="SQL.Injection" severity="high" msg="IPS signature matched"'
    lines.append(ips_line)

    # + 1 Syslog-prefixed webfilter-Zeile
    prefix_line = "<190>" + _format_row(
        date_str, "08:50:00", 1_719_132_200_000_000_000,
        "10.0.2.77", "niaj@acme.corp", "gemini.google.com", "/app/chat",
        "passthrough", "Business Services", "HTTPS", "get", 410, 5120, "ftgd_allow",
        1, 30000,
    )
    lines.append(prefix_line)

    with open("testdata/fortinet_sample.log", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} lines to testdata/fortinet_sample.log")


if __name__ == "__main__":
    main()
