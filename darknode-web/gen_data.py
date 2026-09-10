#!/usr/bin/env python3
"""
DarkNode OS — Massive Data & Config Generator
Generates ~154,000 lines of realistic cyberpunk/hacker-themed JSON data.
"""

import json
import os
import random
import hashlib
import string
import datetime

random.seed(0xDEADBEEF)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
CONFIG_DIR = os.path.join(BASE, "config")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)


def write_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    lines = sum(1 for _ in open(path))
    print(f"  {os.path.basename(path):30s} -> {lines:>7,} lines")


def rand_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def rand_mac():
    return ":".join(f"{random.randint(0,255):02x}" for _ in range(6))


def rand_hex(n):
    return "".join(random.choices("0123456789abcdef", k=n))


def rand_hash(algo="sha256"):
    data = rand_hex(64).encode()
    if algo == "md5":
        return hashlib.md5(data).hexdigest()
    if algo == "sha1":
        return hashlib.sha1(data).hexdigest()
    return hashlib.sha256(data).hexdigest()


def rand_ts(year=2026):
    m = random.randint(1, 9)
    d = random.randint(1, 28)
    h = random.randint(0, 23)
    mi = random.randint(0, 59)
    s = random.randint(0, 59)
    return f"{year}-{m:02d}-{d:02d}T{h:02d}:{mi:02d}:{s:02d}Z"


def rand_domain():
    words = ["shadow", "dark", "null", "void", "phantom", "spectre", "zero", "omega",
             "nexus", "cipher", "ghost", "viper", "cobra", "black", "red", "silent",
             "storm", "pulse", "core", "byte", "flux", "hex", "bit", "syn", "net"]
    tlds = [".onion", ".xyz", ".io", ".cc", ".ru", ".cn", ".net", ".org", ".tk", ".top"]
    return random.choice(words) + random.choice(words) + str(random.randint(1, 999)) + random.choice(tlds)


def rand_port():
    return random.choice([21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995,
                          1433, 1521, 2049, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017])


SEVERITIES = ["critical", "high", "medium", "low", "informational"]
PROTOCOLS = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "DNS", "SSH", "FTP", "SMTP", "SNMP",
             "TLS", "ARP", "DHCP", "NTP", "LDAP", "RDP", "SMB", "MQTT", "gRPC", "WebSocket"]
OS_LIST = ["Linux 5.15", "Linux 6.1", "Windows Server 2022", "Windows 11", "FreeBSD 14",
           "macOS Ventura", "Ubuntu 22.04", "Debian 12", "CentOS Stream 9", "Fedora 39",
           "Kali 2024.1", "Arch Linux", "Alpine 3.19", "RHEL 9", "OpenBSD 7.4"]
VENDORS = ["Cisco", "Palo Alto", "Fortinet", "Juniper", "F5", "Check Point", "SonicWall",
           "Barracuda", "Sophos", "Trend Micro", "CrowdStrike", "DarknodeOne", "Carbon Black",
           "Symantec", "McAfee", "Mandiant", "Recorded Future", "Anomali", "ThreatConnect"]

MITRE_TACTICS = [
    "TA0001-Initial Access", "TA0002-Execution", "TA0003-Persistence",
    "TA0004-Privilege Escalation", "TA0005-Defense Evasion", "TA0006-Credential Access",
    "TA0007-Discovery", "TA0008-Lateral Movement", "TA0009-Collection",
    "TA0010-Exfiltration", "TA0011-Command and Control", "TA0040-Impact"
]

MITRE_TECHNIQUES = [
    "T1059-Command and Scripting Interpreter", "T1053-Scheduled Task/Job",
    "T1547-Boot or Logon Autostart Execution", "T1548-Abuse Elevation Control Mechanism",
    "T1027-Obfuscated Files or Information", "T1003-OS Credential Dumping",
    "T1082-System Information Discovery", "T1021-Remote Services",
    "T1005-Data from Local System", "T1041-Exfiltration Over C2 Channel",
    "T1071-Application Layer Protocol", "T1486-Data Encrypted for Impact",
    "T1566-Phishing", "T1190-Exploit Public-Facing Application",
    "T1078-Valid Accounts", "T1055-Process Injection", "T1036-Masquerading",
    "T1098-Account Manipulation", "T1070-Indicator Removal", "T1110-Brute Force",
    "T1018-Remote System Discovery", "T1570-Lateral Tool Transfer",
    "T1560-Archive Collected Data", "T1048-Exfiltration Over Alternative Protocol",
    "T1573-Encrypted Channel", "T1490-Inhibit System Recovery",
    "T1204-User Execution", "T1133-External Remote Services",
    "T1543-Create or Modify System Process", "T1068-Exploitation for Privilege Escalation"
]

MALWARE_FAMILIES = [
    "DarkComet", "Emotet", "TrickBot", "Ryuk", "Conti", "LockBit", "BlackCat", "Hive",
    "Cobalt Strike", "Metasploit", "Mimikatz", "BloodHound", "Sliver", "Brute Ratel",
    "QakBot", "IcedID", "BazarLoader", "Dridex", "Agent Tesla", "FormBook",
    "RedLine", "Raccoon", "Vidar", "AsyncRAT", "NjRAT", "Remcos", "Warzone RAT",
    "PlugX", "ShadowPad", "Winnti", "APT41 Toolkit", "Lazarus Suite", "Turla Snake",
    "Fancy Bear X-Agent", "Equation Group Tools", "DarkSide", "REvil", "BlackMatter",
    "Pandora", "Royal", "Play", "BianLian", "Akira", "Medusa", "NoEscape",
    "PhobosRAT", "SystemBC", "BumbleBee", "Pikabot", "DarkGate"
]

HACKER_HANDLES = [
    "z3r0day", "ph4ntom", "n1ghtshade", "v0idwalker", "c1ph3r", "darkfl0w", "r00tk1t",
    "gh0stpr0t0col", "nullbyt3", "sh4d0wm1nd", "h3xm4ster", "byt3cr4ft", "d4t4wr41th",
    "n3tw0rkn1nja", "c0d3sp3ctr3", "b1naryb0ss", "3xpl01t3r", "cr4ckj4ck", "s1l3ntst0rm",
    "d1g1t4lfury", "m4lw4r3m4g3", "p4ck3tsniff3r", "r3v3rs3r", "d3crypt0r", "pr0xyh4ck"
]

SKILL_CATEGORIES = [
    "Reverse Engineering", "Exploit Development", "Malware Analysis", "Network Penetration",
    "Web Application Security", "Cryptanalysis", "Social Engineering", "Digital Forensics",
    "Binary Exploitation", "Kernel Hacking", "Wireless Security", "Cloud Security",
    "SCADA/ICS Hacking", "Mobile Security", "Blockchain Analysis", "OSINT",
    "Steganography", "Firmware Analysis", "Protocol Analysis", "Red Teaming"
]

BADGES = [
    "First Blood", "Zero Day Hunter", "Root Access", "Ghost Protocol", "Shadow Ops",
    "Cipher Master", "Network Ninja", "Malware Surgeon", "Forensic Eye", "Crypto Breaker",
    "Bug Bounty Legend", "CTF Champion", "Penetration Expert", "Exploit Artist",
    "Threat Hunter", "Incident Commander", "Security Architect", "Code Auditor",
    "Vulnerability Researcher", "APT Tracker", "Darknet Explorer", "Binary Wizard",
    "Packet Whisperer", "Firewall Breacher", "Privilege Escalator", "Data Exfiltrator",
    "Shell Master", "Kernel Panic", "Memory Corruption", "Race Condition"
]

LOG_SOURCES = [
    "kernel", "sshd", "nginx", "apache2", "systemd", "firewalld", "auditd", "cron",
    "darknode-core", "darknode-darknode", "darknode-nexus", "darknode-proxy",
    "darknode-scanner", "darknode-crypto", "darknode-mesh", "darknode-vault",
    "iptables", "fail2ban", "snort", "suricata", "ossec", "wazuh", "rsyslog",
    "postgres", "redis", "elasticsearch", "docker", "containerd", "kubelet"
]


