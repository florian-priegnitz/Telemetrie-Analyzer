"""One-shot Generator für AWS VPC Flow Logs Mock-Fixture.

Erzeugt zwei Dateien:
- testdata/aws_vpc_v2_sample.log   — v2 Default (14 Felder, kein Header)
- testdata/aws_vpc_v5_sample.log   — v5 Custom mit pkt-dst-aws-service (Header)
"""

# Fixture v2: klassisches Format, nur IPs — 22 Zeilen
V2_ROWS = [
    # (src_ip, dst_ip, src_port, dst_port, bytes, start_ts, end_ts, action, log_status)
    ("10.0.1.42",   "52.85.132.1",    51234, 443,  42810,  1719131732, 1719131792, "ACCEPT", "OK"),   # CloudFront
    ("10.0.1.42",   "52.85.132.1",    51234, 443,  128,    1719131793, 1719131853, "ACCEPT", "OK"),
    ("10.0.1.50",   "99.83.157.10",   52100, 443,  2560,   1719131802, 1719131862, "ACCEPT", "OK"),   # AWS IP-Range
    ("10.0.1.50",   "99.83.157.10",   52100, 443,  128000, 1719131863, 1719131923, "ACCEPT", "OK"),
    ("10.0.1.33",   "140.82.121.4",   40123, 443,  890,    1719131833, 1719131893, "ACCEPT", "OK"),   # GitHub
    ("10.0.1.44",   "52.85.132.1",    55001, 443,  3540,   1719131838, 1719131898, "ACCEPT", "OK"),
    ("10.0.1.55",   "8.8.8.8",        55002, 53,   84,     1719131842, 1719131902, "ACCEPT", "OK"),   # DNS
    ("10.0.1.66",   "104.26.14.205",  41235, 443,  512,    1719131851, 1719131911, "REJECT", "OK"),   # Cloudflare
    ("10.0.1.77",   "151.101.1.195",  41236, 443,  1820,   1719131871, 1719131931, "ACCEPT", "OK"),   # Fastly
    ("10.0.1.88",   "52.85.132.42",   41237, 443,  12800,  1719131890, 1719131950, "ACCEPT", "OK"),
    ("10.0.1.99",   "52.85.132.42",   41238, 443,  890512, 1719131908, 1719131968, "ACCEPT", "OK"),
    ("10.0.2.10",   "35.244.166.12",  41239, 443,  7168,   1719131929, 1719131989, "ACCEPT", "OK"),   # Cloud Run
    ("10.0.2.21",   "104.18.2.101",   41240, 443,  3072,   1719131950, 1719132010, "ACCEPT", "OK"),
    ("10.0.2.32",   "172.65.251.78",  41241, 443,  128,    1719131969, 1719132029, "REJECT", "OK"),
    ("10.0.1.42",   "52.85.132.1",    51235, 443,  612,    1719131988, 1719132048, "ACCEPT", "OK"),
    ("10.0.2.43",   "34.117.59.81",   41242, 443,  2560,   1719132009, 1719132069, "ACCEPT", "OK"),
    ("10.0.2.54",   "104.19.193.119", 41243, 443,  2048,   1719132030, 1719132090, "REJECT", "OK"),
    ("10.0.1.50",   "52.85.132.1",    51251, 443,  24080,  1719132062, 1719132122, "ACCEPT", "OK"),
    ("10.0.2.76",   "34.117.59.81",   41244, 443,  4608,   1719132082, 1719132142, "ACCEPT", "OK"),
    ("10.0.1.42",   "13.107.21.200",  51252, 443,  3072,   1719132105, 1719132165, "ACCEPT", "OK"),   # Microsoft
    ("10.0.3.5",    "216.58.214.78",  42001, 53,   92,     1719132122, 1719132182, "ACCEPT", "OK"),   # Google DNS
    ("10.0.3.10",   "104.26.15.205",  42002, 443,  2048,   1719132145, 1719132205, "ACCEPT", "OK"),
]

# v2: NODATA-Zeile (soll übersprungen werden)
V2_NODATA = ("-", "-", "-", "-", "-", 1719132200, 1719132260, "-", "NODATA")

