from src.database import localSession
from src.models.product import ProductTable

db = localSession()

sample = ProductTable(name="Macbook", price=22500.00)
db.add(sample)
db.commit()
db.close()

print("Sample inserted Successfully")
