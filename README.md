# model_context_protocol

This project is an exploration of the Model Context Protocol (MCP) framework. Below is a summary of the tasks and progress made in this project:

## Overview
The project involves creating and running MCP servers with various functionalities, including integration with Redis, PostgreSQL, and weather APIs. The MCP framework is used to define tools and resources for these servers.

## Tasks Completed

### 1. MCP Redis Server
- Implemented a custom Redis adapter using `redis.asyncio`.
- Created an MCP server that interacts with Redis for storing and retrieving key-value pairs.
- File: `mcp_redis_server.py`

### 2. MCP PostgreSQL Server
- Integrated PostgreSQL with MCP using `psycopg`.
- Implemented tools and resources to:
  - Retrieve database schema information.
  - Store and retrieve key-value pairs in a custom MCP store table.
- Managed database connection lifecycle using an async context manager.
- File: `mcp_postgres_server.py`

### 3. Weather API Server
- Created an MCP server to fetch weather alerts and forecasts using the National Weather Service (NWS) API.
- Implemented tools to:
  - Get active weather alerts for a US state.
  - Get weather forecasts for a specific location (latitude and longitude).
- File: `weather.py`

### 4. Demo MCP Server
- Created a demo MCP server with basic tools and resources:
  - Addition tool to add two numbers.
  - Greeting resource to generate personalized greetings.
- File: `server_test.py`

### 5. Configuration
- Configured multiple MCP servers in `claude_desktop_config.json` for easy execution.
- Added support for Redis, PostgreSQL, and weather API servers.

### 6. Environment Setup
- Added `.venv` to `.gitignore` to exclude the virtual environment from version control.
- Configured environment variables for database connection in `.env` file.

## Dependencies
The project uses the following dependencies:
- `httpx`
- `mcp[cli]`
- `redis`
- `psycopg[binary]`
- `modelcontextprotocol`

## How to Run
1. Set up the required environment variables in the `.env` file.
2. Use the commands in `claude_desktop_config.json` to run the desired MCP server.
3. For example, to run the Redis server:
   ```bash
   uv run --with mcp[cli] mcp run mcp_redis_server.py
   ```

## Future Work
- Add more tools and resources to the MCP servers.
- Improve error handling and logging.
- Explore additional integrations with other databases and APIs.