# ---------------------------------------------------------------------------
# 1. exploits-db.json  (~15000 lines)
# ---------------------------------------------------------------------------
def gen_exploits_db():
    print("Generating exploits-db.json ...")
    exploit_types = ["Remote Code Execution", "Buffer Overflow", "SQL Injection",
                     "Cross-Site Scripting", "Privilege Escalation", "Denial of Service",
                     "Authentication Bypass", "Directory Traversal", "Command Injection",
                     "Deserialization", "Use-After-Free", "Integer Overflow",
                     "Format String", "Race Condition", "Memory Corruption",
                     "Heap Overflow", "Stack Overflow", "Type Confusion",
                     "Logic Flaw", "Information Disclosure"]
    platforms = ["Windows", "Linux", "macOS", "iOS", "Android", "FreeBSD",
                 "Cisco IOS", "Juniper JUNOS", "Palo Alto PAN-OS", "VMware ESXi",
                 "Docker", "Kubernetes", "AWS", "Azure", "GCP"]
    categories = ["webapp", "network", "local", "remote", "kernel", "firmware",
                  "cloud", "container", "iot", "scada", "mobile", "wireless"]
    entries = []
    for i in range(500):
        year = random.randint(2018, 2026)
        seq = random.randint(1000, 59999)
        cve = f"CVE-{year}-{seq}"
        etype = random.choice(exploit_types)
        sev = random.choice(SEVERITIES[:4])
        cvss = round(random.uniform(3.0, 10.0), 1)
        affected = random.sample(platforms, random.randint(1, 4))
        payload_lines = []
        for _ in range(random.randint(5, 15)):
            payload_lines.append(rand_hex(random.randint(40, 120)))
        mitigation_steps = [
            f"Apply vendor patch {cve}-fix-{random.randint(1,9)}",
            f"Update to version {random.randint(2,15)}.{random.randint(0,9)}.{random.randint(1,30)}",
            f"Implement WAF rule to block {etype.lower()} patterns",
            f"Restrict network access to affected service on port {rand_port()}",
            f"Enable ASLR and DEP on affected systems",
            f"Monitor IDS/IPS for signature SID-{random.randint(100000,999999)}",
            f"Disable unnecessary service: {random.choice(['smb','rdp','telnet','ftp','snmp'])}",
        ]
        references = [
            f"https://nvd.nist.gov/vuln/detail/{cve}",
            f"https://exploit-db.com/exploits/{random.randint(40000,55000)}",
            f"https://github.com/advisories/GHSA-{rand_hex(4)}-{rand_hex(4)}-{rand_hex(4)}",
            f"https://www.cvedetails.com/cve/{cve}/",
            f"https://packetstormsecurity.com/files/{random.randint(160000,180000)}/",
        ]
        entry = {
            "id": f"DKEXP-{i+1:04d}",
            "cve": cve,
            "title": f"{etype} in {random.choice(affected)} {random.choice(['Service','Daemon','Module','Component','Driver','Library','API','Protocol Handler'])}",
            "type": etype,
            "category": random.choice(categories),
            "severity": sev,
            "cvss_v3": cvss,
            "cvss_vector": f"CVSS:3.1/AV:{random.choice('NAL')}/AC:{random.choice('LH')}/PR:{random.choice('NLH')}/UI:{random.choice('NR')}/S:{random.choice('UC')}/C:{random.choice('NLH')}/I:{random.choice('NLH')}/A:{random.choice('NLH')}",
            "affected_systems": affected,
            "affected_versions": [f"{random.randint(1,12)}.{random.randint(0,9)}.{random.randint(0,30)}" for _ in range(random.randint(2, 5))],
            "discovery_date": f"{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "disclosure_date": f"{year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "patch_available": random.choice([True, True, True, False]),
            "exploit_available": random.choice([True, True, False]),
            "in_the_wild": random.choice([True, False, False, False]),
            "payload": {
                "type": random.choice(["shellcode", "python", "ruby", "powershell", "bash", "c", "raw"]),
                "architecture": random.choice(["x86", "x86_64", "arm", "arm64", "mips", "universal"]),
                "size_bytes": random.randint(128, 65536),
                "encoded": random.choice([True, False]),
                "encoder": random.choice(["xor", "base64", "shikata_ga_nai", "alpha_mixed", "none"]),
                "bad_chars": "\\x00\\x0a\\x0d" if random.random() > 0.3 else "\\x00",
                "hex_dump": payload_lines,
                "shellcode_hash": rand_hash("sha256"),
            },
            "technical_details": {
                "description": f"A {sev}-severity {etype.lower()} vulnerability exists in the {random.choice(['input validation','authentication','session management','memory management','file handling','network protocol','cryptographic','access control'])} module. An attacker can exploit this by sending specially crafted {random.choice(['packets','requests','input','payloads','data'])} to the target {random.choice(['service','server','application','endpoint','daemon'])}.",
                "root_cause": random.choice(["Improper input validation", "Missing bounds check", "Incorrect access control",
                                             "Use of deprecated cryptographic algorithm", "Race condition in shared resource",
                                             "Uninitialized memory access", "Integer overflow in size calculation",
                                             "Missing authentication for critical function", "Improper neutralization of special elements",
                                             "Incorrect permission assignment"]),
                "attack_vector": random.choice(["Network", "Adjacent Network", "Local", "Physical"]),
                "attack_complexity": random.choice(["Low", "High"]),
                "privileges_required": random.choice(["None", "Low", "High"]),
                "user_interaction": random.choice(["None", "Required"]),
                "impact": {
                    "confidentiality": random.choice(["None", "Low", "High"]),
                    "integrity": random.choice(["None", "Low", "High"]),
                    "availability": random.choice(["None", "Low", "High"])
                },
                "proof_of_concept": f"#!/usr/bin/env python3\nimport socket\nimport struct\n\ntarget = '{rand_ip()}'\nport = {rand_port()}\n\ndef exploit():\n    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n    s.connect((target, port))\n    payload = b'\\x41' * {random.randint(256, 8192)}\n    payload += struct.pack('<Q', 0x{rand_hex(16)})\n    payload += b'\\x90' * {random.randint(16, 256)}\n    s.send(payload)\n    response = s.recv(4096)\n    print(f'Response: {{response}}')\n    s.close()\n\nif __name__ == '__main__':\n    exploit()\n",
            },
            "mitigation": random.sample(mitigation_steps, random.randint(3, 6)),
            "references": random.sample(references, random.randint(2, 5)),
            "tags": random.sample(["0day", "wormable", "rce", "dos", "lpe", "auth-bypass",
                                    "web", "network", "kernel", "critical-infra", "apt-used",
                                    "ransomware", "supply-chain", "iot", "cloud"], random.randint(2, 6)),
            "author": random.choice(HACKER_HANDLES),
            "last_modified": rand_ts(),
        }
        entries.append(entry)
    write_json(os.path.join(DATA_DIR, "exploits-db.json"), {"exploits": entries, "metadata": {"total": len(entries), "generated": rand_ts(), "version": "3.7.1"}})


# ---------------------------------------------------------------------------
# 2. network-topology.json  (~12000 lines)
# ---------------------------------------------------------------------------
def gen_network_topology():
    print("Generating network-topology.json ...")
    node_types = ["router", "switch", "firewall", "server", "workstation", "iot_device",
                  "access_point", "load_balancer", "ids", "honeypot", "vpn_gateway",
                  "dns_server", "proxy", "storage", "hypervisor"]
    vlans = [{"id": v, "name": n, "cidr": c} for v, n, c in [
        (10, "Management", "10.0.10.0/24"), (20, "Servers", "10.0.20.0/24"),
        (30, "Workstations", "10.0.30.0/24"), (40, "DMZ", "10.0.40.0/24"),
        (50, "IoT", "10.0.50.0/24"), (60, "Guest", "10.0.60.0/24"),
        (70, "VoIP", "10.0.70.0/24"), (80, "Security", "10.0.80.0/24"),
        (100, "DarkNet Mesh", "172.16.0.0/16"), (200, "Shadow Net", "192.168.100.0/24"),
    ]]
    nodes = []
    for i in range(200):
        ntype = random.choice(node_types)
        vlan = random.choice(vlans)
        ifaces = []
        for j in range(random.randint(1, 6)):
            ifaces.append({
                "name": f"eth{j}" if j < 4 else f"bond{j-4}",
                "mac": rand_mac(),
                "ip": rand_ip(),
                "subnet": random.choice(["255.255.255.0", "255.255.254.0", "255.255.240.0"]),
                "speed": random.choice(["100Mbps", "1Gbps", "10Gbps", "25Gbps", "40Gbps"]),
                "duplex": "full",
                "status": random.choice(["up", "up", "up", "down"]),
                "mtu": random.choice([1500, 9000]),
                "rx_bytes": random.randint(10**6, 10**12),
                "tx_bytes": random.randint(10**6, 10**12),
                "rx_packets": random.randint(10**4, 10**9),
                "tx_packets": random.randint(10**4, 10**9),
                "rx_errors": random.randint(0, 1000),
                "tx_errors": random.randint(0, 500),
                "rx_dropped": random.randint(0, 200),
                "tx_dropped": random.randint(0, 100),
            })
        services_on_node = []
        for _ in range(random.randint(1, 8)):
            services_on_node.append({
                "name": random.choice(["ssh", "http", "https", "dns", "smtp", "ntp",
                                       "snmp", "ldap", "rdp", "mysql", "postgres",
                                       "redis", "elasticsearch", "kafka", "darknode-agent"]),
                "port": rand_port(),
                "protocol": random.choice(["TCP", "UDP"]),
                "status": random.choice(["running", "running", "running", "stopped", "error"]),
                "pid": random.randint(100, 65535),
                "uptime_seconds": random.randint(60, 10**7),
            })
        routes = []
        for _ in range(random.randint(2, 8)):
            routes.append({
                "destination": f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.0/{random.choice([8,16,24])}",
                "gateway": rand_ip(),
                "interface": random.choice([ifc["name"] for ifc in ifaces]),
                "metric": random.randint(1, 1000),
                "flags": random.choice(["UG", "U", "UGS", "UH"]),
            })
        node = {
            "id": f"NODE-{i+1:04d}",
            "hostname": f"dn-{ntype[:3]}-{rand_hex(4)}",
            "type": ntype,
            "os": random.choice(OS_LIST),
            "vendor": random.choice(VENDORS) if ntype in ["router", "switch", "firewall", "ids"] else "DarkNode Systems",
            "model": f"DN-{random.randint(1000,9999)}{random.choice('ABCDEFG')}",
            "firmware_version": f"{random.randint(1,8)}.{random.randint(0,15)}.{random.randint(0,99)}",
            "serial": f"DN{rand_hex(12).upper()}",
            "location": {
                "rack": f"R{random.randint(1,50):02d}",
                "unit": random.randint(1, 42),
                "datacenter": random.choice(["DC-ALPHA", "DC-BRAVO", "DC-CHARLIE", "DC-SHADOW", "DC-VOID"]),
                "floor": random.randint(1, 5),
                "gps": {"lat": round(random.uniform(-90, 90), 6), "lon": round(random.uniform(-180, 180), 6)}
            },
            "vlan": vlan,
            "interfaces": ifaces,
            "services": services_on_node,
            "routing_table": routes,
            "hardware": {
                "cpu": random.choice(["Intel Xeon E-2388G", "AMD EPYC 7763", "ARM Cortex-A78",
                                      "Intel Core i9-13900K", "AMD Ryzen 9 7950X", "Qualcomm Snapdragon 8cx"]),
                "cores": random.choice([2, 4, 8, 16, 32, 64, 128]),
                "ram_gb": random.choice([4, 8, 16, 32, 64, 128, 256, 512]),
                "storage": [{"type": random.choice(["NVMe SSD", "SATA SSD", "HDD", "NVMe"]),
                             "capacity_gb": random.choice([256, 512, 1024, 2048, 4096, 8192]),
                             "used_pct": round(random.uniform(5, 95), 1)} for _ in range(random.randint(1, 4))],
                "gpu": random.choice([None, "NVIDIA A100", "NVIDIA T4", "AMD MI250X"]),
            },
            "security": {
                "firewall_enabled": random.choice([True, True, True, False]),
                "ids_enabled": random.choice([True, True, False]),
                "encryption": random.choice(["AES-256-GCM", "ChaCha20-Poly1305", "AES-128-CBC", "none"]),
                "last_scan": rand_ts(),
                "vulnerabilities_found": random.randint(0, 50),
                "compliance_score": round(random.uniform(40, 100), 1),
                "certificates": [{"cn": rand_domain(), "issuer": random.choice(["DarkNode CA", "Let's Encrypt", "DigiCert"]),
                                   "expires": f"2027-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                                   "fingerprint": rand_hash("sha1")} for _ in range(random.randint(0, 3))],
            },
            "status": random.choice(["online", "online", "online", "online", "degraded", "offline", "maintenance"]),
            "uptime_seconds": random.randint(3600, 10**8),
            "last_seen": rand_ts(),
        }
        nodes.append(node)
    # connections
    connections = []
    for i in range(400):
        src = random.randint(0, 199)
        dst = random.randint(0, 199)
        if src == dst:
            dst = (dst + 1) % 200
        connections.append({
            "id": f"CONN-{i+1:04d}",
            "source": nodes[src]["id"],
            "target": nodes[dst]["id"],
            "type": random.choice(["ethernet", "fiber", "wireless", "vpn_tunnel", "mesh_link", "dark_channel"]),
            "protocol": random.choice(PROTOCOLS),
            "bandwidth_mbps": random.choice([100, 1000, 10000, 25000, 40000]),
            "latency_ms": round(random.uniform(0.1, 500), 2),
            "packet_loss_pct": round(random.uniform(0, 5), 3),
            "jitter_ms": round(random.uniform(0, 50), 2),
            "encrypted": random.choice([True, True, False]),
            "status": random.choice(["active", "active", "active", "degraded", "down"]),
            "established": rand_ts(2025),
            "bytes_transferred": random.randint(10**6, 10**14),
        })
    write_json(os.path.join(DATA_DIR, "network-topology.json"), {
        "topology": {"nodes": nodes, "connections": connections, "vlans": vlans},
        "metadata": {"total_nodes": len(nodes), "total_connections": len(connections), "generated": rand_ts(), "version": "2.4.0"}
    })


# ---------------------------------------------------------------------------
# 3. threat-intel.json  (~12000 lines)
# ---------------------------------------------------------------------------
def gen_threat_intel():
    print("Generating threat-intel.json ...")
    ioc_types = ["ip", "domain", "url", "hash_md5", "hash_sha1", "hash_sha256",
                 "email", "mutex", "registry_key", "filename", "certificate_hash"]
    threat_actors = [
        {"name": "APT-PHANTOM", "origin": "Unknown", "motivation": "Espionage"},
        {"name": "SHADOW-BEAR", "origin": "Eastern Europe", "motivation": "Financial"},
        {"name": "DARK-SERPENT", "origin": "East Asia", "motivation": "Espionage"},
        {"name": "NEON-SPIDER", "origin": "South America", "motivation": "Hacktivism"},
        {"name": "VOID-WOLF", "origin": "Middle East", "motivation": "Sabotage"},
        {"name": "GHOST-DRAGON", "origin": "East Asia", "motivation": "IP Theft"},
        {"name": "CRIMSON-HAWK", "origin": "North America", "motivation": "Financial"},
        {"name": "STEEL-VIPER", "origin": "South Asia", "motivation": "Espionage"},
        {"name": "OBSIDIAN-FOX", "origin": "Eastern Europe", "motivation": "Ransomware"},
        {"name": "CIPHER-JACKAL", "origin": "Africa", "motivation": "Fraud"},
        {"name": "QUANTUM-RAVEN", "origin": "Western Europe", "motivation": "Hacktivism"},
        {"name": "BINARY-SCORPION", "origin": "Central Asia", "motivation": "Sabotage"},
    ]
    campaigns = [
        "Operation Midnight Storm", "Operation Digital Harvest", "Operation Shadow Gate",
        "Operation Dark Nexus", "Operation Phantom Grid", "Operation Zero Dawn",
        "Operation Crimson Tide", "Operation Black Mirror", "Operation Silent Thunder",
        "Operation Void Protocol", "Operation Ghost Chain", "Operation Neon Pulse"
    ]
    iocs = []
    for i in range(300):
        ioc_type = random.choice(ioc_types)
        if ioc_type == "ip":
            value = rand_ip()
        elif ioc_type == "domain":
            value = rand_domain()
        elif ioc_type == "url":
            value = f"https://{rand_domain()}/{rand_hex(8)}/{random.choice(['payload','dropper','c2','beacon','exfil','gate'])}.{random.choice(['php','asp','jsp','py','exe','dll'])}"
        elif ioc_type == "hash_md5":
            value = rand_hash("md5")
        elif ioc_type == "hash_sha1":
            value = rand_hash("sha1")
        elif ioc_type == "hash_sha256":
            value = rand_hash("sha256")
        elif ioc_type == "email":
            value = f"{random.choice(HACKER_HANDLES)}@{rand_domain()}"
        elif ioc_type == "mutex":
            value = f"Global\\{rand_hex(8)}-{rand_hex(4)}-{rand_hex(4)}-{rand_hex(12)}"
        elif ioc_type == "registry_key":
            value = f"HKLM\\SOFTWARE\\{random.choice(['Microsoft','Classes','Policies'])}\\{rand_hex(8)}"
        elif ioc_type == "filename":
            value = f"{rand_hex(8)}.{random.choice(['exe','dll','ps1','bat','vbs','js','hta','scr'])}"
        else:
            value = rand_hash("sha1")

        actor = random.choice(threat_actors)
        ttp_list = []
        for _ in range(random.randint(2, 8)):
            ttp_list.append({
                "tactic": random.choice(MITRE_TACTICS),
                "technique": random.choice(MITRE_TECHNIQUES),
                "procedure": f"Threat actor uses {random.choice(['custom tooling','living-off-the-land binaries','fileless malware','encrypted channels','domain fronting','fast flux DNS','process hollowing','DLL side-loading','registry persistence','scheduled tasks'])} to {random.choice(['establish persistence','escalate privileges','evade detection','move laterally','exfiltrate data','maintain access','deploy ransomware','harvest credentials','enumerate network','disable security controls'])}."
            })

        malware_used = random.sample(MALWARE_FAMILIES, random.randint(1, 5))
        c2_infra = []
        for _ in range(random.randint(1, 5)):
            c2_infra.append({
                "ip": rand_ip(),
                "domain": rand_domain(),
                "port": rand_port(),
                "protocol": random.choice(["HTTPS", "DNS", "ICMP", "Custom TCP", "WebSocket", "gRPC"]),
                "beacon_interval_sec": random.randint(10, 3600),
                "jitter_pct": random.randint(0, 50),
                "first_seen": rand_ts(2025),
                "last_seen": rand_ts(),
                "status": random.choice(["active", "active", "sinkholed", "dormant", "taken_down"]),
                "hosting_provider": random.choice(["BulletProof Host Co", "DarkCloud VPS", "ShadowNet Hosting",
                                                    "Offshore Servers LLC", "Anonymous Hosting AG"]),
                "asn": f"AS{random.randint(10000,99999)}",
                "country": random.choice(["RU", "CN", "IR", "KP", "BR", "RO", "UA", "NG", "IN", "VN"]),
            })

        ioc_entry = {
            "id": f"IOC-{i+1:04d}",
            "type": ioc_type,
            "value": value,
            "confidence": random.randint(30, 100),
            "severity": random.choice(SEVERITIES[:4]),
            "first_seen": rand_ts(2024),
            "last_seen": rand_ts(),
            "source": random.choice(["DarkNode ThreatFeed", "OSINT", "Honeypot", "Malware Sandbox",
                                      "Partner Exchange", "Internal Investigation", "Dark Web Monitor"]),
            "threat_actor": actor,
            "campaign": random.choice(campaigns),
            "malware_families": malware_used,
            "ttps": ttp_list,
            "c2_infrastructure": c2_infra,
            "related_iocs": [f"IOC-{random.randint(1,300):04d}" for _ in range(random.randint(1, 6))],
            "tags": random.sample(["apt", "ransomware", "botnet", "phishing", "c2", "dropper",
                                    "exfiltration", "lateral-movement", "persistence", "evasion",
                                    "credential-theft", "supply-chain", "zero-day"], random.randint(2, 6)),
            "kill_chain_phase": random.choice(["reconnaissance", "weaponization", "delivery",
                                                "exploitation", "installation", "command-and-control",
                                                "actions-on-objectives"]),
            "detection_rules": {
                "yara": f"rule {rand_hex(8)} {{ strings: $a = {{{rand_hex(20)}}} condition: $a }}",
                "snort": f'alert tcp any any -> any any (msg:"DarkNode IOC {i+1}"; content:"|{rand_hex(16)}|"; sid:{random.randint(1000000,9999999)}; rev:1;)',
                "sigma": f"title: DarkNode Detection {i+1}\nlogsource:\n  category: process_creation\ndetection:\n  selection:\n    CommandLine|contains: '{rand_hex(12)}'\n  condition: selection",
            },
        }
        iocs.append(ioc_entry)
    write_json(os.path.join(DATA_DIR, "threat-intel.json"), {
        "threat_intelligence": {
            "iocs": iocs,
            "threat_actors": threat_actors,
            "campaigns": campaigns,
        },
        "metadata": {"total_iocs": len(iocs), "generated": rand_ts(), "feed_version": "4.2.0", "classification": "TLP:AMBER"}
    })


# ---------------------------------------------------------------------------
# 4. system-logs.json  (~15000 lines)
# ---------------------------------------------------------------------------
def gen_system_logs():
    print("Generating system-logs.json ...")
    log_levels = ["EMERGENCY", "ALERT", "CRITICAL", "ERROR", "WARNING", "NOTICE", "INFO", "DEBUG"]
    msg_templates = [
        "Connection established from {ip} on port {port}",
        "Authentication failure for user '{user}' from {ip}",
        "Service {service} started successfully (PID {pid})",
        "Disk usage on /dev/{disk} exceeded {pct}% threshold",
        "Firewall rule {rule} matched: DROP {proto} {ip}:{port}",
        "TLS handshake completed with cipher {cipher}",
        "Process {proc} (PID {pid}) killed by OOM killer",
        "Kernel panic - not syncing: {reason}",
        "SELinux: denied {{ {action} }} for pid={pid} comm=\"{proc}\"",
        "Failed password for invalid user {user} from {ip} port {port} ssh2",
        "New USB device found, idVendor={vendor}, idProduct={product}",
        "Out of memory: Killed process {pid} ({proc}) total-vm:{vm}kB",
        "segfault at {addr} ip {addr2} sp {addr3} error {errno}",
        "DarkNode mesh peer {peer} connected via encrypted tunnel",
        "Darknode scan completed: {vulns} vulnerabilities found on {hosts} hosts",
        "Intrusion detected: {attack} from {ip} targeting {target}",
        "Certificate for {domain} expires in {days} days",
        "Database replication lag: {lag}ms (threshold: {threshold}ms)",
        "Container {container} health check failed ({attempts} consecutive failures)",
        "Rate limit exceeded for API key {apikey}: {requests} req/s",
    ]
    entries = []
    for i in range(1000):
        level = random.choice(log_levels)
        src = random.choice(LOG_SOURCES)
        tmpl = random.choice(msg_templates)
        msg = tmpl.format(
            ip=rand_ip(), port=rand_port(), user=random.choice(HACKER_HANDLES),
            service=random.choice(LOG_SOURCES), pid=random.randint(1, 65535),
            disk=random.choice(["sda1", "sdb1", "nvme0n1p1", "mapper/vg0-root"]),
            pct=random.randint(80, 99), rule=f"FW-{random.randint(1,999):03d}",
            proto=random.choice(["TCP", "UDP", "ICMP"]),
            cipher=random.choice(["TLS_AES_256_GCM_SHA384", "TLS_CHACHA20_POLY1305_SHA256",
                                   "ECDHE-RSA-AES128-GCM-SHA256"]),
            proc=random.choice(["nginx", "sshd", "darknode-core", "python3", "java", "node"]),
            reason=random.choice(["VFS: Unable to mount root fs", "Attempted to kill init!",
                                   "Fatal exception in interrupt"]),
            action=random.choice(["read", "write", "execute", "open", "connectto"]),
            vendor=rand_hex(4), product=rand_hex(4),
            vm=random.randint(100000, 99999999),
            addr=f"0x{rand_hex(16)}", addr2=f"0x{rand_hex(16)}", addr3=f"0x{rand_hex(16)}",
            errno=random.randint(1, 15),
            peer=f"PEER-{rand_hex(6)}",
            vulns=random.randint(0, 200), hosts=random.randint(1, 100),
            attack=random.choice(["SQL Injection", "XSS", "Brute Force", "Port Scan",
                                   "Buffer Overflow", "DDoS", "Path Traversal"]),
            target=random.choice(["web-server-01", "db-cluster", "auth-service", "api-gateway"]),
            domain=rand_domain(), days=random.randint(1, 90),
            lag=random.randint(10, 30000), threshold=random.randint(100, 5000),
            container=f"dk-{rand_hex(12)}", attempts=random.randint(3, 20),
            apikey=f"dk_{rand_hex(32)}", requests=random.randint(100, 50000),
        )
        # stack trace for errors/criticals
        stack = None
        if level in ("EMERGENCY", "ALERT", "CRITICAL", "ERROR") and random.random() > 0.3:
            frames = []
            for f_idx in range(random.randint(5, 20)):
                frames.append({
                    "file": f"/opt/darknode/{random.choice(['core','lib','modules','services','utils'])}/{rand_hex(8)}.{random.choice(['py','go','rs','c','cpp'])}",
                    "line": random.randint(1, 5000),
                    "function": f"{random.choice(['handle','process','validate','parse','execute','dispatch','resolve','transform'])}_{rand_hex(6)}",
                    "locals": {f"var_{j}": rand_hex(random.randint(4, 32)) for j in range(random.randint(2, 6))},
                })
            stack = {
                "exception_type": random.choice(["RuntimeError", "SegmentationFault", "NullPointerException",
                                                  "BufferOverflowError", "ConnectionRefused", "TimeoutError",
                                                  "PermissionDenied", "OutOfMemoryError", "PanicException"]),
                "message": msg,
                "frames": frames,
                "thread_id": random.randint(1, 256),
                "thread_name": f"worker-{random.randint(1,64)}",
            }
        ctx = {
            "hostname": f"dn-{rand_hex(4)}",
            "ip": rand_ip(),
            "process": src,
            "pid": random.randint(1, 65535),
            "tid": random.randint(1, 512),
            "user": random.choice(["root", "darknode", "daemon", "www-data", "nobody"]),
            "session_id": rand_hex(32),
            "correlation_id": f"{rand_hex(8)}-{rand_hex(4)}-{rand_hex(4)}-{rand_hex(4)}-{rand_hex(12)}",
            "environment": random.choice(["production", "staging", "development"]),
            "region": random.choice(["us-east-1", "eu-west-1", "ap-southeast-1", "darknet-alpha", "darknet-beta"]),
        }
        entry = {
            "id": f"LOG-{i+1:06d}",
            "timestamp": rand_ts(),
            "level": level,
            "facility": random.choice(["kern", "user", "daemon", "auth", "syslog", "local0", "local7"]),
            "source": src,
            "message": msg,
            "context": ctx,
        }
        if stack:
            entry["stack_trace"] = stack
        entries.append(entry)
    write_json(os.path.join(DATA_DIR, "system-logs.json"), {
        "logs": entries,
        "metadata": {"total": len(entries), "generated": rand_ts(), "retention_days": 90}
    })


# ---------------------------------------------------------------------------
# 5. user-profiles.json  (~8000 lines)
# ---------------------------------------------------------------------------
def gen_user_profiles():
    print("Generating user-profiles.json ...")
    profiles = []
    all_handles = list(HACKER_HANDLES) + [f"{random.choice(['x','0x','_'])}{rand_hex(6)}" for _ in range(75)]
    for i in range(100):
        handle = all_handles[i] if i < len(all_handles) else f"user_{rand_hex(6)}"
        skills = []
        for sk in random.sample(SKILL_CATEGORIES, random.randint(3, 10)):
            skills.append({
                "name": sk,
                "level": random.randint(1, 100),
                "xp": random.randint(100, 500000),
                "certifications": random.sample([
                    "OSCP", "OSCE", "OSWE", "GPEN", "GXPN", "CEH", "CISSP", "CISM",
                    "GCIH", "GCFA", "GNFA", "GREM", "eCPPT", "eCPTX", "CRTP", "CRTO"
                ], random.randint(0, 4)),
                "projects_completed": random.randint(0, 200),
            })
        history = []
        for _ in range(random.randint(5, 30)):
            history.append({
                "action": random.choice(["exploit_submitted", "vulnerability_reported", "ctf_win",
                                          "tool_published", "bounty_earned", "code_reviewed",
                                          "training_completed", "mission_completed", "team_joined",
                                          "rank_up", "badge_earned", "challenge_solved"]),
                "timestamp": rand_ts(),
                "details": {
                    "target": random.choice([rand_domain(), rand_ip(), f"CTF-{rand_hex(6)}"]),
                    "reward": random.randint(0, 50000) if random.random() > 0.5 else None,
                    "difficulty": random.choice(["trivial", "easy", "medium", "hard", "insane"]),
                    "points": random.randint(10, 10000),
                },
            })
        tools_used = []
        for _ in range(random.randint(3, 15)):
            tools_used.append({
                "name": random.choice(["Metasploit", "Burp Suite", "Nmap", "Wireshark", "Ghidra",
                                        "IDA Pro", "Cobalt Strike", "Hashcat", "John the Ripper",
                                        "sqlmap", "Aircrack-ng", "Volatility", "Autopsy", "Radare2",
                                        "Binary Ninja", "x64dbg", "Frida", "Objection", "DarkNode Toolkit",
                                        "BloodHound", "Responder", "CrackMapExec", "Impacket", "Mimikatz"]),
                "proficiency": random.choice(["beginner", "intermediate", "advanced", "expert", "master"]),
                "hours_used": random.randint(10, 50000),
            })
        profile = {
            "id": f"USER-{i+1:04d}",
            "handle": handle,
            "avatar_hash": rand_hash("md5"),
            "rank": random.choice(["Script Kiddie", "Apprentice", "Journeyman", "Expert",
                                    "Master", "Elite", "Legendary", "Shadow Architect"]),
            "reputation": random.randint(0, 1000000),
            "level": random.randint(1, 100),
            "xp_total": random.randint(1000, 10000000),
            "joined": rand_ts(random.randint(2020, 2025)),
            "last_active": rand_ts(),
            "status": random.choice(["online", "away", "busy", "invisible", "offline"]),
            "bio": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(50, 200)))}",
            "location": random.choice(["Unknown", "Darknet", "Cyberspace", "The Grid", "Null Zone",
                                        "Shadow Realm", "Digital Void", "Matrix Node", "Underground"]),
            "pgp_fingerprint": f"{rand_hex(4)} {rand_hex(4)} {rand_hex(4)} {rand_hex(4)} {rand_hex(4)}  {rand_hex(4)} {rand_hex(4)} {rand_hex(4)} {rand_hex(4)} {rand_hex(4)}".upper(),
            "skills": skills,
            "badges": random.sample(BADGES, random.randint(3, 15)),
            "history": history,
            "tools": tools_used,
            "statistics": {
                "exploits_submitted": random.randint(0, 500),
                "vulnerabilities_found": random.randint(0, 1000),
                "ctf_wins": random.randint(0, 100),
                "ctf_participations": random.randint(0, 500),
                "bounties_earned_usd": random.randint(0, 2000000),
                "code_commits": random.randint(0, 50000),
                "missions_completed": random.randint(0, 300),
                "upvotes_received": random.randint(0, 100000),
                "followers": random.randint(0, 50000),
                "following": random.randint(0, 5000),
            },
            "preferences": {
                "theme": random.choice(["dark-matrix", "neon-cyber", "void-black", "blood-red", "ice-blue"]),
                "terminal_font": random.choice(["JetBrains Mono", "Fira Code", "Hack", "Source Code Pro", "Cascadia Code"]),
                "shell": random.choice(["zsh", "bash", "fish", "darkshell", "powershell"]),
                "editor": random.choice(["vim", "neovim", "emacs", "vscode", "nano", "darknode-edit"]),
                "language": random.choice(["en", "ja", "zh", "ru", "de", "ko", "ar", "pt"]),
                "notifications": {"email": random.choice([True, False]), "push": random.choice([True, False]),
                                   "sound": random.choice([True, False]), "desktop": random.choice([True, False])},
            },
        }
        profiles.append(profile)
    write_json(os.path.join(DATA_DIR, "user-profiles.json"), {
        "users": profiles,
        "metadata": {"total": len(profiles), "generated": rand_ts()}
    })


