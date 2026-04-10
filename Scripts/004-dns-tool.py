import socket
import dns.resolver
import argparse


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DNS Lookup Tool - Query DNS records for a domain"
    )
    parser.add_argument("domain", help="Domain name to look up")
    parser.add_argument(
        "-t", "--types",
        nargs="+",
        default=["A", "AAAA", "MX", "NS", "TXT", "CNAME"],
        help="Record types to query (default: A AAAA MX NS TXT CNAME)"
    )
    return parser.parse_args()


def basic_lookup(domain):
    """Perform a basic forward DNS lookup using socket."""
    results = {"ipv4": [], "ipv6": []}

    try:
        addr_info = socket.getaddrinfo(domain, None)
        for entry in addr_info:
            family, _, _, _, sockaddr = entry
            ip = sockaddr[0]
            if family == socket.AF_INET and ip not in results["ipv4"]:
                results["ipv4"].append(ip)
            elif family == socket.AF_INET6 and ip not in results["ipv6"]:
                results["ipv6"].append(ip)
    except socket.gaierror as e:
        results["error"] = str(e)

    return results


def query_records(domain, record_types):
    """Query specific DNS record types using dnspython."""
    results = {}

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records = []
            for rdata in answers:
                records.append(str(rdata))
            results[rtype] = {
                "records": records,
                "ttl": answers.rrset.ttl
            }
        except dns.resolver.NoAnswer:
            results[rtype] = {"records": [], "note": "No records found"}
        except dns.resolver.NXDOMAIN:
            results[rtype] = {"records": [], "note": "Domain does not exist"}
            break
        except dns.resolver.NoNameservers:
            results[rtype] = {"records": [], "note": "No nameservers available"}
        except dns.exception.DNSException as e:
            results[rtype] = {"records": [], "note": str(e)}

    return results


def reverse_lookup(ip):
    """Perform a reverse DNS lookup on an IP address."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return None


def display_results(domain, basic, records):
    """Display all DNS lookup results."""
    print("=" * 55)
    print(f"  DNS LOOKUP: {domain}")
    print("=" * 55)

    print(f"\n  Basic Resolution (via OS resolver)")
    print("-" * 45)
    if "error" in basic:
        print(f"  Error: {basic['error']}")
    else:
        for ip in basic.get("ipv4", []):
            rev = reverse_lookup(ip)
            rev_str = f" -> {rev}" if rev else ""
            print(f"  IPv4: {ip}{rev_str}")
        for ip in basic.get("ipv6", []):
            print(f"  IPv6: {ip}")

    print(f"\n  Detailed Records")
    print("-" * 45)
    for rtype, data in records.items():
        if data["records"]:
            print(f"\n  [{rtype}] (TTL: {data['ttl']}s)")
            for record in data["records"]:
                print(f"    {record}")
        else:
            note = data.get("note", "No records")
            print(f"\n  [{rtype}] {note}")


if __name__ == "__main__":
    args = parse_args()
    basic = basic_lookup(args.domain)
    records = query_records(args.domain, args.types)
    display_results(args.domain, basic, records)