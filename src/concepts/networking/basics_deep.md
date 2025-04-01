### Networking Concepts (In-Depth)

#### Basic Networking Concepts (Expanded)

1. **OSI Model**:
   - **Layer-by-Layer Mechanics**:
     - **Physical**: Bit-level transmission (e.g., 10GBASE-T over Cat6 cables). Signal modulation, encoding (NRZ, Manchester).
     - **Data Link**: Frames with headers (e.g., Ethernet: preamble, destination/source MAC, EtherType). Error detection via CRC. Protocols like ARP map IPs to MACs.
     - **Network**: IP packet structure (header with TTL, source/dest IP). Fragmentation if MTU exceeded. ICMP for diagnostics (e.g., ping).
     - **Transport**: TCP header includes sequence numbers, ACKs, window size for flow control. Congestion control (e.g., TCP Reno, Cubic). UDP: minimalist, no retransmission.
     - **Session**: Manages logical connections (e.g., NetBIOS). Rarely isolated in modern stacks.
     - **Presentation**: Handles data translation (e.g., JPEG encoding, SSL/TLS encryption). MIME types in email.
     - **Application**: Protocols like HTTP (REST APIs), SMTP, FTP. Often includes middleware (e.g., gRPC).
   - **Real-World**: In a cloud VPC, Layer 3 (IP routing) and Layer 4 (TCP/UDP) dominate, but Aviatrix’s overlay might abstract lower layers.

2. **IP Addressing**:
   - **IPv4 Details**: 32-bit address space (~4.3B addresses). CIDR notation (e.g., /24 = 255.255.255.0 mask). Exhaustion led to NAT and IPv6.
   - **IPv6 Details**: 128-bit, hex notation (e.g., 2001:0db8:85a3::8a2e:0370:7334). No NAT needed due to vast space. Stateless Address Autoconfiguration (SLAAC).
   - **Subnetting Math**: /24 → 256 IPs, /25 → 128 IPs (2^(32-n)). First/last reserved (network/broadcast). Example: 192.168.1.0/25 → 192.168.1.0–127.
   - **Cloud Context**: AWS VPC CIDR (e.g., 10.0.0.0/16) split into subnets (e.g., 10.0.1.0/24). Aviatrix manages cross-VPC/CIDR routing.

3. **TCP vs. UDP**:
   - **TCP Deep Dive**: 3-way handshake ensures reliability. Slow-start, congestion avoidance (e.g., drops window size on packet loss). Retransmission via timeouts (RTO). Header: 20 bytes (options extra).
   - **UDP Deep Dive**: 8-byte header (source/dest port, length, checksum). No ordering, no flow control—ideal for DNS (53), RTP (VoIP). QUIC (UDP-based) adds reliability for HTTP/3.
   - **Use Case**: Aviatrix might use TCP for control plane (reliable config sync) and UDP for high-speed data plane.

4. **Routing and Switching**:
   - **Switching**: MAC learning via flooding, then forwarding table. VLANs (802.1Q) tag frames for segmentation. Spanning Tree Protocol (STP) prevents loops.
   - **Routing**: Longest prefix match in routing tables (e.g., 10.0.0.0/16 over 10.0.0.0/8). Static vs. dynamic (OSPF, BGP). ECMP (Equal-Cost Multi-Path) for load balancing.
   - **Cloud**: AWS Route Tables vs. Aviatrix’s centralized routing control.

5. **DNS**:
   - **Resolution Flow**: Recursive resolver queries root (.), TLD (.com), then authoritative NS. Caching reduces latency (TTL-based).
   - **Records**: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), SRV (service).
   - **Security**: DNSSEC signs records to prevent spoofing. Aviatrix might integrate DNS filtering in its security stack.

#### Above-Average Networking Concepts (Expanded)

1. **Software-Defined Networking (SDN)**:
   - **Architecture**: Control plane (e.g., OpenFlow controller) programs data plane (switches/routers) via APIs. Southbound (OpenFlow, NETCONF), Northbound (REST APIs).
   - **Benefits**: Dynamic traffic engineering, policy-based routing. Scales via abstraction.
   - **Aviatrix**: Uses SDN to create a unified control plane across AWS, Azure, GCP—e.g., managing transit gateways programmatically.

2. **Virtual Private Cloud (VPC)**:
   - **Components**: Subnets (public/private), Route Tables (e.g., 0.0.0.0/0 → IGW), Security Groups (stateful rules), NACLs (stateless ACLs).
   - **Peering**: VPC-to-VPC via private IPs (no overlap allowed). Transit Gateway scales this.
   - **Aviatrix**: Extends VPCs with a transit hub, enabling multi-region/cloud routing with BGP.

3. **Overlay vs. Underlay Networks**:
   - **Underlay**: Physical topology (e.g., ISP backbone). Protocols like MPLS, IS-IS.
   - **Overlay**: Virtual tunnels (e.g., VXLAN: UDP encapsulation, 24-bit VNID for 16M segments). GRE (IP-in-IP), IPsec (encrypted tunnels).
   - **Aviatrix**: Builds overlays for secure, scalable connectivity—e.g., VXLAN over public internet between clouds.

4. **BGP (Border Gateway Protocol)**:
   - **Mechanics**: Path-vector protocol. Advertises AS paths (e.g., AS1→AS2→AS3). Attributes: Local Preference (internal), MED (external hint), AS Path (loop prevention).
   - **States**: Idle → Connect → Active → OpenSent → OpenConfirm → Established.
   - **Cloud Use**: Aviatrix leverages eBGP for multi-cloud peering, ensuring optimal path selection.

