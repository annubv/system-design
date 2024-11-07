# E-Comm App like Flipkart/Amazon

## Functional Requirement
- Search for products
- See products details
- Add products to cart
- Place orders


## Non Functional Requirement
- Highly Consistent
- Available
- Low latency for search
- Failure protection
- Handle concurrency and heavy read and writes


## Capacity Estimations
- 1B active users
- 100M products
    - Lets say 1KB per product
    - 100M * 1KB = 100GB (enought to store in one machine, but we will partition)
- 10% users place products
    - 100M orders per day

## API Design
1. seach products
    - searchProducts(qs)
    - in reality theres a recomm. engine based on user history and surroundings, but lets keep it simple

2. Add to cart
    - addToCart(userId, productId, data)

3. Place order
    - placeOrder(userId, cartId)


## DB Design
- User Table
    - email
    - hash pass 
    - addr