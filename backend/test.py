from app.database.connection import SessionLocal


try:
    db = SessionLocal()
    print("Database session created successfully!")

    db.close()
    print("Database session closed successfully!")

except Exception as e:
    print("Database session failed!")
    print(e)