5. **Load Balancing**:
   - **Layer 4**: IP/Port-based (e.g., HAProxy). Algorithms: Round-robin, least connections.
   - **Layer 7**: Content-aware (e.g., NGINX). Sticky sessions via cookies, URL rewriting.
   - **Cloud**: AWS ALB (app-level), NLB (TCP/UDP). Aviatrix offers distributed LB for multi-cloud.

6. **Network Address Translation (NAT)**:
   - **SNAT**: Rewrites source IP (e.g., private 10.0.0.5 → public 54.1.2.3).
   - **DNAT**: Rewrites destination IP (e.g., public 54.1.2.3 → private 10.0.0.5).
   - **PAT (Port Address Translation)**: Maps multiple private IPs to one public IP using ports.
   - **Cloud**: AWS NAT Gateway hides private subnet IPs. Aviatrix might optimize NAT for egress traffic.

---

### Security Concepts (In-Depth)

#### Basic Security Concepts (Expanded)

1. **Firewalls**:
   - **Stateless**: Rule per packet (e.g., “allow TCP 80”). No connection tracking—fast but limited.
   - **Stateful**: Tracks sessions (e.g., “allow reply to outbound 80”). Drops unsolicited inbound.
   - **NGFW**: Adds DPI (Deep Packet Inspection), app awareness (e.g., Palo Alto identifies Zoom traffic).

2. **Encryption**:
   - **Symmetric**: AES-256 (block cipher, 256-bit key). Modes: CBC (chaining), GCM (auth+encrypt). Fast, but key exchange is tricky.
   - **Asymmetric**: RSA (2048-bit keys), ECC (faster, smaller keys). Diffie-Hellman for key exchange.
   - **TLS**: Handshake (client hello, server cert, key exchange), then AES for data. Cipher suites (e.g., TLS_AES_256_GCM_SHA384).

3. **Authentication and Authorization**:
   - **AuthN**: OAuth 2.0 (tokens), SAML (XML-based SSO), Kerberos (ticket-based).
   - **AuthZ**: RBAC (roles), ABAC (attributes, e.g., “allow if dept=IT and time=9-5”).
   - **MFA**: TOTP (e.g., Google Authenticator), push notifications.

4. **VPN (Virtual Private Network)**:
   - **IPsec**: AH (auth only), ESP (encrypt+auth). IKE (Internet Key Exchange) negotiates SAs (Security Associations).
   - **OpenVPN**: SSL-based, user-space. Tun (L3) vs. Tap (L2) modes.
   - **Cloud**: Site-to-site VPN between on-prem and VPC.

5. **Threats**:
   - **DDoS**: Volumetric (flood bandwidth), Protocol (SYN flood), App-layer (HTTP flood).
   - **MitM**: ARP spoofing, DNS hijacking. Mitigated by TLS, HSTS.
   - **Phishing**: Spear (targeted), Whaling (executives). DMARC/SPF/DKIM for email.

#### Above-Average Security Concepts (Expanded)

1. **Zero Trust Architecture**:
   - **Core**: “Never trust, always verify.” No implicit trust based on location (e.g., inside VPC).
   - **Tech**: Microsegmentation (limit lateral movement), Identity-aware proxies (e.g., BeyondCorp), continuous monitoring.
   - **Aviatrix**: Enforces Zero Trust with policy-driven access across clouds.

2. **Network Segmentation**:
   - **Techniques**: VLANs, subnets, firewalls. In cloud: Security Groups (per instance), NACLs (per subnet).
   - **Microsegmentation**: Granular, per-workload policies (e.g., VM1 talks to VM2 on 443 only).
   - **Aviatrix**: Dynamic segmentation across multi-cloud via its controller.

3. **IPsec**:
   - **Phases**: IKEv1 (Phase 1: ISAKMP SA, Phase 2: IPsec SA) vs. IKEv2 (simplified).
   - **Crypto**: AES-GCM, SHA-256 HMAC. Lifetime renegotiation (e.g., 24h).
   - **Cloud**: Secures Aviatrix transit gateways over public internet.

4. **Intrusion Detection/Prevention Systems (IDS/IPS)**:
   - **IDS**: Signature-based (known attacks) vs. Anomaly-based (stats deviation). Snort rules (e.g., “alert tcp any any -> any 23”).
   - **IPS**: Inline blocking (e.g., drop malformed packets). Suricata with multi-threading.
   - **Cloud**: AWS GuardDuty (IDS), Aviatrix integrates with NGFW partners.

5. **Cloud Security Posture Management (CSPM)**:
   - **Checks**: IAM over-permissions, public S3 buckets, unencrypted EBS.
   - **Tools**: Prisma Cloud, AWS Config. Aviatrix adds network-layer visibility (e.g., misconfigured routes).
   - **Process**: Continuous scanning, remediation workflows.

6. **Secure Access Service Edge (SASE)**:
   - **Components**: SD-WAN (optimized routing), FWaaS (firewall-as-a-service), ZTNA (Zero Trust Network Access), CASB (cloud app security).
   - **Architecture**: Edge-deployed (POPs), cloud-native. Reduces latency vs. backhauling to HQ.
   - **Aviatrix**: SASE-like with multi-cloud transit, secure egress, and policy enforcement.

---

### Aviatrix Tie-In
- **Multi-Cloud Networking**: BGP for route propagation, overlays for connectivity, transit hubs for scale.
- **Security**: Zero Trust policies, IPsec tunnels, integration with NGFWs.
- **Interview Angle**: “Aviatrix’s controller abstracts VPC complexity, using SDN to enforce segmentation and secure traffic with IPsec or Zero Trust principles.”

