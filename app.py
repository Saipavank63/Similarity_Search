from fastapi import FastAPI, HTTPException, status
from typing import List
import pandas as pd

from SAP_Take_Home_Challenge_Model_Build import find_similar_products

app = FastAPI()

@app.get("/find_similar_products")
def get_similar_products(product_id: str, num_similar: int) -> List[str]:
    try:
        #validate input parameters
        if not product_id:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Product ID cannot be empty")
        if num_similar <= 0:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Number of similar products must be greater than 0")
    
        similar_products = find_similar_products(product_id, num_similar)

        if not similar_products:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No similar products found")
        
        return similar_products
    
    except KeyError:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Product ID not found")
    except ValueError as ve:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = str(ve))
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
