import socket
import os

# Input and output file paths (assumes same directory)
INPUT_FILE = "AzureDomains.txt"
OUTPUT_FILE = "AzureBlockListIPs.txt"

resolved_ips = set()
skipped_domains = []

def resolve_domain(domain):
    """Try to resolve a domain name to all IPs"""
    try:
        infos = socket.getaddrinfo(domain, None)
        return [info[4][0] for info in infos]
    except socket.gaierror:
        return []

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    for domain in domains:
        if domain.startswith("*.") or "*" in domain:
            skipped_domains.append(domain)
            continue
        ips = resolve_domain(domain)
        if ips:
            resolved_ips.update(ips)
        else:
            print(f"⚠️ Could not resolve: {domain}")

    # Write IPs to file (overwrite)
    with open(OUTPUT_FILE, "w") as f:
        for ip in sorted(resolved_ips):
            f.write(ip + "\n")

    print(f"✅ Resolved {len(resolved_ips)} unique IPs.")
    if skipped_domains:
        print(f"⚠️ Skipped {len(skipped_domains)} wildcard domains:")
        for d in skipped_domains:
            print(f"  - {d}")

if __name__ == "__main__":
    main()
