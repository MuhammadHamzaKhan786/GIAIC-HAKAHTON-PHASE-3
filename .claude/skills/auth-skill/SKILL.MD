---
name: auth-skill
description: Design and implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **Core Authentication Flows**
   - User signup with input validation
   - User signin with credential verification
   - Password reset and change flows
   - Session and authentication state management

2. **Password Security**
   - Hash passwords using `bcrypt` or `argon2`
   - Never store or log plain-text passwords
   - Use per-user salts and sufficient hash rounds
   - Compare hashes securely during signin

3. **JWT Token Handling**
   - Generate JWT access tokens on successful signin
   - Use refresh tokens for long-lived sessions
   - Define token expiry and rotation strategy
   - Verify JWTs on protected routes and APIs

4. **Better Auth Integration**
   - Configure Better Auth with environment variables
   - Enable email/password authentication
   - Integrate OAuth providers if required
   - Handle callbacks, sessions, and token storage

## Best Practices
- Enforce strong password policies
- Use HTTPS in all environments
- Keep JWT payloads minimal (no sensitive data)
- Store secrets in environment variables
- Implement rate limiting on auth endpoints
- Separate authentication logic from business logic
- Log authentication events without exposing credentials

## Example Structure

```ts
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

// Signup
export async function signup(email: string, password: string) {
  const hashedPassword = await bcrypt.hash(password, 12);

  return db.user.create({
    data: {
      email,
      password: hashedPassword,
    },
  });
}

// Signin
export async function signin(user: { id: string }) {
  return jwt.sign(
    { userId: user.id },
    process.env.JWT_SECRET!,
    { expiresIn: "15m" }
  );
}