# ---------------------------------------------------------------------------
# 6. malware-signatures.json  (~12000 lines)
# ---------------------------------------------------------------------------
def gen_malware_signatures():
    print("Generating malware-signatures.json ...")
    behaviors = [
        "Process injection via CreateRemoteThread",
        "Registry modification for persistence",
        "DNS tunneling for C2 communication",
        "File encryption with AES-256",
        "Credential harvesting from LSASS memory",
        "Lateral movement via SMB/PsExec",
        "Data exfiltration over HTTPS",
        "Anti-VM detection via CPUID instruction",
        "Rootkit installation via driver loading",
        "Keylogger with screenshot capture",
        "Browser cookie/password theft",
        "Cryptocurrency mining (Monero XMR)",
        "Fileless execution via PowerShell",
        "DLL sideloading for evasion",
        "Ransomware note creation and wallpaper change",
        "Shadow copy deletion via vssadmin",
        "Disabling Windows Defender real-time protection",
        "Establishing reverse shell over TCP",
        "Clipboard hijacking for cryptocurrency addresses",
        "Bootkit modification of MBR/VBR",
    ]
    entries = []
    for i in range(400):
        family = random.choice(MALWARE_FAMILIES)
        variant = f"{family}.{random.choice(string.ascii_uppercase)}{random.randint(1,99)}"
        detection_names = [
            f"Trojan.{family}.{rand_hex(4).upper()}",
            f"Win32/{family}.{random.choice(string.ascii_uppercase)}!{random.choice(['ml','mtb','rfn'])}",
            f"Mal/{family}-{random.choice(string.ascii_uppercase)}",
            f"HEUR:Trojan.Win32.{family}.gen",
            f"a]variant.{family}.{random.randint(1,999)}",
        ]
        static_indicators = {
            "file_size_range": {"min": random.randint(1024, 65536), "max": random.randint(65537, 10485760)},
            "file_types": random.sample(["PE32", "PE64", "ELF", "Mach-O", "DLL", "SYS", "MSI",
                                          "JAR", "PS1", "VBS", "HTA", "JS", "LNK", "ISO", "IMG"], random.randint(1, 4)),
            "entropy": round(random.uniform(6.0, 8.0), 4),
            "packer": random.choice(["UPX", "Themida", "VMProtect", "ASPack", "PECompact", "Custom", "None"]),
            "compiler": random.choice(["MSVC", "MinGW", "GCC", "Go", "Rust", "Nim", "Delphi", ".NET", "Python"]),
            "imports_suspicious": random.sample([
                "VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread", "NtUnmapViewOfSection",
                "ZwQuerySystemInformation", "GetProcAddress", "LoadLibraryA", "WinExec",
                "ShellExecuteA", "URLDownloadToFileA", "InternetOpenA", "CryptEncrypt",
                "RegSetValueExA", "CreateServiceA", "AdjustTokenPrivileges"
            ], random.randint(3, 10)),
            "sections": [
                {"name": s, "entropy": round(random.uniform(3.0, 8.0), 4),
                 "virtual_size": random.randint(4096, 1048576),
                 "raw_size": random.randint(4096, 1048576),
                 "characteristics": random.choice(["0xE0000060", "0x60000020", "0xC0000040"])}
                for s in random.sample([".text", ".rdata", ".data", ".rsrc", ".reloc", ".bss",
                                         ".upx0", ".upx1", ".vmp0", ".themida"], random.randint(3, 7))
            ],
        }
        network_indicators = {
            "domains": [rand_domain() for _ in range(random.randint(1, 8))],
            "ips": [rand_ip() for _ in range(random.randint(1, 6))],
            "urls": [f"https://{rand_domain()}/{rand_hex(8)}" for _ in range(random.randint(1, 5))],
            "user_agents": [f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) {rand_hex(16)}" for _ in range(random.randint(1, 3))],
            "c2_protocol": random.choice(["HTTPS", "DNS", "ICMP", "Custom Binary", "WebSocket", "Tor"]),
            "dns_queries": [f"{rand_hex(12)}.{rand_domain()}" for _ in range(random.randint(1, 5))],
        }
        sandbox_results = {
            "score": random.randint(30, 100),
            "verdict": random.choice(["malicious", "malicious", "suspicious", "likely_malicious"]),
            "execution_time_sec": random.randint(30, 600),
            "processes_created": random.randint(1, 30),
            "files_created": random.randint(0, 50),
            "files_modified": random.randint(0, 30),
            "files_deleted": random.randint(0, 20),
            "registry_keys_modified": random.randint(0, 100),
            "network_connections": random.randint(0, 50),
            "mutexes_created": [f"Global\\{rand_hex(16)}" for _ in range(random.randint(0, 5))],
            "screenshots_captured": random.randint(0, 10),
        }

        entry = {
            "id": f"MAL-{i+1:04d}",
            "family": family,
            "variant": variant,
            "classification": random.choice(["trojan", "ransomware", "worm", "rat", "backdoor",
                                              "rootkit", "botnet", "spyware", "adware", "miner",
                                              "dropper", "loader", "stealer", "clipper", "wiper"]),
            "severity": random.choice(SEVERITIES[:3]),
            "first_seen": rand_ts(random.randint(2019, 2025)),
            "last_seen": rand_ts(),
            "hashes": {
                "md5": rand_hash("md5"),
                "sha1": rand_hash("sha1"),
                "sha256": rand_hash("sha256"),
                "ssdeep": f"{random.randint(100,9999)}:{rand_hex(30)}:{rand_hex(30)}",
                "imphash": rand_hash("md5"),
                "tlsh": f"T1{rand_hex(70)}",
            },
            "detection_names": detection_names,
            "behaviors": random.sample(behaviors, random.randint(3, 10)),
            "static_indicators": static_indicators,
            "network_indicators": network_indicators,
            "sandbox_results": sandbox_results,
            "mitre_mapping": [
                {"tactic": random.choice(MITRE_TACTICS), "technique": random.choice(MITRE_TECHNIQUES)}
                for _ in range(random.randint(2, 8))
            ],
            "detection_rules": {
                "yara": f"rule {family}_{rand_hex(6)} {{\n  meta:\n    author = \"DarkNode Threat Lab\"\n    date = \"{rand_ts()[:10]}\"\n    description = \"Detects {variant}\"\n  strings:\n    $hex1 = {{ {' '.join(rand_hex(2) for _ in range(16))} }}\n    $str1 = \"{rand_hex(16)}\" ascii wide\n    $str2 = \"{rand_hex(12)}\" ascii\n  condition:\n    uint16(0) == 0x5A4D and any of them\n}}",
                "snort": f'alert tcp $HOME_NET any -> $EXTERNAL_NET any (msg:"DARKNODE {variant} C2 Traffic"; content:"|{rand_hex(20)}|"; depth:64; sid:{random.randint(3000000,9999999)}; rev:1;)',
            },
            "threat_level": random.randint(1, 10),
            "prevalence": random.choice(["widespread", "common", "uncommon", "rare", "targeted"]),
            "remediation": {
                "automated_removal": random.choice([True, False]),
                "tool": f"DarkNode Cleaner v{random.randint(1,5)}.{random.randint(0,9)}",
                "manual_steps": [
                    f"Boot into safe mode",
                    f"Terminate process {variant.split('.')[0].lower()}.exe",
                    f"Delete file C:\\Windows\\Temp\\{rand_hex(8)}.dll",
                    f"Remove registry key HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\{rand_hex(8)}",
                    f"Run full system scan with updated signatures",
                    f"Reset compromised credentials",
                    f"Monitor network for residual C2 traffic for 72 hours",
                ],
            },
        }
        entries.append(entry)
    write_json(os.path.join(DATA_DIR, "malware-signatures.json"), {
        "signatures": entries,
        "metadata": {"total": len(entries), "generated": rand_ts(), "signature_db_version": "2026.09.08.001"}
    })


