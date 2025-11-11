# generate_fortigate_objects.py

def is_ip_or_subnet(value: str) -> bool:
    """Determine if the string looks like an IP address or subnet (IPv4 or IPv6)."""
    import ipaddress
    try:
        ipaddress.ip_network(value, strict=False)
        return True
    except ValueError:
        return False


def main():
    input_file = "input.txt"
    output_file = "fortigate_output.txt"

    # Ask user for base name (X)
    base_name = input("Enter base name for Fortigate objects (e.g., Microsoft): ").strip()

    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    url_counter = 1
    ip_counter = 1
    output_lines = []

    for line in lines:
        if is_ip_or_subnet(line):
            # IP or subnet
            entry_name = f'{base_name}_IP_{ip_counter}'
            output_lines.append(f'edit "{entry_name}"')
            output_lines.append(f'    set subnet {line}')
            output_lines.append(f'next\n')
            ip_counter += 1
        else:
            # FQDN / URL
            entry_name = f'{base_name}_URL_{url_counter}'
            output_lines.append(f'edit "{entry_name}"')
            output_lines.append(f'    set type fqdn')
            output_lines.append(f'    set fqdn "{line}"')
            output_lines.append(f'next\n')
            url_counter += 1

    # Write results
    with open(output_file, "w") as f:
        f.write("\n".join(output_lines))

    print(f"✅ Fortigate configuration written to '{output_file}'")
    print(f"→ {url_counter - 1} FQDNs and {ip_counter - 1} IPs processed.")


if __name__ == "__main__":
    main()
