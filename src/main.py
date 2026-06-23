from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, get_db
from .models.product import ProductTable

from sqlalchemy.orm import Session
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

Base.metadata.create_all(bind=engine)
print("Product Table created Successfully")

@app.get('/api/get_products')
def get_products(db : Session=Depends(get_db)):
    products = db.query(ProductTable).all()
    return {
        "Products":[
            {
                "id" : i.id,
                "name" :i.name,
                "price" : i.price
            }
            for i in products
        ]
    }