# ---------------------------------------------------------------------------
# 7. vulnerability-scan.json  (~10000 lines)
# ---------------------------------------------------------------------------
def gen_vulnerability_scan():
    print("Generating vulnerability-scan.json ...")
    hosts = []
    for i in range(150):
        ip = rand_ip()
        open_ports = []
        for _ in range(random.randint(2, 15)):
            port = rand_port()
            service = random.choice(["ssh", "http", "https", "ftp", "smtp", "dns", "mysql",
                                      "postgres", "redis", "mongodb", "elasticsearch", "rdp",
                                      "smb", "snmp", "ldap", "ntp", "darknode-rpc", "darknode-mesh"])
            vulns = []
            for _ in range(random.randint(0, 8)):
                vulns.append({
                    "cve": f"CVE-{random.randint(2018,2026)}-{random.randint(1000,59999)}",
                    "title": f"{random.choice(['Remote','Local','Authenticated','Unauthenticated'])} {random.choice(['Code Execution','Privilege Escalation','Information Disclosure','Denial of Service','Buffer Overflow','SQL Injection','XSS'])} in {service}",
                    "severity": random.choice(SEVERITIES[:4]),
                    "cvss": round(random.uniform(2.0, 10.0), 1),
                    "description": f"A vulnerability in {service} allows {random.choice(['remote attackers','local users','authenticated users','unauthenticated attackers'])} to {random.choice(['execute arbitrary code','escalate privileges','read sensitive data','cause a denial of service','bypass authentication','inject malicious commands'])} via {random.choice(['specially crafted packets','malformed input','buffer overflow','SQL injection','path traversal','deserialization of untrusted data'])}.",
                    "solution": f"Update {service} to version {random.randint(2,20)}.{random.randint(0,9)}.{random.randint(1,50)} or later",
                    "exploit_available": random.choice([True, False]),
                    "patch_available": random.choice([True, True, True, False]),
                    "references": [f"https://nvd.nist.gov/vuln/detail/CVE-{random.randint(2018,2026)}-{random.randint(1000,59999)}"],
                })
            open_ports.append({
                "port": port,
                "protocol": random.choice(["tcp", "udp"]),
                "state": "open",
                "service": service,
                "version": f"{random.randint(1,15)}.{random.randint(0,9)}.{random.randint(0,99)}",
                "banner": f"{service.upper()}/{random.randint(1,9)}.{random.randint(0,9)} {random.choice(['ready','OK','running','active'])}",
                "ssl": random.choice([True, False]) if port in [443, 8443, 993, 995] else random.choice([True, False, False, False]),
                "vulnerabilities": vulns,
            })

        host = {
            "id": f"HOST-{i+1:04d}",
            "ip": ip,
            "hostname": f"dn-{rand_hex(6)}.darknode.local",
            "mac": rand_mac(),
            "os_detected": random.choice(OS_LIST),
            "os_confidence": random.randint(70, 100),
            "status": "up",
            "scan_time_sec": round(random.uniform(5, 300), 2),
            "ports_scanned": random.choice([1000, 5000, 10000, 65535]),
            "open_ports": open_ports,
            "risk_score": round(random.uniform(0, 100), 1),
            "risk_level": random.choice(["critical", "high", "medium", "low"]),
            "compliance": {
                "pci_dss": random.choice(["pass", "fail", "N/A"]),
                "hipaa": random.choice(["pass", "fail", "N/A"]),
                "nist_800_53": random.choice(["pass", "fail", "N/A"]),
                "cis_benchmark": random.choice(["pass", "fail", "N/A"]),
                "iso_27001": random.choice(["pass", "fail", "N/A"]),
                "score": round(random.uniform(30, 100), 1),
            },
            "network_info": {
                "gateway": rand_ip(),
                "dns_servers": [rand_ip() for _ in range(random.randint(1, 3))],
                "domain": "darknode.local",
                "vlan": random.choice([10, 20, 30, 40, 50, 100]),
            },
            "last_scan": rand_ts(),
        }
        hosts.append(host)
    write_json(os.path.join(DATA_DIR, "vulnerability-scan.json"), {
        "scan_results": {
            "hosts": hosts,
            "summary": {
                "total_hosts": len(hosts),
                "total_vulnerabilities": sum(sum(len(p["vulnerabilities"]) for p in h["open_ports"]) for h in hosts),
                "critical": random.randint(10, 50),
                "high": random.randint(50, 200),
                "medium": random.randint(100, 500),
                "low": random.randint(200, 800),
            },
            "scan_config": {
                "scanner": "DarkNode VulnScanner v4.2",
                "scan_type": "full",
                "port_range": "1-65535",
                "timing": "T4",
                "scripts": ["vuln", "auth", "default", "discovery"],
            },
        },
        "metadata": {"generated": rand_ts(), "scan_id": f"SCAN-{rand_hex(16)}"}
    })


