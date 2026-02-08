---
name: database-skill
description: Design and manage databases including table creation, migrations, and scalable schema design.
---

# Database Skill

## Instructions

1. **Schema design**
   - Identify entities and relationships
   - Normalize tables to reduce redundancy
   - Define primary and foreign keys
   - Choose appropriate data types

2. **Table creation**
   - Create tables with clear naming conventions
   - Apply constraints (NOT NULL, UNIQUE, DEFAULT)
   - Add indexes for frequently queried columns
   - Enforce referential integrity

3. **Migrations**
   - Create versioned migration files
   - Support up and down migrations
   - Apply migrations safely across environments
   - Avoid destructive changes in production

4. **Database evolution**
   - Modify schemas incrementally
   - Backfill data when adding new columns
   - Maintain backward compatibility
   - Document schema changes

## Best Practices
- Use snake_case for table and column names
- Never edit applied migrations directly
- Keep schemas simple and explicit
- Index intentionally, not excessively
- Test migrations on staging before production
- Separate read and write concerns when scaling

## Example Structure
```sql
-- Create users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Migration example
ALTER TABLE users
ADD COLUMN is_active BOOLEAN DEFAULT true;
