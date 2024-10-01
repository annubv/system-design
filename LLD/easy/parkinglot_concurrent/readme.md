# PARKING LOT SYSTEM

## REQUIREMENTS

- 3 Parking gates working simultaneously
- Handle race conditions
- Multiple vehicle types
- Parking has multiple floors
- Each floor has multiple parking spot
- A parking spot can be avaialable or unavailable
- A parking spot can handle a bike or a car
    - For simplicity lets consider a spot can handle only one type of vehicle


## Entities Identification

- Vehicle (Can have multiple types)
- Parking Spot (To handle a vehicle)
    - Can add a vehicle 
    - Can remove a vehicle
    - Handle race conditions
- Floor (Has multiple parking spots)
    - Can add spot
    - Has info about all its parking spots
- Gate
    - Can be an exit or entry gate
    - Should work in parallel (on its own thread)
    - Simulate time for entry and exit of a car
    - Mark entry and exit time of vehicle
- Billing
    - Has a car id
    - Procceses payment
    - payment type -> offline/online
- Ticket
    - Has a car id
    - stores entry and exit of the car
    - also stores the amount due
    - method to calculate the amount on the basis of entry and exit time
- ParkingLot
    - Stores floors -> which stores parking spots
    - Stores vehicle data -> {id: vehicle_data}