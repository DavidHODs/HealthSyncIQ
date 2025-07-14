# HealthSync - API Backend (Ongoing)

This project is the backend API for HealthSync, an application designed to facilitate secure and efficient healthcare data management and communication. HealthSync aims to provide a robust and scalable foundation for managing healthcare related information.

Features (Under Development)
Secure Data Handling – Implementing robust mechanisms for sensitive health data. (Future: Encryption, Access Control)

Tech Stack
FastAPI – High-performance web framework for building asynchronous APIs.

PostgreSQL – Relational database for storing structured health data and communication logs.

SQLAlchemy/Pydantic – ORM for data modeling and validation of complex healthcare entities.

Alembic – Database migrations for evolving the schema securely.

Poetry – Dependency management for a clean and reproducible development environment.

Docker & Docker Compose – Containerization for consistent development and deployment environments.

MyPy – Static type checking to ensure code quality and reduce errors in a critical domain.

## Install Poetry

Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed before proceeding.  

You can install Poetry using the official installer:  

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Dependencies

```sh
make install
```

### Run Linters

Run auto-formatting and static analysis checks:

```sh
make lint
```

### Run the Application

Start the FastAPI application:

```sh
make run
```
