### BGP (Border Gateway Protocol)

#### Layman’s Terms
- **What It Is**: Imagine BGP as a "smart postal service" for the internet. It’s a system that figures out the best way to send letters (data) between different cities (networks), even if those cities are run by different companies (like AWS, Azure, or your office).
- **How It Works**: Each city tells its neighbors, “Hey, I’ve got these streets (networks) you can reach through me.” BGP listens to all these updates and picks the fastest or shortest route to deliver the mail.
- **Why It’s Useful**: Without BGP, every city would need to know every road in the world (impossible!). Instead, BGP keeps things simple by sharing just enough info to get the job done.
- **Example**: If your online store (AWS) needs to send sales data to your analytics team (Azure), BGP makes sure the data takes the best path through the internet “headquarters” (Transit Hub).

#### Technical Terms
- **Definition**: BGP is a standardized **path-vector routing protocol** used to exchange routing information between different **autonomous systems (AS)**—unique networks with their own IP ranges and policies (e.g., AS12345 for AWS, AS67890 for Azure).
- **Key Features**:
  - **Dynamic Routing**: Updates routes automatically as networks change (e.g., a new subnet is added).
  - **Attributes**: Uses metrics like **AS Path** (list of networks passed through), **Local Preference** (internal priority), and **MED** (Multi-Exit Discriminator, external hint) to choose the best path.
  - **Scalability**: Handles the entire internet’s routing table (~900,000 prefixes).
- **Mechanics**:
  - **Messages**: Open (start session), Update (share routes), Keepalive (stay connected), Notification (error).
  - **States**: Idle → Connect → Active → OpenSent → OpenConfirm → Established.
  - **eBGP vs. iBGP**: External BGP (between ASes, e.g., AWS ↔ Azure) vs. Internal BGP (within an AS, e.g., AWS regions).
- **Cloud Use**: In Aviatrix, BGP runs over tunnels to advertise VPC/VNet CIDRs (e.g., “10.1.0.0/16 is in AWS”) to the Transit Hub, enabling dynamic multi-cloud routing.
- **Example**: AWS (AS16509) advertises 10.1.0.0/16 to the Transit Hub, which propagates it to Azure via BGP Update messages.
