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
        
        _pool = await asyncpg.create_pool(
            database_url,
            min_size=5,
            max_size=20,
            command_timeout=60,
            server_settings={
                'search_path': f"{env.get('DB_SCHEMA', 'confessions')}, public"
            }
        )
    
    return _pool

async def query(sql: str, *args):
    """Execute a query and return results"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(sql, *args)

async def execute(sql: str, *args):
    """Execute a query without returning results"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(sql, *args)

async def fetchrow(sql: str, *args):
    """Fetch a single row"""
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(sql, *args)

async def close_pool():
    """Close the database connection pool"""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

