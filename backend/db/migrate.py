import asyncpg
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def migrate():
    """Run the database migration"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    # Connect to database
    conn = await asyncpg.connect(database_url)
    
    try:
        # Read schema file
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        await conn.execute(schema_sql)
        
        print("✅ Migration completed successfully!")
        print("   - Created schema: confessions")
        print("   - Created table: confessions")
        print("   - Created indexes and triggers")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(migrate())