# ---------------------------------------------------------------------------
# 8. packet-captures.json  (~12000 lines)
# ---------------------------------------------------------------------------
def gen_packet_captures():
    print("Generating packet-captures.json ...")
    packets = []
    for i in range(500):
        proto = random.choice(PROTOCOLS)
        src_ip = rand_ip()
        dst_ip = rand_ip()
        src_port = random.randint(1024, 65535)
        dst_port = rand_port()
        payload_size = random.randint(20, 1500)
        hex_lines = []
        for offset in range(0, payload_size, 16):
            chunk_size = min(16, payload_size - offset)
            hex_data = " ".join(rand_hex(2) for _ in range(chunk_size))
            ascii_repr = "".join(random.choice(string.printable[:62] + "....") for _ in range(chunk_size))
            hex_lines.append(f"{offset:04x}  {hex_data:<48s}  |{ascii_repr}|")

        flags = []
        if proto == "TCP":
            flags = random.sample(["SYN", "ACK", "FIN", "RST", "PSH", "URG", "ECE", "CWR"], random.randint(1, 4))

        analysis = {
            "protocol_stack": [],
            "alerts": [],
            "classification": random.choice(["normal", "suspicious", "malicious", "encrypted", "tunneled"]),
        }
        # Build protocol stack
        analysis["protocol_stack"].append({
            "layer": "Ethernet",
            "src_mac": rand_mac(),
            "dst_mac": rand_mac(),
            "ethertype": "0x0800" if random.random() > 0.1 else "0x86DD",
        })
        analysis["protocol_stack"].append({
            "layer": "IP",
            "version": 4,
            "src": src_ip,
            "dst": dst_ip,
            "ttl": random.randint(1, 255),
            "tos": random.choice([0, 32, 40, 46, 48]),
            "id": random.randint(0, 65535),
            "flags": random.choice(["DF", "MF", ""]),
            "fragment_offset": 0,
            "checksum": f"0x{rand_hex(4)}",
        })
        if proto in ["TCP", "HTTP", "HTTPS", "SSH", "FTP", "SMTP"]:
            analysis["protocol_stack"].append({
                "layer": "TCP",
                "src_port": src_port,
                "dst_port": dst_port,
                "seq": random.randint(0, 2**32 - 1),
                "ack": random.randint(0, 2**32 - 1),
                "window": random.randint(1024, 65535),
                "flags": flags,
                "checksum": f"0x{rand_hex(4)}",
                "options": random.sample(["MSS", "SACK", "Timestamps", "Window Scale", "NOP"], random.randint(0, 3)),
            })
        elif proto in ["UDP", "DNS", "SNMP", "NTP", "DHCP"]:
            analysis["protocol_stack"].append({
                "layer": "UDP",
                "src_port": src_port,
                "dst_port": dst_port,
                "length": payload_size + 8,
                "checksum": f"0x{rand_hex(4)}",
            })
        if proto == "HTTP":
            analysis["protocol_stack"].append({
                "layer": "HTTP",
                "method": random.choice(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]),
                "uri": f"/{rand_hex(8)}/{random.choice(['api','data','login','upload','download','status'])}",
                "version": "HTTP/1.1",
                "host": rand_domain(),
                "user_agent": f"DarkNode-Agent/{random.randint(1,5)}.{random.randint(0,9)}",
                "content_type": random.choice(["application/json", "text/html", "application/octet-stream"]),
                "content_length": payload_size,
            })
        elif proto == "DNS":
            analysis["protocol_stack"].append({
                "layer": "DNS",
                "id": random.randint(0, 65535),
                "qr": random.choice([0, 1]),
                "opcode": 0,
                "query": rand_domain(),
                "type": random.choice(["A", "AAAA", "CNAME", "MX", "TXT", "NS", "SOA", "PTR"]),
                "response": [rand_ip() for _ in range(random.randint(0, 4))],
            })

        if analysis["classification"] in ("suspicious", "malicious"):
            alert_msgs = [
                f"Potential C2 beacon detected (interval: {random.randint(10,300)}s)",
                f"Anomalous data transfer: {random.randint(1,100)}MB to external IP",
                f"Known malicious domain contacted: {rand_domain()}",
                f"Suspicious encoded payload in {proto} traffic",
                f"Port scan detected from {src_ip}",
                f"Brute force attempt detected ({random.randint(10,1000)} attempts)",
                f"DNS tunneling indicators detected",
                f"Encrypted channel with non-standard cipher",
            ]
            for _ in range(random.randint(1, 3)):
                analysis["alerts"].append({
                    "rule_id": f"DNIDS-{random.randint(10000,99999)}",
                    "message": random.choice(alert_msgs),
                    "severity": random.choice(SEVERITIES[:3]),
                    "action": random.choice(["alert", "log", "drop", "reject"]),
                })

        packet = {
            "id": f"PKT-{i+1:06d}",
            "timestamp": rand_ts(),
            "capture_interface": random.choice(["eth0", "eth1", "wlan0", "bond0", "tun0", "veth0", "br0"]),
            "frame_length": payload_size + random.randint(14, 54),
            "capture_length": payload_size + random.randint(14, 54),
            "source": {"ip": src_ip, "port": src_port, "mac": rand_mac()},
            "destination": {"ip": dst_ip, "port": dst_port, "mac": rand_mac()},
            "protocol": proto,
            "flags": flags if proto == "TCP" else [],
            "ttl": random.randint(1, 255),
            "payload": {
                "size_bytes": payload_size,
                "hex_dump": hex_lines,
                "entropy": round(random.uniform(3.0, 8.0), 4),
                "printable_pct": round(random.uniform(10, 90), 1),
                "hash": rand_hash("sha256"),
            },
            "analysis": analysis,
            "session_id": f"SES-{rand_hex(16)}",
            "flow": {
                "bytes_to_server": random.randint(100, 10**7),
                "bytes_to_client": random.randint(100, 10**7),
                "packets_to_server": random.randint(1, 10000),
                "packets_to_client": random.randint(1, 10000),
                "duration_ms": random.randint(1, 300000),
                "state": random.choice(["established", "syn_sent", "fin_wait", "closed", "time_wait"]),
            },
        }
        packets.append(packet)
    write_json(os.path.join(DATA_DIR, "packet-captures.json"), {
        "captures": packets,
        "metadata": {"total_packets": len(packets), "generated": rand_ts(), "pcap_version": "2.4", "capture_duration_sec": 3600}
    })


# ---------------------------------------------------------------------------
# 9. forensics-artifacts.json  (~10000 lines)
# ---------------------------------------------------------------------------
def gen_forensics_artifacts():
    print("Generating forensics-artifacts.json ...")
    artifact_types = ["file", "registry", "process", "network_connection", "event_log",
                      "memory_dump", "browser_history", "email", "usb_device", "scheduled_task",
                      "service", "driver", "prefetch", "amcache", "shimcache", "mft_entry"]
    entries = []
    for i in range(200):
        atype = random.choice(artifact_types)
        base = {
            "id": f"ART-{i+1:04d}",
            "case_id": f"CASE-{random.randint(1,50):04d}",
            "type": atype,
            "timestamp": rand_ts(),
            "collected_by": random.choice(HACKER_HANDLES),
            "evidence_source": f"DISK-{rand_hex(8).upper()}",
            "chain_of_custody": [
                {"action": "collected", "by": random.choice(HACKER_HANDLES), "timestamp": rand_ts(), "hash": rand_hash()},
                {"action": "analyzed", "by": random.choice(HACKER_HANDLES), "timestamp": rand_ts(), "hash": rand_hash()},
                {"action": "reported", "by": random.choice(HACKER_HANDLES), "timestamp": rand_ts(), "hash": rand_hash()},
            ],
            "tags": random.sample(["malware", "persistence", "lateral-movement", "exfiltration",
                                    "credential-theft", "c2", "rootkit", "ransomware", "cleanup",
                                    "reconnaissance", "staging", "impact"], random.randint(1, 5)),
            "notes": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(80, 300)))}",
            "risk_score": round(random.uniform(0, 100), 1),
            "ioc_match": random.choice([True, True, False, False, False]),
        }

        if atype == "file":
            base["data"] = {
                "path": f"/{random.choice(['usr','var','tmp','opt','home','etc','root'])}/{random.choice(['lib','bin','share','local','log','cache','darknode'])}/{rand_hex(8)}.{random.choice(['exe','dll','so','py','sh','conf','dat','log','tmp','bin'])}",
                "size_bytes": random.randint(1, 10**9),
                "created": rand_ts(2025),
                "modified": rand_ts(),
                "accessed": rand_ts(),
                "owner": random.choice(["root", "darknode", "www-data", "nobody"]),
                "permissions": random.choice(["rwxr-xr-x", "rw-r--r--", "rwx------", "rw-rw-r--", "rwsr-xr-x"]),
                "hashes": {"md5": rand_hash("md5"), "sha1": rand_hash("sha1"), "sha256": rand_hash("sha256")},
                "magic": random.choice(["ELF 64-bit LSB executable", "PE32+ executable", "Python script",
                                         "Bourne-Again shell script", "data", "gzip compressed data",
                                         "PGP encrypted data", "ASCII text"]),
                "entropy": round(random.uniform(1.0, 8.0), 4),
                "strings_count": random.randint(10, 50000),
                "suspicious_strings": [rand_hex(random.randint(8, 32)) for _ in range(random.randint(0, 10))],
            }
        elif atype == "registry":
            base["data"] = {
                "hive": random.choice(["HKLM", "HKCU", "HKU", "HKCR"]),
                "key": f"SOFTWARE\\{random.choice(['Microsoft','Classes','Policies','DarkNode'])}\\{rand_hex(8)}\\{rand_hex(6)}",
                "value_name": rand_hex(8),
                "value_type": random.choice(["REG_SZ", "REG_DWORD", "REG_BINARY", "REG_EXPAND_SZ", "REG_MULTI_SZ"]),
                "value_data": rand_hex(random.randint(8, 128)),
                "last_modified": rand_ts(),
                "previous_value": rand_hex(random.randint(8, 64)) if random.random() > 0.5 else None,
            }
        elif atype == "process":
            base["data"] = {
                "pid": random.randint(1, 65535),
                "ppid": random.randint(1, 65535),
                "name": random.choice(["svchost.exe", "explorer.exe", "cmd.exe", "powershell.exe",
                                        "darknode-agent", "python3", "bash", "nginx", "java"]),
                "cmdline": f"{random.choice(['/usr/bin/python3','/bin/bash','C:\\Windows\\System32\\cmd.exe'])} {rand_hex(16)}",
                "user": random.choice(["SYSTEM", "root", "darknode", "Administrator"]),
                "start_time": rand_ts(),
                "cpu_pct": round(random.uniform(0, 100), 2),
                "memory_mb": random.randint(1, 8192),
                "threads": random.randint(1, 256),
                "handles": random.randint(10, 5000),
                "network_connections": [
                    {"local": f"{rand_ip()}:{random.randint(1024,65535)}", "remote": f"{rand_ip()}:{rand_port()}",
                     "state": random.choice(["ESTABLISHED", "LISTEN", "TIME_WAIT", "CLOSE_WAIT"]),
                     "protocol": "TCP"} for _ in range(random.randint(0, 8))
                ],
                "loaded_modules": [f"{rand_hex(8)}.{random.choice(['dll','so','dylib'])}" for _ in range(random.randint(5, 30))],
                "injected_code": random.choice([True, False, False, False]),
            }
        elif atype == "memory_dump":
            base["data"] = {
                "dump_type": random.choice(["full", "kernel", "process", "mini"]),
                "size_mb": random.randint(256, 65536),
                "acquisition_tool": random.choice(["winpmem", "LiME", "DumpIt", "Volatility", "DarkNode MemGrab"]),
                "profile": random.choice(["Win10x64_19041", "Win11x64_22621", "Linux_5.15_x64", "Linux_6.1_x64"]),
                "processes_found": random.randint(20, 500),
                "suspicious_processes": random.randint(0, 15),
                "injected_dlls": random.randint(0, 10),
                "hidden_processes": random.randint(0, 5),
                "network_artifacts": random.randint(0, 50),
                "encryption_keys_found": random.randint(0, 10),
                "strings_extracted": random.randint(1000, 1000000),
                "yara_matches": [
                    {"rule": f"MAL_{random.choice(MALWARE_FAMILIES)}_{rand_hex(4)}",
                     "offset": f"0x{rand_hex(16)}",
                     "matched_data": rand_hex(32)} for _ in range(random.randint(0, 8))
                ],
            }
        elif atype == "browser_history":
            base["data"] = {
                "browser": random.choice(["Chrome", "Firefox", "Edge", "Tor Browser", "DarkNode Browser"]),
                "profile": f"Profile {random.randint(0,5)}",
                "entries": [
                    {"url": f"https://{rand_domain()}/{rand_hex(8)}",
                     "title": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(10, 50)))}",
                     "visit_time": rand_ts(),
                     "visit_count": random.randint(1, 100),
                     "typed_count": random.randint(0, 10),
                     "transition": random.choice(["typed", "link", "auto_bookmark", "form_submit", "reload"]),
                     } for _ in range(random.randint(5, 25))
                ],
                "downloads": [
                    {"url": f"https://{rand_domain()}/{rand_hex(8)}.{random.choice(['exe','zip','rar','tar.gz','pdf'])}",
                     "path": f"/home/user/Downloads/{rand_hex(8)}.{random.choice(['exe','zip','rar'])}",
                     "size": random.randint(1024, 10**8),
                     "timestamp": rand_ts(),
                     "hash": rand_hash()} for _ in range(random.randint(0, 10))
                ],
            }
        else:
            base["data"] = {
                "raw": rand_hex(random.randint(64, 512)),
                "parsed": {
                    "timestamp": rand_ts(),
                    "source": random.choice(LOG_SOURCES),
                    "event_id": random.randint(1, 65535),
                    "level": random.choice(["Information", "Warning", "Error", "Critical"]),
                    "message": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(50, 200)))}",
                    "details": {f"field_{j}": rand_hex(random.randint(4, 32)) for j in range(random.randint(3, 10))},
                },
            }

        timeline_events = []
        for _ in range(random.randint(3, 15)):
            timeline_events.append({
                "timestamp": rand_ts(),
                "action": random.choice(["created", "modified", "accessed", "deleted", "executed",
                                          "connected", "transferred", "encrypted", "exfiltrated",
                                          "injected", "loaded", "started", "stopped", "logged"]),
                "details": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(30, 100)))}",
                "source_artifact": f"ART-{random.randint(1,200):04d}" if random.random() > 0.5 else None,
            })
        base["timeline"] = timeline_events
        entries.append(base)

    write_json(os.path.join(DATA_DIR, "forensics-artifacts.json"), {
        "artifacts": entries,
        "metadata": {"total": len(entries), "generated": rand_ts(), "examiner": "DarkNode Forensics Lab", "case_count": 50}
    })