# Fixture v5 Custom: mit pkt-src-aws-service + pkt-dst-aws-service — 12 Zeilen
# Header: version account-id interface-id srcaddr dstaddr srcport dstport protocol
#         packets bytes start end action log-status pkt-src-aws-service pkt-dst-aws-service
V5_ROWS = [
    # (src_ip, dst_ip, src_port, dst_port, bytes, start_ts, pkt_src_service, pkt_dst_service, action)
    ("10.0.1.42", "10.0.0.5",      51300, 443, 2560,  1719131732, "-",         "BEDROCK",     "ACCEPT"),
    ("10.0.1.42", "10.0.0.5",      51300, 443, 32768, 1719131793, "-",         "BEDROCK",     "ACCEPT"),
    ("10.0.1.50", "10.0.0.7",      52200, 443, 8192,  1719131832, "-",         "SAGEMAKER",   "ACCEPT"),
    ("10.0.1.50", "10.0.0.7",      52200, 443, 65536, 1719131893, "-",         "SAGEMAKER",   "ACCEPT"),
    ("10.0.1.33", "10.0.0.9",      52300, 443, 4096,  1719131923, "-",         "COMPREHEND",  "ACCEPT"),
    ("10.0.1.44", "10.0.0.11",     52400, 443, 512,   1719131953, "-",         "TEXTRACT",    "ACCEPT"),
    ("10.0.1.55", "10.0.0.13",     52500, 443, 2048,  1719131984, "-",         "REKOGNITION", "ACCEPT"),
    ("10.0.1.66", "10.0.0.15",     52600, 443, 8192,  1719132015, "-",         "POLLY",       "ACCEPT"),
    ("10.0.1.77", "10.0.0.17",     52700, 443, 512,   1719132046, "-",         "TRANSLATE",   "ACCEPT"),
    ("10.0.1.88", "10.0.0.19",     52800, 443, 1024,  1719132077, "-",         "LEX",         "ACCEPT"),
    ("10.0.1.99", "10.0.0.21",     52900, 443, 128,   1719132108, "-",         "BEDROCK",     "REJECT"),
    # Service-less flow (public internet) — domain fällt auf dstaddr zurück
    ("10.0.2.10", "52.85.132.1",   53000, 443, 4096,  1719132140, "-",         "-",           "ACCEPT"),
]


def build_v2():
    lines = []
    for row in V2_ROWS:
        fields = [
            "2", "123456789010", "eni-abc123def0456",
            row[0], row[1], str(row[2]), str(row[3]),
            "6",  # TCP
            "5", str(row[4]),
            str(row[5]), str(row[6]),
            row[7], row[8],
        ]
        lines.append(" ".join(fields))
    # NODATA-Line
    nd = V2_NODATA
    lines.append(" ".join([
        "2", "123456789010", "eni-abc123def0456",
        nd[0], nd[1], nd[2], nd[3], "-", "-", nd[4],
        str(nd[5]), str(nd[6]), nd[7], nd[8],
    ]))
    return "\n".join(lines) + "\n"


def build_v5():
    header = (
        "version account-id interface-id srcaddr dstaddr srcport dstport protocol "
        "packets bytes start end action log-status pkt-src-aws-service pkt-dst-aws-service"
    )
    lines = [header]
    for row in V5_ROWS:
        fields = [
            "5", "123456789010", "eni-abc123def0456",
            row[0], row[1], str(row[2]), str(row[3]),
            "6", "10", str(row[4]),
            str(row[5]), str(row[5] + 60),
            row[8], "OK",
            row[6], row[7],
        ]
        lines.append(" ".join(fields))
    return "\n".join(lines) + "\n"


def main():
    with open("testdata/aws_vpc_v2_sample.log", "w", encoding="utf-8") as f:
        f.write(build_v2())
    with open("testdata/aws_vpc_v5_sample.log", "w", encoding="utf-8") as f:
        f.write(build_v5())
    print("Wrote testdata/aws_vpc_v2_sample.log (22 + 1 NODATA)")
    print("Wrote testdata/aws_vpc_v5_sample.log (12 mit Header)")


if __name__ == "__main__":
    main()
