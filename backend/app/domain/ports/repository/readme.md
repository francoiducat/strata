# Repository Ports

This package contains repository interface (port) definitions used by the application layer.

- Each class defines the minimal contract expected by the domain and application layers.
- Implementations live in the infrastructure/adapters layer (e.g. SQLAlchemy repositories).

Guidelines:
- Keep interfaces small and focused.
- Use domain entities in method signatures (not ORM models).
- Implementers should return domain entities and raise domain-specific exceptions where appropriate.