# ---------------------------------------------------------------------------
# 10. command-reference.json  (~12000 lines)
# ---------------------------------------------------------------------------
def gen_command_reference():
    print("Generating command-reference.json ...")
    cmd_categories = ["network", "exploitation", "reconnaissance", "forensics", "crypto",
                      "stealth", "system", "file", "process", "mesh", "vault", "darknode"]
    commands = []
    cmd_names = [
        "netscan", "portsweep", "vulnprobe", "exploitrun", "payloadgen", "shellbind",
        "reverseshell", "privesc", "credgrab", "hashcrack", "keylog", "screencap",
        "filedump", "regspy", "proclist", "procject", "dllload", "memread", "memscan",
        "disasm", "decompile", "hexedit", "binpatch", "cryptolock", "cryptounlock",
        "stegohide", "stegoreveal", "netsniff", "dnstunnel", "icmptunnel", "vpntunnel",
        "meshconnect", "meshroute", "meshbroadcast", "meshpeers", "vaultstore",
        "vaultretrieve", "vaultencrypt", "vaultdecrypt", "darknodescan", "darknodewatch",
        "darknodealert", "darknodeblock", "logwipe", "logforge", "timestomp",
        "rootinstall", "rootremove", "backdoorplant", "backdoorchecck", "pivotmap",
        "lateralmove", "exfildata", "c2connect", "c2beacon", "c2command",
        "opseccheck", "traceblock", "antidebug", "antivm", "antisandbox",
        "chainproxy", "torroute", "i2proute", "darkroute", "ghostmode",
        "decoynet", "honeytrap", "canarytoken", "tripwire", "alertengine",
        "bruteforce", "dictattack", "rainbowtable", "passthehash", "passtheticket",
        "kerberoast", "asreproast", "dcsync", "goldenticket", "silverticket",
        "mimidump", "lsassdump", "samdump", "ntdsdump", "adrecon",
        "bloodhound", "sharphound", "rubeus", "seatbelt", "winpeas",
        "linpeas", "pspy", "linenum", "lse", "suidenum",
        "webshell", "sqlmap", "xsstest", "ssrfprobe", "lfitest",
        "rfitest", "cmdinject", "deserialize", "jwtcrack", "apifuzz",
        "subdomenum", "dnsrecon", "whois", "shodan", "censys",
        "osintgather", "emailharvest", "phonesearch", "socialscan", "darkwebcrawl",
        "wifiscan", "wificrack", "wifijam", "bluetoothscan", "rfcapture",
        "firmextract", "firmanalyze", "iotscan", "scadaprobe", "plcattack",
        "cloudenum", "s3scan", "gcpaudit", "azurerecon", "containerbreak",
        "k8senum", "dockerescape", "cicdpoison", "supplychaincheck", "dependencyaudit",
        "malwareanalyze", "sandboxrun", "yarascan", "sigmacheck", "snortrule",
        "incidentlog", "timelinebuild", "evidencecollect", "reportgen", "briefing",
        "teamcomms", "missionbrief", "taskassign", "statusreport", "debrief",
        "encrypt", "decrypt", "sign", "verify", "keygenerate",
        "certrequest", "certvalidate", "pkimanage", "hsminit", "tpmextract",
        "perfmon", "benchmark", "stresstest", "loadtest", "fuzztest",
        "codeaudit", "staticanalysis", "dynamicanalysis", "tainttrack", "symbolicexec",
        "patchdiff", "bindiff", "funcmatch", "callgraph", "cfgextract",
        "aiassist", "mlclassify", "anomalydetect", "behaviormodel", "threatpredict",
        "quantumprep", "postquantum", "latticecrypto", "hashbased", "codebased",
        "blockchainmon", "txanalyze", "wallettrack", "smartaudit", "defiprobe",
        "abortscan", "cleantraces", "securedelete", "burnafter", "deadmanswitch",
        "sleepagent", "wakeagent", "heartbeat", "checkpulse", "gosilent",
        "darkping", "darktrace", "darksync", "darkstream", "darkvault",
        "noderegister", "nodedecommission", "nodehealth", "nodeupgrade", "nodemigrate",
        "clusterjoin", "clusterleave", "clusterstatus", "clusterbalance", "clusterfailover",
        "dbbackup", "dbrestore", "dbmigrate", "dbaudit", "dbencrypt",
        "apiregister", "apithrottle", "apimonitor", "apilog", "apirevoke",
        "useradd", "userdel", "usermod", "groupadd", "groupmod",
        "roleassign", "rolerevoke", "permcheck", "accessaudit", "sessionkill",
        "firewallup", "firewalldown", "firewallrule", "firewalllog", "firewallaudit",
        "vpnstart", "vpnstop", "vpnstatus", "vpnroute", "vpnkill",
        "torstart", "torstop", "torcircuit", "toridentity", "torbridges",
        "proxychains", "sockssetup", "httpproxy", "dnsmasq", "dnscrypt",
    ]
    for i in range(300):
        name = cmd_names[i] if i < len(cmd_names) else f"dncmd_{rand_hex(6)}"
        cat = random.choice(cmd_categories)
        num_opts = random.randint(5, 20)
        options = []
        used_short = set()
        for j in range(num_opts):
            short = None
            ch = random.choice(string.ascii_lowercase)
            if ch not in used_short:
                short = f"-{ch}"
                used_short.add(ch)
            opt_name = f"--{random.choice(['target','port','protocol','output','format','verbose','quiet','timeout','retry','threads','delay','proxy','interface','rate','depth','recursive','follow','force','dry-run','color','json','xml','csv','binary','hex','base64','encrypt','compress','silent','debug','trace','profile','config','input','filter','exclude','include','limit','offset','sort','reverse','unique','count','summary','raw','all','no-cache','no-verify','no-color','interactive','batch','parallel','sequential','random','ordered','append','overwrite','backup','restore','verify','checksum','hash','sign','encrypt-key','decrypt-key','passphrase','keyfile','certfile','cafile','cipher','digest','iterations','salt','iv','padding','encoding','charset','locale','timezone','timestamp','duration','interval','threshold','min','max','avg','percentile','deviation','variance','median','mode'])}-{rand_hex(3)}"
            options.append({
                "long": opt_name,
                "short": short,
                "type": random.choice(["string", "integer", "boolean", "float", "file", "ip", "port", "enum"]),
                "required": random.choice([True, False, False, False]),
                "default": random.choice([None, "auto", "0", "false", "stdout", "1000", "10"]),
                "description": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(30, 100)))}",
                "env_var": f"DN_{name.upper()}_{opt_name.replace('--','').replace('-','_').upper()[:20]}" if random.random() > 0.7 else None,
            })
        examples = []
        for _ in range(random.randint(3, 8)):
            examples.append({
                "title": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(15, 50)))}",
                "command": f"{name} {' '.join(random.choice(['--target ' + rand_ip(), '--port ' + str(rand_port()), '-v', '--output /tmp/result.json', '--threads 50', '--timeout 30', '--format json', '--proxy socks5://127.0.0.1:9050', '--recursive', '--depth 5']) for _ in range(random.randint(2, 6)))}",
                "output": f"{''.join(random.choices(string.ascii_lowercase + string.digits + ' .:->', k=random.randint(50, 200)))}",
                "notes": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(20, 80)))}",
            })
        man_sections = {
            "NAME": f"{name} - DarkNode OS {cat} utility",
            "SYNOPSIS": f"{name} [OPTIONS] [TARGET...]",
            "DESCRIPTION": f"{''.join(random.choices(string.ascii_lowercase + ' .,;:', k=random.randint(200, 600)))}",
            "OPTIONS": f"See options array for full details. {num_opts} options available.",
            "ENVIRONMENT": f"DN_{name.upper()}_HOME, DN_{name.upper()}_CONFIG, DN_{name.upper()}_LOG",
            "FILES": f"/etc/darknode/{name}.conf, ~/.darknode/{name}.rc, /var/log/darknode/{name}.log",
            "EXIT_STATUS": "0 on success, 1 on error, 2 on invalid arguments, 130 on interrupt",
            "EXAMPLES": f"See examples array for {len(examples)} usage examples.",
            "BUGS": f"Report bugs to darknode-bugs@{rand_domain()}",
            "AUTHOR": random.choice(HACKER_HANDLES),
            "SEE_ALSO": ", ".join(random.sample(cmd_names[:50], min(5, len(cmd_names[:50])))),
            "HISTORY": f"First released in DarkNode OS v{random.randint(1,4)}.{random.randint(0,9)}.0 ({random.randint(2020,2025)})",
            "SECURITY": f"Requires {'root' if random.random() > 0.5 else 'darknode-user'} privileges. {'Uses encrypted channels.' if random.random() > 0.3 else 'Plaintext mode available with --no-encrypt.'}",
        }
        cmd = {
            "id": f"CMD-{i+1:04d}",
            "name": name,
            "category": cat,
            "version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,99)}",
            "description": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(60, 200)))}",
            "syntax": f"{name} [options] <target>",
            "options": options,
            "examples": examples,
            "man_page": man_sections,
            "aliases": [f"{name[:3]}", f"dn-{name}"] if random.random() > 0.5 else [],
            "requires_root": random.choice([True, False]),
            "network_required": random.choice([True, True, False]),
            "platforms": random.sample(["linux", "windows", "macos", "freebsd", "darknode-os"], random.randint(1, 5)),
            "installed_by_default": random.choice([True, True, False]),
            "package": f"darknode-{cat}-tools",
            "dependencies": random.sample(cmd_names[:30], random.randint(0, 5)),
            "last_updated": rand_ts(),
        }
        commands.append(cmd)
    write_json(os.path.join(DATA_DIR, "command-reference.json"), {
        "commands": commands,
        "metadata": {"total": len(commands), "generated": rand_ts(), "version": "5.1.0"}
    })


