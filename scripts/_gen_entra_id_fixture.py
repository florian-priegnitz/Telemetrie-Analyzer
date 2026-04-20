"""One-shot Generator für Azure Entra ID Sign-In Logs Mock-Fixture (JSONL)."""

import json

# (time, upn, display, app, app_id, ip, ca_status, error_code, failure_reason)
ROWS = [
    ("2024-06-23T08:15:32.000Z", "alice@acme.onmicrosoft.com", "Alice",   "Microsoft 365 Copilot", "00000000-1111-1111-1111-000000000001", "203.0.113.42",  "success",    0,     "None"),
    ("2024-06-23T08:16:02.100Z", "bob@acme.onmicrosoft.com",   "Bob",     "ChatGPT Enterprise",    "00000000-1111-1111-1111-000000000002", "203.0.113.50",  "success",    0,     "None"),
    ("2024-06-23T08:16:44.250Z", "bob@acme.onmicrosoft.com",   "Bob",     "Claude Enterprise",     "00000000-1111-1111-1111-000000000003", "203.0.113.50",  "success",    0,     "None"),
    ("2024-06-23T08:17:11.000Z", "carol@acme.onmicrosoft.com", "Carol",   "Notion AI",             "00000000-1111-1111-1111-000000000004", "203.0.113.33",  "success",    0,     "None"),
    ("2024-06-23T08:18:05.500Z", "dave@acme.onmicrosoft.com",  "Dave",    "GitHub Copilot",        "00000000-1111-1111-1111-000000000005", "203.0.113.44",  "success",    0,     "None"),
    ("2024-06-23T08:19:13.000Z", "eve@acme.onmicrosoft.com",   "Eve",     "Perplexity AI",         "00000000-1111-1111-1111-000000000006", "203.0.113.66",  "failure",    53003, "Access blocked by Conditional Access"),
    ("2024-06-23T08:20:17.800Z", "alice@acme.onmicrosoft.com", "Alice",   "Microsoft 365 Copilot", "00000000-1111-1111-1111-000000000001", "203.0.113.42",  "success",    0,     "None"),
    ("2024-06-23T08:21:03.100Z", "frank@acme.onmicrosoft.com", "Frank",   "Hugging Face",          "00000000-1111-1111-1111-000000000007", "203.0.113.77",  "success",    0,     "None"),
    ("2024-06-23T08:22:41.200Z", "grace@acme.onmicrosoft.com", "Grace",   "OpenAI Platform",       "00000000-1111-1111-1111-000000000008", "203.0.113.88",  "success",    0,     "None"),
    ("2024-06-23T08:23:00.400Z", "heidi@acme.onmicrosoft.com", "Heidi",   "Anthropic Console",     "00000000-1111-1111-1111-000000000009", "203.0.113.99",  "notApplied", 0,     "None"),
    ("2024-06-23T08:25:18.300Z", "bob@acme.onmicrosoft.com",   "Bob",     "ChatGPT Enterprise",    "00000000-1111-1111-1111-000000000002", "",              "success",    0,     "None"),  # leere IP → UserId-Fallback
    ("2024-06-23T08:26:29.000Z", "ivan@acme.onmicrosoft.com",  "Ivan",    "Mistral Le Chat",       "00000000-1111-1111-1111-00000000000a", "203.0.113.110", "success",    0,     "None"),
    ("2024-06-23T08:27:55.550Z", "judy@acme.onmicrosoft.com",  "Judy",    "Gemini for Workspace",  "00000000-1111-1111-1111-00000000000b", "203.0.113.121", "success",    0,     "None"),
    ("2024-06-23T08:29:02.000Z", "mallory@acme.onmicrosoft.com","Mallory","ChatGPT Enterprise",    "00000000-1111-1111-1111-000000000002", "203.0.113.132", "success",    50126, "Invalid password"),  # bad creds
    ("2024-06-23T08:30:11.600Z", "niaj@acme.onmicrosoft.com",  "Niaj",    "Microsoft 365 Copilot", "00000000-1111-1111-1111-000000000001", "203.0.113.143", "failure",    53003, "Access blocked"),
    ("2024-06-23T08:31:48.150Z", "olivia@acme.onmicrosoft.com","Olivia",  "Cohere",                "00000000-1111-1111-1111-00000000000c", "203.0.113.154", "success",    0,     "None"),
    ("2024-06-23T08:33:27.000Z", "peggy@acme.onmicrosoft.com", "Peggy",   "Replicate",             "00000000-1111-1111-1111-00000000000d", "203.0.113.165", "success",    0,     "None"),
    ("2024-06-23T08:34:15.250Z", "trent@acme.onmicrosoft.com", "Trent",   "OpenAI Platform",       "00000000-1111-1111-1111-000000000008", "203.0.113.176", "success",    500121, "MFA failure"),
    ("2024-06-23T08:40:11.000Z", "ursula@acme.onmicrosoft.com","Ursula",  "Claude Enterprise",     "00000000-1111-1111-1111-000000000003", "203.0.113.187", "success",    0,     "None"),
    ("2024-06-23T08:41:44.100Z", "victor@acme.onmicrosoft.com","Victor",  "DeepSeek",              "00000000-1111-1111-1111-00000000000e", "2001:db8::1",   "success",    0,     "None"),  # IPv6
]


def build_event(i, row):
    ts, upn, display, app, app_id, ip, ca_status, error_code, failure_reason = row
    # Eindeutige UserIds per Index
    user_id = f"{i:08x}-aaaa-bbbb-cccc-{i:012x}"
    event = {
        "TimeGenerated": ts,
        "CreatedDateTime": ts,
        "UserPrincipalName": upn,
        "UserId": user_id,
        "UserDisplayName": display,
        "AppDisplayName": app,
        "AppId": app_id,
        "IPAddress": ip,
        "Location": "DE",
        "LocationDetails": {"city": "Berlin", "countryOrRegion": "DE"},
        "Status": {
            "errorCode": error_code,
            "failureReason": failure_reason,
            "additionalDetails": "MFA completed" if error_code == 0 else "",
        },
        "ConditionalAccessStatus": ca_status,
        "DeviceDetail": {"operatingSystem": "Windows", "browser": "Chrome"},
        "ClientAppUsed": "Browser",
        "AuthenticationProtocol": "oAuth2",
        "ResourceDisplayName": app,
        "CorrelationId": f"corr-{i:08x}",
    }
    return event


def main():
    with open("testdata/entra_signin_sample.log", "w", encoding="utf-8") as f:
        for i, row in enumerate(ROWS, 1):
            event = build_event(i, row)
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f"Wrote {len(ROWS)} JSONL events to testdata/entra_signin_sample.log")


if __name__ == "__main__":
    main()
