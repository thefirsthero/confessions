from os import environ as env
import asyncpg
from typing import Optional

# Database connection pool
_pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    """Get or create database connection pool"""
    global _pool
    
    if _pool is None:
        database_url = env.get('DATABASE_URL')
        
        if not database_url:
            raise RuntimeError("Missing DATABASE_URL environment variable")
        
        async def init_connection(conn):
            """Initialize connection with search_path for Neon compatibility"""
            await conn.execute(f"SET search_path TO {env.get('DB_SCHEMA', 'confessions')}, public")
        
        _pool = await asyncpg.create_pool(
            database_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
            statement_cache_size=0,  # Disable statement caching for Neon pooler compatibility
            init=init_connection
        )
    
    return _pool

async def query(sql: str, *args):
    """Execute a query and return results"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(f"SET search_path TO {env.get('DB_SCHEMA', 'confessions')}, public")
        return await conn.fetch(sql, *args)

async def execute(sql: str, *args):
    """Execute a query without returning results"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(f"SET search_path TO {env.get('DB_SCHEMA', 'confessions')}, public")
        return await conn.execute(sql, *args)

async def fetchrow(sql: str, *args):
    """Fetch a single row"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(f"SET search_path TO {env.get('DB_SCHEMA', 'confessions')}, public")
        return await conn.fetchrow(sql, *args)

async def close_pool():
    """Close the database connection pool"""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