# ---------------------------------------------------------------------------
# 11. themes.json  (~8000 lines)
# ---------------------------------------------------------------------------
def gen_themes():
    print("Generating themes.json ...")
    theme_names = [
        "Matrix Green", "Neon Cyber", "Void Black", "Blood Red", "Ice Blue",
        "Phantom Purple", "Solar Flare", "Deep Ocean", "Toxic Waste", "Chrome Silver",
        "Midnight Blue", "Ember Orange", "Ghost White", "Stealth Gray", "Acid Green",
        "Plasma Pink", "Quantum Violet", "Dark Matter", "Binary Gold", "Shadow Teal"
    ]
    themes = []
    for idx, tname in enumerate(theme_names):
        def rc():
            return f"#{rand_hex(6)}"
        def ra():
            return f"rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},{round(random.uniform(0.05,1.0),2)})"
        colors = {}
        # 50+ color variables
        prefixes = ["bg", "fg", "border", "accent", "primary", "secondary", "tertiary",
                     "success", "warning", "error", "info", "muted", "highlight", "selection",
                     "link", "visited", "hover", "active", "focus", "disabled",
                     "header", "sidebar", "panel", "card", "modal", "tooltip", "dropdown",
                     "input", "button", "badge", "tag", "tab", "menu", "nav",
                     "scrollbar", "shadow", "glow", "gradient-start", "gradient-end",
                     "terminal-bg", "terminal-fg", "terminal-cursor", "terminal-selection",
                     "terminal-black", "terminal-red", "terminal-green", "terminal-yellow",
                     "terminal-blue", "terminal-magenta", "terminal-cyan", "terminal-white",
                     "terminal-bright-black", "terminal-bright-red", "terminal-bright-green",
                     "terminal-bright-yellow", "terminal-bright-blue", "terminal-bright-magenta",
                     "terminal-bright-cyan", "terminal-bright-white",
                     "syntax-keyword", "syntax-string", "syntax-number", "syntax-comment",
                     "syntax-function", "syntax-variable", "syntax-operator", "syntax-type",
                     "syntax-constant", "syntax-tag", "syntax-attribute", "syntax-property",
                     "chart-1", "chart-2", "chart-3", "chart-4", "chart-5", "chart-6",
                     "chart-7", "chart-8", "chart-9", "chart-10",
                     "status-online", "status-away", "status-busy", "status-offline",
                     "threat-critical", "threat-high", "threat-medium", "threat-low",
                     "network-node", "network-edge", "network-active", "network-inactive",
                     "scan-progress", "scan-complete", "scan-error"]
        for p in prefixes:
            colors[p] = rc()
            colors[f"{p}-alpha"] = ra()

        typography = {
            "font-family-primary": random.choice(["'JetBrains Mono', monospace", "'Fira Code', monospace",
                                                    "'Hack', monospace", "'Source Code Pro', monospace"]),
            "font-family-secondary": random.choice(["'Inter', sans-serif", "'Roboto', sans-serif",
                                                      "'Space Grotesk', sans-serif"]),
            "font-size-xs": f"{random.choice([10,11,12])}px",
            "font-size-sm": f"{random.choice([12,13,14])}px",
            "font-size-md": f"{random.choice([14,15,16])}px",
            "font-size-lg": f"{random.choice([18,20,22])}px",
            "font-size-xl": f"{random.choice([24,28,32])}px",
            "font-size-xxl": f"{random.choice([36,42,48])}px",
            "font-weight-normal": random.choice([300, 400]),
            "font-weight-medium": random.choice([500, 600]),
            "font-weight-bold": random.choice([700, 800]),
            "line-height-tight": random.choice([1.2, 1.25]),
            "line-height-normal": random.choice([1.4, 1.5, 1.6]),
            "line-height-loose": random.choice([1.8, 2.0]),
            "letter-spacing-tight": "-0.02em",
            "letter-spacing-normal": "0em",
            "letter-spacing-wide": "0.05em",
        }
        spacing = {f"space-{n}": f"{n * random.choice([4,8])}px" for n in range(13)}
        borders = {
            "border-width-thin": "1px",
            "border-width-medium": "2px",
            "border-width-thick": "3px",
            "border-radius-sm": f"{random.choice([2,3,4])}px",
            "border-radius-md": f"{random.choice([6,8])}px",
            "border-radius-lg": f"{random.choice([12,16])}px",
            "border-radius-full": "9999px",
            "border-style": random.choice(["solid", "dashed", "dotted"]),
        }
        shadows = {
            "shadow-sm": f"0 1px 2px {ra()}",
            "shadow-md": f"0 4px 6px {ra()}",
            "shadow-lg": f"0 10px 15px {ra()}",
            "shadow-xl": f"0 20px 25px {ra()}",
            "shadow-glow": f"0 0 20px {rc()}",
            "shadow-neon": f"0 0 10px {rc()}, 0 0 20px {rc()}, 0 0 40px {rc()}",
            "shadow-inner": f"inset 0 2px 4px {ra()}",
        }
        animations = {
            "transition-fast": f"{random.choice([100,150])}ms ease",
            "transition-normal": f"{random.choice([200,250,300])}ms ease",
            "transition-slow": f"{random.choice([400,500])}ms ease",
            "animation-pulse": f"pulse {random.choice([1,1.5,2])}s infinite",
            "animation-glow": f"glow {random.choice([2,3])}s infinite alternate",
            "animation-scan": f"scan {random.choice([3,5,8])}s linear infinite",
            "animation-flicker": f"flicker {round(random.uniform(0.1,0.5),1)}s infinite",
            "animation-matrix-rain": f"matrix-rain {random.randint(5,20)}s linear infinite",
        }
        effects = {
            "blur-sm": "blur(4px)",
            "blur-md": "blur(8px)",
            "blur-lg": "blur(16px)",
            "backdrop-blur": f"blur({random.choice([8,12,16])}px)",
            "noise-opacity": round(random.uniform(0.02, 0.1), 3),
            "scanline-opacity": round(random.uniform(0.02, 0.08), 3),
            "crt-curvature": round(random.uniform(0, 0.05), 3),
            "glitch-intensity": round(random.uniform(0, 1), 2),
            "chromatic-aberration": f"{round(random.uniform(0, 3), 1)}px",
        }

        theme = {
            "id": f"THEME-{idx+1:03d}",
            "name": tname,
            "slug": tname.lower().replace(" ", "-"),
            "author": random.choice(HACKER_HANDLES),
            "version": f"{random.randint(1,3)}.{random.randint(0,9)}.{random.randint(0,15)}",
            "description": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(60, 150)))}",
            "dark_mode": True,
            "high_contrast": random.choice([True, False]),
            "colors": colors,
            "typography": typography,
            "spacing": spacing,
            "borders": borders,
            "shadows": shadows,
            "animations": animations,
            "effects": effects,
            "breakpoints": {"sm": "640px", "md": "768px", "lg": "1024px", "xl": "1280px", "xxl": "1536px"},
            "z_index": {"dropdown": 1000, "sticky": 1020, "fixed": 1030, "modal_backdrop": 1040,
                        "modal": 1050, "popover": 1060, "tooltip": 1070, "toast": 1080},
            "custom_properties": {f"--dn-{rand_hex(6)}": rc() for _ in range(random.randint(10, 25))},
            "created": rand_ts(random.randint(2023, 2025)),
            "updated": rand_ts(),
        }
        themes.append(theme)
    write_json(os.path.join(CONFIG_DIR, "themes.json"), {
        "themes": themes,
        "metadata": {"total": len(themes), "generated": rand_ts(), "default_theme": "THEME-001"}
    })


# ---------------------------------------------------------------------------
# 12. keybindings.json  (~6000 lines)
# ---------------------------------------------------------------------------
def gen_keybindings():
    print("Generating keybindings.json ...")
    contexts = ["global", "terminal", "editor", "file-manager", "network-map",
                "exploit-panel", "threat-feed", "log-viewer", "packet-inspector",
                "settings", "dashboard", "modal", "command-palette"]
    mods = ["Ctrl", "Alt", "Shift", "Meta", "Ctrl+Shift", "Ctrl+Alt", "Alt+Shift"]
    keys = list(string.ascii_uppercase) + [f"F{n}" for n in range(1, 13)] + \
           ["Enter", "Escape", "Tab", "Space", "Backspace", "Delete", "Insert",
            "Home", "End", "PageUp", "PageDown", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
            "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/"]
    bindings = []
    for i in range(500):
        ctx = random.choice(contexts)
        mod = random.choice(mods)
        key = random.choice(keys)
        binding = {
            "id": f"KB-{i+1:04d}",
            "context": ctx,
            "key": f"{mod}+{key}",
            "command": f"{ctx.replace('-','_')}.{random.choice(['open','close','toggle','run','stop','next','prev','search','filter','sort','copy','paste','delete','save','load','refresh','zoom_in','zoom_out','reset','focus','blur','select_all','clear','submit','cancel','undo','redo','expand','collapse'])}_{rand_hex(4)}",
            "description": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(20, 80)))}",
            "category": random.choice(["navigation", "editing", "view", "tools", "system", "debug"]),
            "when": f"{ctx}.isActive && !modal.isOpen" if random.random() > 0.3 else f"{ctx}.isActive",
            "default": True,
            "customizable": random.choice([True, True, True, False]),
            "os_override": {
                "macos": f"Cmd+{key}" if "Ctrl" in mod else None,
                "linux": None,
                "windows": None,
            },
        }
        bindings.append(binding)
    write_json(os.path.join(CONFIG_DIR, "keybindings.json"), {
        "keybindings": bindings,
        "metadata": {"total": len(bindings), "generated": rand_ts(), "version": "2.1.0"}
    })


# ---------------------------------------------------------------------------
# 13. permissions.json  (~8000 lines)
# ---------------------------------------------------------------------------
def gen_permissions():
    print("Generating permissions.json ...")
    resources = ["exploits", "network", "threats", "logs", "users", "malware", "scans",
                 "packets", "forensics", "commands", "themes", "keybindings", "permissions",
                 "services", "firewall", "vault", "mesh", "darknode", "crypto", "api"]
    actions = ["create", "read", "update", "delete", "execute", "export", "import",
               "admin", "audit", "share"]
    perms = []
    for res in resources:
        for act in actions:
            perms.append({
                "id": f"PERM-{res.upper()}-{act.upper()}",
                "resource": res,
                "action": act,
                "description": f"{act.capitalize()} access to {res} resource",
                "risk_level": random.choice(["low", "medium", "high", "critical"]),
                "requires_mfa": random.choice([True, False, False]),
                "audit_log": True,
                "rate_limit": random.choice([None, "100/min", "1000/hour", "10000/day"]),
            })

    role_names = [
        "root", "admin", "security_analyst", "threat_hunter", "incident_responder",
        "forensic_examiner", "penetration_tester", "malware_analyst", "network_engineer",
        "soc_analyst_l1", "soc_analyst_l2", "soc_analyst_l3", "vulnerability_manager",
        "compliance_officer", "audit_reviewer", "developer", "devops_engineer",
        "system_administrator", "database_admin", "cloud_architect",
        "red_team_lead", "blue_team_lead", "purple_team_member", "ciso",
        "guest", "read_only", "api_service", "automated_scanner",
        "training_user", "contractor"
    ]
    roles = []
    for rname in role_names:
        if rname == "root":
            granted = [p["id"] for p in perms]
        elif rname in ("admin", "ciso"):
            granted = [p["id"] for p in perms if random.random() > 0.05]
        elif rname in ("guest", "read_only"):
            granted = [p["id"] for p in perms if p["action"] == "read" and random.random() > 0.3]
        else:
            granted = [p["id"] for p in perms if random.random() > 0.5]

        inherits = []
        if rname not in ("root", "guest"):
            inherits = random.sample([r for r in role_names if r != rname and r != "root"],
                                     random.randint(0, 3))

        constraints = {
            "ip_whitelist": [rand_ip() for _ in range(random.randint(0, 5))] if random.random() > 0.5 else [],
            "time_restriction": random.choice([None, "business_hours", "24x7", "weekdays_only"]),
            "max_sessions": random.randint(1, 50),
            "session_timeout_min": random.choice([15, 30, 60, 120, 480, 1440]),
            "password_policy": {
                "min_length": random.choice([8, 12, 16, 20]),
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": random.choice([True, False]),
                "max_age_days": random.choice([30, 60, 90, 180, 365]),
                "history_count": random.choice([5, 10, 24]),
                "lockout_attempts": random.choice([3, 5, 10]),
                "lockout_duration_min": random.choice([15, 30, 60]),
            },
            "mfa_required": random.choice([True, True, False]),
            "mfa_methods": random.sample(["totp", "webauthn", "sms", "email", "hardware_key"], random.randint(1, 3)),
            "allowed_environments": random.sample(["production", "staging", "development", "darknet"], random.randint(1, 4)),
        }

        role = {
            "name": rname,
            "display_name": rname.replace("_", " ").title(),
            "description": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(40, 120)))}",
            "level": random.randint(0, 100),
            "permissions_granted": granted,
            "permissions_denied": [p["id"] for p in random.sample(perms, random.randint(0, 10))],
            "inherits_from": inherits,
            "constraints": constraints,
            "created": rand_ts(2023),
            "updated": rand_ts(),
            "created_by": "root",
            "active": True,
        }
        roles.append(role)

    write_json(os.path.join(CONFIG_DIR, "permissions.json"), {
        "permissions": perms,
        "roles": roles,
        "metadata": {"total_permissions": len(perms), "total_roles": len(roles), "generated": rand_ts(), "rbac_version": "3.0.0"}
    })


