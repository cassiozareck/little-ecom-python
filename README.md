Little-Ecom-Python is a small-scale ecommerce api application made in python+django designed primarily for learning purposes. It serves as a segment of a larger project known as Little-Ecom, which was developed in Go with microservices architecture. Please visit: https://github.com/cassiozareck/little-ecom

Endpoints
Item Management

    add-item/: Add a new item.
    update/: Update an existing item.
    remove-item/<int:item_id>/: Remove an item.
    items/: Retrieve all items.
    buy-item: Execute the purchase of an item.

User Authentication

    auth/register/: Register a new user.
    auth/signin/: Sign in for existing users.
    auth/validate_token/: Validate JWT tokens for secure transactions.

Security

To interact with certain endpoints, especially those that alter data or require user identity verification, a valid JWT token must be used. This ensures that all requests are securely authenticated and authorized.
