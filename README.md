# Finance Tracker API

A FastAPI backend service for personal finance management.

## Features

- User authentication
- Transaction tracking
- Category management
- Budget planning
- Spending analytics

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL/SQLite
- JWT Authentication

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Project Structure
app/
├── main.py # FastAPI application
├── config.py # Configuration
├── database.py # Database setup
├── models/ # Database models
├── schemas/ # Data validation
├── api/ # API endpoints
└── services/ # Business logic

## Development

This is a work in progress. More features coming soon!