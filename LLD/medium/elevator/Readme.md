# Elevator System
- Multiple Elevators running on multiple floors
- Each elevator has capacity limit
- Users can request for elevators from any floor
- Elevator movement should be optimised to have min waiting time for users

## Entity Identifcation
- Direction (Representing direction of elevator movement)
- Request (Represent a user request for elevator)
    - Source
    - Destination
- Elevator (Maintains requests list, has capacity limit)
- ElevatorController (Maintains a list of elevators and returns the optimal elevator for a request) 
