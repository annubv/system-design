# API Rate Limiter

## Algos:
1. Token Bucket
2. Leaking Bucket
3. Fixed Window Count
4. Sliding Window Log
5. Sliding Window Count


### Token Bucket
- Can be implemented through counter
- Capacity to hold tokens
- More tokens -> overflow
- Refiller: In 1 minutes, add more tokens
- If access, its overflow, removed
- Flow:
    - Is there token:
        - No: Denied -> HTTP 429
        - Yes: Reduce token, give access
- Can give tokens per user, example -> 3 tokens per user per minute



### Leaking Bucket
- Can be implemented through queue
- Flow:
    - Queue fill?
        - No -> Request add -> process
        - Yes -> Deny
- Not works when there's a burst of requests


### Fixed Window Count
- Divides time into timeframe of fixed length, lets say minutes
- Each window has a counter lets say 3
- Disadvantage:
    - When the requests come at edges of windows, we may allow more requests than the system can handle
    - Example:
    - Window 1 -> 8:00 - 8:05 and Window 2 -> 8:05 - 8:10
    - If requests are at edges, lets say 8:04 - 8:05 has 3 requests and 8:05 - 8:06 has 3 requests, we are handling 6 requests together


### Sliding Window Log
- Fixes disadv of fixed window
- This has log instead of counter
- No fixed time frames for window
- Lets say we want to allow 3 req per minute
- Flow:
    - Req 1 -> Log timestamp 1 (start window)
    - Req 2 -> Log timestamp 2 (within widow of 1 minutes)
    - Req 3 -> Log timestamp 3 (now window is filled)
    - Req 4 -> Log timestamp 4 (one minute not crossed, but window filled -> Deny)
    
    - 1 minute passed

    - Req 5 -> Log timestamp 5 (Slide window, remove elements until Req 5 is in window)
- Disadv:
    - Storing denied req logs


### Sliding Window Count
- Used Fixed Window Count and Sliding Window Log
- Lets say rule -> 5 req/minute allowed
- Flow:
    - Find requests present in current window
    - And finds whether it crossed the limit


### Components

- Can use redis to store counter
- need config file to store details (disk or cache)


### Design

- If we have api gateway, we can apply rate limited there, else at the application level
- For distributed rate limiters, have a common store in redis
- But redis doesnt have atomicity for parallel requests?
    - Bring atomicity to redis using existing solutions, but it will increase latency
    - Otherwise it will be a limitation