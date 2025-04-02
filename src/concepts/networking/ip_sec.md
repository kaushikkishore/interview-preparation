### IPsec (Internet Protocol Security)

#### Layman’s Terms
- **What It Is**: Think of IPsec as a “secret envelope” for your letters. It scrambles the message and locks it so only the right person (with the key) can open it, even if someone steals it while it’s traveling over the internet.
- **How It Works**: Before sending data, IPsec wraps it in this secure envelope and adds a special “handshake” to agree on the lock and key. Then, it sends it through a private “tunnel” (like a hidden road) so outsiders can’t see where it’s going or what’s inside.
- **Why It’s Useful**: It keeps your data safe from hackers eavesdropping or pretending to be someone else.
- **Example**: When your store (AWS) sends customer data to the analytics team (Azure), IPsec makes sure no one can read it along the way.

#### Technical Terms
- **Definition**: IPsec is a **suite of protocols** that secures IP communications by **encrypting** and **authenticating** packets, commonly used for VPNs (Virtual Private Networks).
- **Key Components**:
  - **AH (Authentication Header)**: Ensures data integrity and authenticity (rarely used alone).
  - **ESP (Encapsulating Security Payload)**: Encrypts + authenticates (most common).
  - **IKE (Internet Key Exchange)**: Negotiates keys and settings (e.g., IKEv2).
- **Modes**:
  - **Transport Mode**: Encrypts payload only (e.g., between two servers).
  - **Tunnel Mode**: Encrypts entire packet, wraps it in a new IP header (e.g., VPNs).
- **Mechanics**:
  - **Encryption**: Algorithms like AES-256 (256-bit keys) in modes like GCM (fast, authenticated).
  - **Authentication**: HMAC-SHA256 ensures data isn’t tampered with.
  - **SA (Security Association)**: Pair of policies/keys for each direction (e.g., AWS → Azure SA).
  - **Process**: IKE Phase 1 (secure channel), Phase 2 (data tunnel), then ESP encrypts packets.
- **Cloud Use**: In Aviatrix, IPsec tunnels connect the Transit Hub to Azure VNet or on-premises, securing traffic over the public internet (e.g., ESP tunnel from 10.100.0.1 to 10.2.0.1).
- **Example**: AWS Transit Gateway establishes an IPsec tunnel to Azure, encrypting packets with AES-256 and routing 10.1.0.0/16 traffic through it.
