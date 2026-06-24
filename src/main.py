from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import Client, create_client
from dotenv import load_dotenv
import os
import stripe 


app = FastAPI()

load_dotenv()
 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


supabase : Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
stripe.api_key = STRIPE_SECRET_KEY

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get('/')
def root():
    return { "status" : "ok", "message" : "E-commerce backend running"}

# ----- Products---
@app.get('/api/products')
def get_products():
    print(supabase.table("products").select("*").execute())
    response = supabase.table("products").select("*").order("id").execute()
    return response.data

@app.get("/api/products/{product_id}")
def get_product(product_id : int):
    response = supabase.table("products").select('*').eq("id", product_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Product not found")
    return response.data;

#---- Checkout ---

class CheckOutRequest(BaseModel):
    product_id : int
    quantity : int = 1

@app.post('/api/create-checkout-session')
def create_checkout_session(req: CheckOutRequest):
    product_response = supabase.table('products').select('*').eq("id", req.product_id).execute()
    product = product_response.data

    if not product :
        raise HTTPException(status_code=404, detail="Product not Found")
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items =[
                {
                    "price_data" : {
                        "currency" : "usd",
                        "product_data" : {
                            "name" : product["name"],
                            "images" : [product['image_url']] if product.get('image_url') else []
                        },
                        "unit_amount" : int(float(product['price']) * 100),
                    },
                    "quatity" : req.quantity,
                }
            ],
            mode = 'payment',
            success_url = f'{FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url = f'{FRONTEND_URL}/cancel'
        )
        return {"checkout_url" : session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


