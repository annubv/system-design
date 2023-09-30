# Dropbox

## 1. WHY DO WE NEED IT?

- File hosting service, enables users to store data on remote servers
- Users pay a subscription fees
- Simplify file sharing between different users or different devices (mobile, laptop, tablets, etc)
- Top benefits of cloud storage
    - **Availability** - Data is available anytime from anywhere
    - **Reliability & Durability** - Cloud storage ensures that users do not lose their data by storing it in multiple geographically distributed servers
    - **Scalability** - Users do not have to worry about storage limitations as long as they are willing to pay for it

## 2. REQUIREMENTS AND GOAL OF THE SYSTEM

### Function Requirements
- Users should be able to upload/download files
- System should support sharing of files/folders between users
- System should support storage of large files
- System should support offline modifications of files or folders, when users come online these changes should be synced
- Changes should be synced across all the devices that user uses

### Non Functional Requirements
- ACID-ity is required (Atomicity, Consistency, Isolation, Durability) of all file oprations
- Availability, Reliability, Scalability

### Extended Requirements
- System can support snapshots of data so that user can go back to any version of the files


## 3. SOME DESIGN CONSIDERATIONS

- We should expect high read and write volumes
- Read-Write ratio will apporximately be same 
- We can divide our files into smaller chunks (say 4MB) while storing on our db
- So if an upload fails, only the failed chunks will be retried
- This will also reduce the amount of data exchange by transferring the updated chunks only
- For smaller changes, clients can create a diff at their end and send the updated chunks only
- Clients can also keep a local copy of metadata at their end to reduce round trips.

## 4. CAPACITY ESTIMATIONS AND CONSTRAINTS

- Let's assume we have 500M users
- 100M daily active users (DAU)
- Let's assume each user has 200 files, thus total files we need to store = `500M * 200 = 100B files`
- Let's also assume that each file on an average is of 100KB. Thus total storage needed = `100B * 100KB = 10PB`.
- Let's assume we have 1M active connections per minute.
- Summarizing we have the following data:

|                      |             |
| -------------------- | ----------- |
| Total Users          | 500 Million |
| Files per user       | 200         |
| Total files          | 100 Billion |
| File size (avg)      | 100 KB      |
| Total Storage        | 10 PB       |




## 5. HIGH LEVEL DESIGN

- The user will specify a folder as a workspace and any file file or folder placed in this folder will propogate onto the cloud, whenever user deletes or modifies it, the same will be reflected on cloud
- Similarly the user have its workspace on all its devices which will be synced across, any changes made on device 1 will also reflect on device 2.
- To faciliate this, at higher level we need to:
    - Store the files and folders
    - Store the metadata like name, size, directory and with whom the file/folder is shared with
    - We also need some mechanism which will tell all the devices when a change is made on one device
- For this, we need to have:
    - A block server which handle file uploads, downloads on cloud storage
    - A metadata server which handle the storage of metadata of files and folders in NoSQL or SQL db
    - A Synchronisation server which will handle the syncing of all the devices by notifying them about the change

<img src="./Resources/4-1.png">

## 6. COMPONENT DESIGN

### 6.1. Client

- The client application monitors the workspace folder on the user's machine and syncs the changes in files with the cloud
- The client works with the storage service to handle the upload/download/modification of files on the cloud storage
- The client also talks with the sync and metadata service to update the metadata of files and folders
- Some important ops of clients are:
    - Upload/Download files
    - Detect changes in the workspace folder
    - Handle conflicts because of offline or concurrent changes

#### How do we handle file transfer efficiency?
- As mentioned above, we can divide our file in fixed sized chunks lets say (4MB) and only transfer the modified chunks when required
- To optimise space and I/O operations per second (IOPS) we can determine the optimal chunk size on the basis of:
    - Storage device we are using on the cloud
    - Average file size on our server
    - Available network bandwidth
- Metadata of files should contain the info about these chunks
- We can keep a local copy of metadata at client to enable offline updates and save a lot of round trips

#### How clients can listen to changes happening with clients?
- One solution is to make periodical HTTP calls to the server expecting a result
- This approach will have a delay in displaying the changes
- We cannot make frequent calls because most of the times the server would return an empty reponse and it will also keep the server busy
- Workaround for these issues is to use an **HTTP long polling connection**
- The server will hold the connection and will send the response when it becomes available
- The client will then immediately send another request with expectation that the server will not respond immediately

#### We can divide our client into following parts:
- **Internal Metadata DB** - It will keep track of all the files, location, chunks, etc.
- **Chunker** - This will be responsible to break down a large file into chunks and transfer only the modified chunks by identifying them. We can also use this to reconstruct the file using the chunks
- **Watcher** - This will monitor the workspace and tell the Indexer about any changes that the user makers. This will also watch for any changes happening on other clients which are broadcasted by the sync service
- **Indexer** - This processes the events from the watcher and updates the metadata db with new information. Once chunks are successfully submitted to or downloaded from the cloud storage, indexer communicates with the sync service to broadcast the changes on all the devices and update remote metadata db

### 6.2. Metadata Database
- Responsible for maintaining the versioning and metadata info of file, chunks, users, workspace, etc.
- It can be a relational one or non-relational
- If we go with non relational DB, we will have to take care of ACID properties with the help of our sync service, since they do not support ACID properties in favour of performance and scalability
- We can also go with a relational DB since it supports ACID properties natively
- We need to store metadata info about different objects such as:
    - Users
    - Files
    - Chunks
    - Devices
    - Workspace

### 6.3. Synchronization Service