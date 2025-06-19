from db.database import engine
from db import models  # This imports all models so their tables are registered

# Create tables
models.Base.metadata.create_all(bind=engine)

print("✅ Tables created in devradar.db")
