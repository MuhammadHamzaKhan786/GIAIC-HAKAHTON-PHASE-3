---
name: backend-skill
description: Build backend systems by generating API routes, handling requests and responses, and connecting to databases.
---

# Backend Skill

## Instructions

1. **Route generation**
   - Define RESTful or RPC-style endpoints
   - Organize routes by feature or resource
   - Apply consistent URL naming conventions
   - Separate public and protected routes

2. **Request handling**
   - Parse request parameters, body, and headers
   - Validate and sanitize user input
   - Handle authentication and authorization
   - Implement middleware for common logic

3. **Response handling**
   - Return proper HTTP status codes
   - Send structured JSON responses
   - Handle errors consistently
   - Avoid leaking internal errors to clients

4. **Database connectivity**
   - Establish secure database connections
   - Use ORM or query builders when appropriate
   - Manage connection pooling
   - Handle database errors gracefully

## Best Practices
- Keep controllers thin and reusable
- Centralize error handling
- Use async/await consistently
- Validate inputs at the boundary
- Follow REST or API design standards
- Log requests and errors responsibly
- Write modular, testable code

## Example Structure
```ts
// Route definition
app.post("/users", async (req, res) => {
  const { email } = req.body;

  const user = await db.user.create({
    data: { email },
  });

  res.status(201).json({
    success: true,
    data: user,
  });
});