# ---------------------------------------------------------------------------
# 14. services.json  (~8000 lines)
# ---------------------------------------------------------------------------
def gen_services():
    print("Generating services.json ...")
    service_defs = [
        ("darknode-core", "Core system orchestrator"),
        ("darknode-darknode", "Security monitoring daemon"),
        ("darknode-nexus", "Mesh network coordinator"),
        ("darknode-vault", "Encrypted data store"),
        ("darknode-proxy", "Network proxy service"),
        ("darknode-scanner", "Vulnerability scanner engine"),
        ("darknode-crypto", "Cryptographic operations service"),
        ("darknode-mesh", "Peer-to-peer mesh network"),
        ("darknode-api", "REST API gateway"),
        ("darknode-web", "Web interface server"),
        ("darknode-auth", "Authentication service"),
        ("darknode-dns", "DNS resolver and cache"),
        ("darknode-log", "Centralized logging service"),
        ("darknode-metrics", "Metrics collection and aggregation"),
        ("darknode-alert", "Alert management and notification"),
        ("darknode-backup", "Automated backup service"),
        ("darknode-sync", "Data synchronization service"),
        ("darknode-queue", "Message queue service"),
        ("darknode-cache", "Distributed cache layer"),
        ("darknode-search", "Full-text search engine"),
        ("darknode-ml", "Machine learning inference engine"),
        ("darknode-sandbox", "Malware sandboxing service"),
        ("darknode-forensics", "Digital forensics toolkit"),
        ("darknode-c2", "Command and control framework"),
        ("darknode-recon", "Reconnaissance automation"),
        ("darknode-exploit", "Exploit management framework"),
        ("darknode-phish", "Phishing simulation platform"),
        ("darknode-cti", "Cyber threat intelligence platform"),
        ("darknode-siem", "Security information event management"),
        ("darknode-soar", "Security orchestration and response"),
        ("darknode-edr", "Endpoint detection and response"),
        ("darknode-ndr", "Network detection and response"),
        ("darknode-xdr", "Extended detection and response"),
        ("darknode-asm", "Attack surface management"),
        ("darknode-vm", "Vulnerability management"),
        ("darknode-grc", "Governance risk compliance"),
        ("darknode-pam", "Privileged access management"),
        ("darknode-iam", "Identity and access management"),
        ("darknode-dlp", "Data loss prevention"),
        ("darknode-casb", "Cloud access security broker"),
    ]
    # Pad to 100
    while len(service_defs) < 100:
        n = len(service_defs)
        service_defs.append((f"darknode-svc-{n:03d}", f"DarkNode auxiliary service {n}"))

    services = []
    all_svc_names = [s[0] for s in service_defs]
    for idx, (sname, sdesc) in enumerate(service_defs):
        port = 8000 + idx
        health_checks = []
        for _ in range(random.randint(1, 4)):
            health_checks.append({
                "type": random.choice(["http", "tcp", "exec", "grpc"]),
                "endpoint": f"http://localhost:{port}/health" if random.random() > 0.3 else f"tcp://localhost:{port}",
                "interval_sec": random.choice([5, 10, 15, 30, 60]),
                "timeout_sec": random.choice([3, 5, 10]),
                "retries": random.choice([3, 5, 10]),
                "success_threshold": random.choice([1, 2, 3]),
                "failure_threshold": random.choice([3, 5, 10]),
                "expected_status": 200 if random.random() > 0.3 else random.choice([200, 204]),
                "expected_body": random.choice([None, '{"status":"ok"}', '{"healthy":true}']),
            })
        deps = random.sample([s for s in all_svc_names if s != sname], random.randint(0, 8))
        env_vars = {}
        for _ in range(random.randint(3, 15)):
            key = f"DN_{sname.upper().replace('-','_')}_{random.choice(['PORT','HOST','DB','SECRET','KEY','LOG_LEVEL','TIMEOUT','WORKERS','MAX_CONN','CACHE_TTL','RETRY','DEBUG'])}_{rand_hex(3).upper()}"
            env_vars[key] = random.choice([str(random.randint(1, 65535)), rand_hex(32), "true", "false",
                                            "info", "debug", "/var/log/darknode", rand_ip()])
        volumes = []
        for _ in range(random.randint(1, 5)):
            volumes.append({
                "host": f"/opt/darknode/{sname}/{random.choice(['data','config','logs','certs','keys'])}",
                "container": f"/app/{random.choice(['data','config','logs','certs','keys'])}",
                "mode": random.choice(["rw", "ro"]),
                "type": random.choice(["bind", "volume", "tmpfs"]),
            })
        resource_limits = {
            "cpu_cores": random.choice([0.5, 1, 2, 4, 8]),
            "memory_mb": random.choice([128, 256, 512, 1024, 2048, 4096]),
            "memory_swap_mb": random.choice([256, 512, 1024, 2048, 4096, 8192]),
            "pids_limit": random.choice([100, 500, 1000, 5000]),
            "ulimits": {
                "nofile": {"soft": 65536, "hard": 65536},
                "nproc": {"soft": 4096, "hard": 8192},
            },
            "network_bandwidth_mbps": random.choice([100, 1000, 10000]),
            "storage_quota_gb": random.choice([1, 5, 10, 50, 100, 500]),
        }
        svc = {
            "id": f"SVC-{idx+1:04d}",
            "name": sname,
            "description": sdesc,
            "version": f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,99)}",
            "type": random.choice(["daemon", "oneshot", "timer", "socket"]),
            "status": random.choice(["running", "running", "running", "stopped", "failed", "disabled"]),
            "enabled": random.choice([True, True, True, False]),
            "port": port,
            "protocol": random.choice(["TCP", "UDP", "gRPC", "WebSocket"]),
            "bind_address": random.choice(["0.0.0.0", "127.0.0.1", "::"]),
            "dependencies": deps,
            "health_checks": health_checks,
            "restart_policy": {
                "type": random.choice(["always", "on-failure", "unless-stopped", "no"]),
                "max_retries": random.choice([3, 5, 10, -1]),
                "delay_sec": random.choice([1, 5, 10, 30]),
                "backoff_multiplier": random.choice([1, 1.5, 2, 3]),
                "max_delay_sec": random.choice([60, 300, 900]),
            },
            "logging": {
                "driver": random.choice(["json-file", "syslog", "journald", "fluentd"]),
                "level": random.choice(["debug", "info", "warning", "error"]),
                "max_size": random.choice(["10m", "50m", "100m", "500m"]),
                "max_files": random.choice([3, 5, 10, 20]),
                "format": random.choice(["json", "text", "logfmt"]),
                "output": f"/var/log/darknode/{sname}.log",
            },
            "environment": env_vars,
            "volumes": volumes,
            "resources": resource_limits,
            "security": {
                "user": random.choice(["darknode", "root", "nobody", f"{sname}-user"]),
                "group": random.choice(["darknode", "root", "nogroup"]),
                "capabilities_add": random.sample(["NET_ADMIN", "SYS_ADMIN", "NET_RAW", "SYS_PTRACE",
                                                     "DAC_OVERRIDE", "CHOWN", "SETUID", "SETGID"], random.randint(0, 3)),
                "capabilities_drop": ["ALL"] if random.random() > 0.3 else [],
                "read_only_rootfs": random.choice([True, False]),
                "no_new_privileges": random.choice([True, True, False]),
                "seccomp_profile": random.choice(["default", "custom", "unconfined"]),
                "apparmor_profile": random.choice(["darknode-default", "unconfined"]),
            },
            "metadata": {
                "labels": {f"app.darknode.io/{k}": v for k, v in
                           [("component", sname), ("version", f"{random.randint(1,5)}.{random.randint(0,9)}"),
                            ("tier", random.choice(["core", "auxiliary", "monitoring", "security"])),
                            ("team", random.choice(["platform", "security", "infra", "ops"]))]},
                "annotations": {f"darknode.io/{rand_hex(8)}": rand_hex(16) for _ in range(random.randint(1, 5))},
                "created": rand_ts(2023),
                "updated": rand_ts(),
            },
        }
        services.append(svc)
    write_json(os.path.join(CONFIG_DIR, "services.json"), {
        "services": services,
        "metadata": {"total": len(services), "generated": rand_ts(), "platform_version": "5.0.0"}
    })


# ---------------------------------------------------------------------------
# 15. firewall-rules.json  (~6000 lines)
# ---------------------------------------------------------------------------
def gen_firewall_rules():
    print("Generating firewall-rules.json ...")
    chains = ["INPUT", "OUTPUT", "FORWARD", "DARKNODE_IN", "DARKNODE_OUT",
              "DARKNODE_FWD", "MESH_FILTER", "DARKNODE_BLOCK", "HONEYPOT_REDIRECT"]
    actions = ["ACCEPT", "DROP", "REJECT", "LOG", "REDIRECT", "SNAT", "DNAT", "MARK", "QUEUE"]
    rules = []
    for i in range(300):
        proto = random.choice(["tcp", "udp", "icmp", "all", "gre", "esp", "ah"])
        src = random.choice([rand_ip(), f"{rand_ip()}/24", f"{rand_ip()}/16", "0.0.0.0/0", "any"])
        dst = random.choice([rand_ip(), f"{rand_ip()}/24", f"{rand_ip()}/16", "0.0.0.0/0", "any"])
        sport = random.choice([None, str(rand_port()), f"{random.randint(1024,60000)}:{random.randint(60001,65535)}"])
        dport = random.choice([None, str(rand_port()), f"{random.randint(1,1024)}"])
        action = random.choice(actions)
        rule = {
            "id": f"FW-{i+1:04d}",
            "chain": random.choice(chains),
            "table": random.choice(["filter", "nat", "mangle", "raw"]),
            "priority": random.randint(1, 10000),
            "protocol": proto,
            "source": src,
            "destination": dst,
            "source_port": sport,
            "destination_port": dport,
            "action": action,
            "direction": random.choice(["inbound", "outbound", "forward"]),
            "interface_in": random.choice([None, "eth0", "eth1", "wlan0", "tun0", "br0"]),
            "interface_out": random.choice([None, "eth0", "eth1", "wlan0", "tun0", "br0"]),
            "state": random.choice([None, "NEW", "ESTABLISHED", "RELATED", "INVALID",
                                     "NEW,ESTABLISHED", "ESTABLISHED,RELATED"]),
            "flags": random.choice([None, "SYN", "SYN,ACK", "FIN", "RST"]) if proto == "tcp" else None,
            "icmp_type": random.choice([None, "echo-request", "echo-reply", "destination-unreachable",
                                         "time-exceeded"]) if proto == "icmp" else None,
            "rate_limit": {
                "enabled": random.choice([True, False, False]),
                "rate": f"{random.randint(1,100)}/{random.choice(['second','minute','hour'])}",
                "burst": random.randint(1, 50),
            } if random.random() > 0.5 else None,
            "logging": {
                "enabled": random.choice([True, True, False]),
                "prefix": f"[DN-FW-{i+1:04d}] " if random.random() > 0.3 else None,
                "level": random.choice(["debug", "info", "notice", "warning", "error"]),
                "limit": f"{random.randint(1,10)}/min" if random.random() > 0.5 else None,
            },
            "comment": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(20, 80)))}",
            "enabled": random.choice([True, True, True, False]),
            "created": rand_ts(2024),
            "updated": rand_ts(),
            "created_by": random.choice(["root", "admin", "firewall-manager", random.choice(HACKER_HANDLES)]),
            "hit_count": random.randint(0, 10**8),
            "last_hit": rand_ts() if random.random() > 0.2 else None,
            "expires": rand_ts() if random.random() > 0.8 else None,
            "tags": random.sample(["critical", "monitoring", "mesh", "external", "internal",
                                    "dmz", "management", "temporary", "auto-generated"], random.randint(1, 4)),
            "geo_filter": {
                "enabled": random.choice([True, False, False]),
                "countries_blocked": random.sample(["CN", "RU", "KP", "IR", "SY", "CU", "VE"],
                                                    random.randint(0, 4)) if random.random() > 0.5 else [],
                "countries_allowed": [] if random.random() > 0.3 else random.sample(["US", "GB", "DE", "JP", "AU"],
                                                                                      random.randint(1, 3)),
            } if random.random() > 0.6 else None,
        }
        rules.append(rule)

    zone_defs = []
    zone_names = ["external", "internal", "dmz", "management", "mesh", "honeypot", "quarantine", "guest"]
    for zname in zone_names:
        zone_defs.append({
            "name": zname,
            "interfaces": random.sample(["eth0", "eth1", "eth2", "wlan0", "br0", "tun0", "veth0"], random.randint(1, 3)),
            "default_action": random.choice(["DROP", "REJECT", "ACCEPT"]),
            "description": f"{''.join(random.choices(string.ascii_lowercase + ' ', k=random.randint(20, 60)))}",
            "rules_applied": random.randint(5, 50),
        })

    write_json(os.path.join(CONFIG_DIR, "firewall-rules.json"), {
        "firewall": {
            "rules": rules,
            "zones": zone_defs,
            "default_policies": {
                "input": "DROP",
                "output": "ACCEPT",
                "forward": "DROP",
            },
            "global_settings": {
                "connection_tracking": True,
                "syn_cookies": True,
                "rp_filter": True,
                "log_martians": True,
                "icmp_rate_limit": "10/second",
                "established_timeout": 432000,
                "syn_timeout": 60,
                "fin_timeout": 30,
            },
        },
        "metadata": {"total_rules": len(rules), "total_zones": len(zone_defs), "generated": rand_ts(), "version": "4.0.0"}
    })


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("  DarkNode OS — Data & Config Generator")
    print("=" * 60)
    print()

    gen_exploits_db()
    gen_network_topology()
    gen_threat_intel()
    gen_system_logs()
    gen_user_profiles()
    gen_malware_signatures()
    gen_vulnerability_scan()
    gen_packet_captures()
    gen_forensics_artifacts()
    gen_command_reference()
    gen_themes()
    gen_keybindings()
    gen_permissions()
    gen_services()
    gen_firewall_rules()

    print()
    print("=" * 60)
    print("  Generation complete!")
    print("=" * 60)
