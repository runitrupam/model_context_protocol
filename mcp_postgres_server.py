from mcp.server.fastmcp import FastMCP
import psycopg
import asyncio
import urllib.parse
import os
from typing import Optional, Dict, List, AsyncIterator
import json
from contextlib import asynccontextmanager


async def get_schema_info(conn: psycopg.AsyncConnection) -> str:
    """Get database schema information including tables and their columns"""
    schema_info: Dict[str, List[Dict]] = {"tables": []}
    
    async with conn.cursor() as cur:
        # Get all tables
        await cur.execute("""
            SELECT 
                table_name,
                table_schema
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """)
        tables = await cur.fetchall()

        for table in tables:
            table_name = table[0]
            schema_name = table[1]
            
            # Get columns for each table
            await cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
            """, (table_name, schema_name))
            
            columns = await cur.fetchall()
            table_info = {
                "table_name": table_name,
                "schema": schema_name,
                "columns": [
                    {
                        "name": col[0],
                        "type": col[1],
                        "nullable": col[2] == "YES",
                        "default": col[3]
                    }
                    for col in columns
                ]
            }
            schema_info["tables"].append(table_info)

    return json.dumps(schema_info, indent=2)


# Create an MCP server
mcp = FastMCP("PostgreSQL Database")

conn: Optional[psycopg.AsyncConnection] = None

@mcp.resource("db://schema")
async def schema() -> str:
    """Get the database schema information"""
    global conn
    if not conn:
        raise RuntimeError("Database connection not initialized")
    return await get_schema_info(conn)

@mcp.resource("store://{key}")
async def get_store(key: str) -> Optional[str]:
    """Get a value from the MCP store"""
    global conn
    if not conn:
        raise RuntimeError("Database connection not initialized")
    async with conn.cursor() as cur:
        await cur.execute("SELECT value FROM mcp_store WHERE key = %s", (key,))
        result = await cur.fetchone()
        return result[0] if result else None

@mcp.tool()
async def set_store(key: str, value: str) -> None:
    """Store a value in the MCP store"""
    global conn
    if not conn:
        raise RuntimeError("Database connection not initialized")
    async with conn.cursor() as cur:
        await cur.execute("""
            INSERT INTO mcp_store (key, value) 
            VALUES (%s, %s)
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
        """, (key, value))
    await conn.commit()

@asynccontextmanager
async def lifespan(_) -> AsyncIterator[None]:
    """Handle database connection lifecycle"""
    global conn
    try:
        # Get database URL from environment variable
        database_url = os.environ.get("DATABASE_URI")
        if not database_url:
            raise RuntimeError(
                "DATABASE_URI environment variable not set. Please configure it in your claude_desktop_config.json"
            )
        
        print("Attempting database connection...")
        conn = await psycopg.AsyncConnection.connect(database_url)
        print("Database connection established successfully")
        
        # Create MCP store table if it doesn't exist
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS mcp_store (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
        await conn.commit()
        
        yield
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        conn = None  # Ensure conn is None on failure
        raise
    finally:
        if conn:
            try:
                await conn.close()
                print("Database connection closed")
            except Exception as e:
                print(f"Error closing connection: {str(e)}")
            conn = None

# Set up the lifespan handler
mcp.lifespan_context = lifespan

if __name__ == "__main__":
    mcp.run()
    

# conn_params = {
#     'dbname': urllib.parse.quote_plus('postgres'),
#     'user': 'atlas',
#     'password': urllib.parse.quote_plus('new_password'),  # Updated password
#     'host': os.environ.get('SQL_HOST', '0.0.0.0'),
#     'port': os.environ.get('SQL_PORT', '5432'),
# }
# conn_string = f"postgresql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{conn_params['dbname']}"
