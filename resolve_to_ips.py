import socket
import os

# Input and output file names
INPUT_FILE = "AzureDomains.txt"
IP_OUTPUT_FILE = "AzureBlockListIPs.txt"
FQDN_OUTPUT_FILE = "Fortigate_URL_List.txt"

resolved_ips = set()
wildcard_domains = []
skipped_domains = []

def resolve_domain(domain):
    """Resolve a domain to IPs, return a list of IPs"""
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

    counter = 1
    for domain in domains:
        if "*" in domain:
            wildcard_domains.append(domain)
            continue
        ips = resolve_domain(domain)
        if ips:
            resolved_ips.update(ips)
        else:
            skipped_domains.append(domain)

    # Write IP feed
    with open(IP_OUTPUT_FILE, "w") as f:
        for ip in sorted(resolved_ips):
            f.write(ip + "\n")

    # Write wildcard FortiGate FQDN entries
    with open(FQDN_OUTPUT_FILE, "w") as f:
        for i, domain in enumerate(wildcard_domains, start=1):
            f.write(f'    edit "Azure_Domain_Wildcard_{i}"\n')
            f.write(f'        set type fqdn\n')
            f.write(f'        set fqdn "{domain}"\n')
            f.write(f'    next\n\n')

    # Summary
    print(f"✅ Resolved {len(resolved_ips)} unique IPs → {IP_OUTPUT_FILE}")
    print(f"✅ Created {len(wildcard_domains)} FortiGate FQDN entries → {FQDN_OUTPUT_FILE}")
    if skipped_domains:
        print(f"⚠️ Could not resolve {len(skipped_domains)} domains:")
        for d in skipped_domains:
            print(f"  - {d}")

if __name__ == "__main__":
    main()
