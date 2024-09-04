# Twitter

## 1. WHY DO WE NEED IT?

- Users can share tweets (short msgs of 140 length)
- Can access through web/app

## 2. FUNCTIONAL AND GOALS OF THE SYSTEM

### Functional Requirements

- Users should be able to submit new tweets
- Users should be able to mark tweets as favourites
- Users should be able to follow other users
- Users should have a timeline
- Users should be allowed to share photos/videos

### Non Functional Requirements

- Should be highly available
- Should have low response time for timeline generation
- Consistency is not important

### Extended Requirements

- Re-tweets
- Searching for tweets
- Trending topics/users
- Tagging other users

## 3. CAPACITY ESTIMATIONS AND CONSTRAINTS

- Let's assume we have 1B users
- We have 200M DAU
- Let's assume we have 100M daily tweet
- Each user follow 200 other users

- If each users favourites 5 tweets per day we have:
    - 200M * 5 = 1B favourites

- Let's assume a user visits the timeline 2 times per day, and visits 5 user profiles
    - Assuming each page will have 20 tweets, the total views would be:
    - 200M DAU * ((2+5)*20) = 200M * 140 = **28B** views per day

### Storage Estimates

- Assuming each tweet will be of 140 character length
- Each character will take 2 bytes
- Let's assume we need to store 30 bytes of metadata
- Total Storage needed:
    - 100M tweets * ((140*2) + 30)  =  100M * 310 = **31B Bytes** = **30GB/DAY**

- Some tweets will also have media.
- Let's assume, on an average every 5th tweet has a photo and every 10th tweet has a video
- Also, lets assume average size of photo = 200KB and avg size of vide = 2MB
- Storage needed for media:
    - (100M/5*200KB) + (100M/10*2MB) = 10M*400KB + 10M*2MB = 10M*400K Bytes + 10M * 2Million Bytes
    - 4TB + 20TB = **24TB/Day**

### Bandwidth Estimates

- Ingres is 24TB: 
    - 24TB/Day = 24TB/86400 = 24000000MB/86400 = **280MB/Sec**
- For outgres, we have 28B views per day
- Every 5th tweet will have a photo as well
- Every 10th tweet will have a video, lets assume user wacthes every 3rd video:
    - ((28B * 280 Bytes)/86400) + ((28B/5 * 200KB)/86400) + ((28B/10/3 * 2MB)/86400)
    - 93MB/sec + 13GB/sec + 22GB/sec
    - **35GB/sec**

## 4. SYSTEM APIs

- tweet(api_key, tweet_data, location, media_ids)

## 5. HIGH LEVEL DESIGN
- We have a read heavy system
- Read 28B/86400 = 325K Tweets/per second
- Write 100M/86400 = 1150 Tweets/per second
- We need efficient DB to store metadata, tweet data and file storage to store photos/videos
- Traffic will be unevenly distributed throughout the day, so better to have a system with more than minimum requirement

## 6. DATABASE DESIGN

- We need to store:
    - Tweet
    - User
    - UserFollow
    - Favourite

- We require join, so we can go for SQL. But, it will cause issues on high scale
- Instead of RDBMS, we can also go for key-value store to enjoy the benefits of NoSql
- We can store media metadata in a table where media_id would be the key and value would be an object containing all the details
- Same approach can be used to store user details
- For storing the media-user, tweet-user, user-user relationships, we can use a wide-column NoSql database like Cassandra
- Table UserPhoto would have a key user_id and value would be list of photo_ids that the user owns in different columns
- Same scheme can be used for storing UserFollow relationship
- These stores always maintain replicas so reliability is sorted
- Also deletion isn't applied instantly to support undo


## 7. DATA SHARDING
- We have hughe ingres and outgres, we need to distribute data
- Sharding on User Id:
    - A server will have all of a single user's tweets, favourites, follows, etc
    - Fast to get a user's data
    - Issue1: If a user becomes hot, high load will be on a single server
    - Ussue2: Maintaining growing data will become difficult

- Sharding on Tweet Id:
    - Map a tweet id to a random server
    - To get a user's all tweets, we will have to seek all the servers
    - A centralized server will aggregate and then return result
    - For timeline generations, will have to query all the servers to get following's tweets in sorted order, then order again.
    - Solves hot user problem but increases latencies

- Sharding on tweet creation time
    - Will help us to get recent tweets quickly
    - But the servers with latest data will always face high load

- Sharding on tweet id and creation data
    - tweet id will consist of an epoch (denoting creation time) and an incrementing sequence for ID
    - Assign tweets to random servers
    - We still would have to query all servers but latency will reduce since we already have epoch for sorting
    - So we do not need a secondary index, only tweet id will be used

## 8. CACHE

- We can use memcache to handle hot tweets/users
- LRU is reasonable, LFU as well
- We can use 80-20 rule for intelligent caching
- We can cache latest data as it has high chances of being consumed


## 9. TIMELINE GENERATION

## 10. REPLICATION AND FAULT TOLERANCE
- We will have master-slave db for write-read
- will have more secondary dbs for failure protection

## 11. LOAD BALANCING
- We can add LBs on:
    - B/W Clients and App servers
    - B/W App servers and DB Replication servers
    - B/W Aggregation servers and cache sercers
- Round robin approach

## 12. MONITORING
- New tweets per day, whats daily peak?
- How many tweets being delivered/day
- Avg latency for timeline


## 13. EXTENDED REQUIREMENTS
- Retweets
- Trending Topics
- Follow Suggestions
- Search

