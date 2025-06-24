import streamlit as st
import requests

def main():
    st.title("Product Similarity Finder")

    product_id = st.text_input("Enter Product ID:")
    num_similar = st.number_input("Enter number of similar products:", min_value=1, step=1)

    if st.button("Find Similar Products"):
        if product_id:
            try:
                response = requests.get(f"http://127.0.0.1:8000/find_similar_products", params={"product_id": product_id, "num_similar": num_similar})
                response.raise_for_status()
                similar_products = response.json()
                st.write(f"Similar Products for {product_id}:")
                for product in similar_products:
                    st.write(product)
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred: {http_err}")
            except Exception as err:
                st.error(f"Other error occurred: {err}")
        else:
            st.warning("Please enter a Product ID")

if __name__ == "__main__":
    main()