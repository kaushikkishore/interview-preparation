### Networking Concepts

#### Basic Networking Concepts
These are foundational ideas you should be comfortable explaining concisely in an interview.

1. **OSI Model**:
   - A 7-layer framework for understanding networking:
     1. Physical (cables, switches)
     2. Data Link (MAC addresses, Ethernet)
     3. Network (IP addresses, routing)
     4. Transport (TCP/UDP, ports)
     5. Session (connection management)
     6. Presentation (data formatting, encryption)
     7. Application (HTTP, FTP, user-facing protocols)
   - Example: "When you visit a website, the request goes from the Application layer (browser) down to Physical (Ethernet cable) and back up on the server side."

2. **IP Addressing**:
   - IPv4 (32-bit, e.g., 192.168.1.1) vs. IPv6 (128-bit, e.g., 2001:0db8::1).
   - Subnetting: Dividing a network into smaller segments (e.g., 192.168.1.0/24 means 256 addresses, 254 usable).
   - Public vs. Private IPs (e.g., 10.0.0.0–10.255.255.255 is private).

3. **TCP vs. UDP**:
   - TCP: Reliable, connection-oriented (e.g., HTTP, email). Uses 3-way handshake (SYN, SYN-ACK, ACK).
   - UDP: Fast, connectionless (e.g., video streaming, DNS). No guaranteed delivery.

4. **Routing and Switching**:
   - **Switches**: Operate at Layer 2 (Data Link), forward frames based on MAC addresses.
   - **Routers**: Operate at Layer 3 (Network), forward packets based on IP addresses using routing tables.
   - Protocols: OSPF, BGP (more on these later).

5. **DNS**:
   - Translates domain names (e.g., google.com) to IP addresses.
   - Process: Client → Resolver → Root Server → TLD Server → Authoritative Server.

#### Above-Average Networking Concepts
These are more advanced topics likely relevant to Aviatrix’s cloud networking focus.

1. **Software-Defined Networking (SDN)**:
   - Decouples the control plane (decision-making) from the data plane (packet forwarding).
   - Benefits: Centralized management, programmability.
   - Example: Aviatrix uses SDN principles for cloud-native networking.

2. **Virtual Private Cloud (VPC)**:
   - A private network within a public cloud (e.g., AWS VPC).
   - Features: Subnets, route tables, gateways (e.g., Internet Gateway, NAT Gateway).
   - Aviatrix enhances VPC connectivity across multi-cloud environments.

3. **Overlay vs. Underlay Networks**:
   - **Underlay**: Physical infrastructure (routers, switches).
   - **Overlay**: Virtual network on top (e.g., VXLAN, GRE tunnels).
   - Aviatrix leverages overlays for secure, scalable multi-cloud connectivity.

4. **BGP (Border Gateway Protocol)**:
   - Dynamic routing protocol used between autonomous systems (AS).
   - Key for multi-cloud: Advertises routes between cloud regions or providers.
   - Attributes: AS Path, Next Hop, Weight.

5. **Load Balancing**:
   - Distributes traffic across servers for scalability/reliability.
   - Types: Layer 4 (TCP/UDP) vs. Layer 7 (HTTP-based, smarter routing).
   - Cloud context: AWS ELB, Aviatrix’s distributed load balancing.

6. **Network Address Translation (NAT)**:
   - Maps private IPs to public IPs.
   - Types: Source NAT (SNAT), Destination NAT (DNAT).
   - Cloud use: NAT Gateways for outbound traffic in VPCs.

---

### Security Concepts

#### Basic Security Concepts
These are foundational ideas to articulate clearly.

1. **Firewalls**:
   - Filters traffic based on rules (e.g., allow port 80, block 22).
   - Types: Stateless (checks each packet) vs. Stateful (tracks connections).

2. **Encryption**:
   - Symmetric (e.g., AES): Same key for encrypt/decrypt.
   - Asymmetric (e.g., RSA): Public/private key pair.
   - Use case: HTTPS uses TLS (combines both).

3. **Authentication and Authorization**:
   - Authentication: Verify identity (e.g., username/password, MFA).
   - Authorization: Determine permissions (e.g., role-based access control).

4. **VPN (Virtual Private Network)**:
   - Secure tunnel over the internet (e.g., IPsec, OpenVPN).
   - Encrypts traffic between endpoints.

5. **Threats**:
   - DDoS: Overwhelms a service with traffic.
   - Man-in-the-Middle (MitM): Intercepts communication.
   - Phishing: Social engineering to steal credentials.

#### Above-Average Security Concepts
These align with Aviatrix’s focus on secure cloud networking.

1. **Zero Trust Architecture**:
   - Principle: Trust nothing, verify everything.
   - Implementation: Perimeter-less security, continuous authentication.
   - Aviatrix use: Granular policies for cloud access.

2. **Network Segmentation**:
   - Divides network into zones to limit breach impact.
   - Cloud example: VPC peering with strict security groups.
   - Aviatrix: Enforces segmentation across multi-cloud.

3. **IPsec**:
   - Secures IP communications with encryption and authentication.
   - Modes: Transport (encrypts payload) vs. Tunnel (encrypts entire packet).
   - Common in site-to-cloud VPNs.

4. **Intrusion Detection/Prevention Systems (IDS/IPS)**:
   - IDS: Monitors and alerts (e.g., Snort).
   - IPS: Actively blocks threats.
   - Cloud twist: Integrated into next-gen firewalls (e.g., Palo Alto, Aviatrix integrations).

5. **Cloud Security Posture Management (CSPM)**:
   - Monitors cloud configs for misconfigurations (e.g., open S3 buckets).
   - Aviatrix context: Visibility into network security policies.

6. **Secure Access Service Edge (SASE)**:
   - Combines networking (SD-WAN) and security (firewall, zero trust) at the edge.
   - Aviatrix aligns with SASE for distributed cloud architectures.

---

### Interview Prep Tips
1. **Relate to Aviatrix**: Their platform focuses on multi-cloud networking, transit gateways, and security. Mention how SDN, BGP, or Zero Trust apply to their solutions.
2. **Be Ready for Scenarios**: E.g., “How would you secure traffic between AWS and Azure?” (Answer: IPsec tunnels, Aviatrix transit, segmentation.)
3. **Brush Up on Cloud**: Know AWS VPCs, Azure VNets, GCP networking basics.
4. **Practice Whiteboarding**: Explain OSI, VPC design, or IPsec tunnel setup.
