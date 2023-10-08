# Facebook Messenger

## 1. WHY DO WE NEED IT?
- Provides instant messaging service
- Users can use both thier phone or desktop


## 2. REQUIREMENTS AND GOALS OF THE SYSTEM

### Functional Requirement
- 1-1 conversations
- Online/Offline status of the users
- Persistantly store chat history

### Non Functional Requirement
- Real time experience with low latency
- High consistency, same chat history should be in all the devices
- Can trade high availability for consistency although it is desirable


### Extended Requirement
- Group Chats
- Push notifications for offline users

## 3. CAPACITY ESTIMATIONS AND CONSTRAINTS
- Assume we have 500M daily active users
- Each user sends 40 msg a day
- `500M * 40 = 20B` msgs per day

### Storage Estimations
- Assume on average each msg is of 100 bytes
- `100bytes * 20B = 2TB/day` storage requirements
- Let's say we need to handle 5 years of storage then storage req = `2TB * 365 days * 5 ~= 3.6PB`
- Aside from this, we would also need to store metadata of the msgs, users, etc
- We also need to consider data replication

### Bandwidth Estimation
- We need to handle 2TB of data every day, this gives us
- `2TB/(24 * 60 * 60) = 25MB/sec`
- We need this for both upload and download

### High Level Estimation

|                      |                    |
| -------------------- | ------------------ |
| Total Messages       | 20 billion per day |
| Storage for 1 day    | 2TB                |
| Storage for 5 years  | 3.6PB              |
| Incoming Data        | 25MB/sec           |
| Outgoing Data        | 25MB/sec           |

## 4. HIGH LEVEL DESIGN

- We need a chat server which will handle to and fro of the msgs
- The workflow would be like:

- User A sends a msg to User B through chat server
- Chat server receives it and sends the ack to User A that the msg is sent
- Chat server will store the msg in the DB and will send it to User B
- User B would send an ack to the chat server upon receiving the msg
- The chat server would then notify User A about the delivery of the msg

<img src="./Resources/5-1.png">


## 5. DETAILED COMPONENT DESIGN