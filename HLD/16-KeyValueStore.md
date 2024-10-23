# KEY-VALUE STORE

Also refered as KV DB or Non-relational DB.

- Key must be unique
- Data can be accessed via key
- Keys can be plain text or hashed values
- Ex: Redis, memcached, Amazon dynamo

## Requirement Gathering

### Functional Requirement
- Give get and set methods to retrive and store a key-value pair

### Non Functional Requirement
- High Availaibility 
- Fault tolerance
- High scalability
- Low latency
- Tunable consistency


## Single Server setup
- Easy: store in a hash table 
- This will save data in memory
- Fast
- We can compress data to fit in memory
- Store frequent data only in memory rest in disk


## Distributed Setup
- Apply CAP theorem
- We might go with availability, can use eventual consistency

## System components
- Data Partition: Use consistent hashing
    - Scaling
    - Heterogeneity (Bigger servers can have more virtual nodes)

- Data Replication:
    - Get a key
    - Get its node on the ring
    - Replicate its data on the next n nodes as well
    - We can tune this n according to our needs
    - Use data centeres at different location also

- Consistency:
    - Lets say:
        - N = number of replicas
        - W = number of replicas we require ack from to consider a successfull write
        - R = number of replicas we require response from to consider a successfull read

    - The config of N,W,R is a tradeoff bw:
        - Latency
        - Consistency


    - R=1, W=N : Optimsed for fast reads
    - R=N, W=1 : Optimised for fast writes
    - W+R>N : Strong consistency
    - W+R<=N : Weak consistency

    - Our goal is to provide better availability for now. But we can tune it.

- Consistency modes:
    - Strong : client never sees out of date data
    - Weak : Read ops may see diff results
    - Eventual : Weak, which eventually is consistent

    - For our sys we are going for eventual as write ops are faster this way

- Inconsistency Resolution:
    - Versioning:
        - Doesnt work when 2 parallel request update the same key, thus there are conflicts
    - Vector clock:
        - D([S1, V1], [S2, V2], ....)
        - In this, conflicts are resolved by the client upon read
        - Conflicts : D([S0, 1], [S1, 2]) AND D([S0, 2], [S1, 1])
        - This adds complexity to the client

- Handling Failures
    - Failure detection:
        - Gossip protocol
        - Each server chooses a set of nodes for heartbeats
        - If a particular server is not responding for a long time, node asks other nodes if that node is down

    - Temporary Failures:
        - If a node is down, another node can take the request (sloppy quorum)
        - When the node is back up, changes are pushed back for consistency (Hinted handoff)

    - Permanent Failures:
        - Merkle Tree
            - Divide space into some buckets lets say 4
            - Hash each key into a bucket
            - Create a single hash node per bucket
            - Build the tree to the root

            - To compare, start with the root
                - If there is a difference then go to left or right tree to find the culprit
                - If the merkle tree matches then both tree have same data
    - Data centre outage:
        - Replicate along data centeres

### Write Path
- Client sends set request
- Request is forwarded to a specific node
- Log request in a commit log file
- Save data in memory
- When memory is full, flush into SSTable (Sorted String Table -> sorted list of key-val pair)

### Read path
- Client sends get request
- Request is forwarded to a specific node
- Check in memory
- If not, check in bloom filter
- find the data in SSTable
- Return the data to the client



|         Goal               |    Technique                 |
| -------------------------- | ---------------------------- |
| Store big data             | consistent hashing           |
| high availability reads    | data replication             |
| high available writes      | versioning, vector clocks    |
| data partition             | consitent hashing            |
| inceremental scalability   | consitent hashing            |
| heterogeneity              | consitent hashing            |
| tunable consistency        | quorum consensus             |
| temporary failures         | sloppy quorum, hinted handoff|
| permanent failures         | merkle tree                  |
| data outage.               | cross center replication     |
