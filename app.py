import os
import httpx
import streamlit as st
import asyncio
import pandas as pd
import io  
from dotenv import load_dotenv
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
api_key = os.getenv("api_key")
search_engine_id = os.getenv("search_engine_id")

async def google_search(api_key, search_engine_id, query, **params):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "searchType": "image",
        **params
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()
    
def run_search(description):
    # results = asyncio.run(google_search(api_key, search_engine_id, query))
    url= "https://admin-apis.isometrik.io/v1/gptChatMsg/"
    payload= json.dumps(
      {
          "session_id": "1735909520932",
          "agent_id": "675bd8da356683fa5bc0731f",
          "message": description,
          "file": ""
      })
    headers = {
                'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJfQUpybXA5cktvcDliZEl4NUNzaEJOUHNCWWNGMTlsWlMzWnBVa1UxUkRVIn0.eyJleHAiOjE3MzU5ODIzMzAsImlhdCI6MTczNTg5NTkzMCwianRpIjoiYWJhNzZkYzYtNzI5Zi00YjllLTgwMmYtZGMxNTEzNWI1NGU1IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5pc29tZXRyaWsuaW8vcmVhbG1zL21hc3RlciIsImF1ZCI6WyI2NzViZDI3MjA3ZjA3ZmY5MjY5MDIzYTdfYXBpLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNDYzNjE3YjctZjJkYi00NDU5LTk2MDUtZDgzMTE0ZGY2YmY1IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiNjc1YmQyNzIwN2YwN2ZmOTI2OTAyM2E3X2FwaS1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiMGNhY2NmZjUtY2M5Ny00NTA1LWI3MGYtYjQxZWMxY2UxYWY3IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2tleWNsb2FrLmlzb21ldHJpay5pbyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiNjc1YmQyNzIwN2YwN2ZmOTI2OTAyM2E3X2FwaS1jbGllbnQiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlLXJlYWxtLW1hc3Rlci1BY2Nlc3MiLCJ1bWFfcHJvdGVjdGlvbiIsIkFkbWluIiwiRGVmYXVsdC1hcHBsaWNhdGlvbi1yb2xlIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiMGNhY2NmZjUtY2M5Ny00NTA1LWI3MGYtYjQxZWMxY2UxYWY3IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJOZWV0aGEgLCIsInByZWZlcnJlZF91c2VybmFtZSI6Im5lZXRoYUBhcHBzY3JpcC5jbyIsImdpdmVuX25hbWUiOiJOZWV0aGEiLCJmYW1pbHlfbmFtZSI6IiwiLCJlbWFpbCI6Im5lZXRoYUBhcHBzY3JpcC5jbyJ9.OizsQun_6ajOVF_5ubKhQ047z11h-9PFagtjCS0HIEUEICab6dfDcnmQ-e1yLlbeQl7jK1KFyWqF4Mc5Lp5sl3z7XrUVfbBGF_lB6V0CTFfqFzsR-3Os8Te-3qSx65U_iLc70z1L7RXNMzbSr7cWn2y_Kr_RBC0hQfuH68Ie3yYTmGFjU7rLZLU7mB4_HcacfAVbtyy8yep2kCAhpBDNtvzlUTI7pAdUDZVZXqnF4elI4LnHOnMrNxu3Au4HGtKAKDNTr0eZKIOK33109xqAquhB4ddDSTS3wwVK5o1-Wy0nHaoJZYe63tXQXJhrEC6Ha9czyj5fgcGnqkwGOcWliA',
                'Content-Type': 'application/json' 
              }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        try:
            return response.json()['text']  # Attempt to parse JSON
        except json.JSONDecodeError as e:
            logger.info(f"JSON decode error: {e}")
            print(f"JSON decode error: {e}")  # Print the error
            return ""
    else:
        logger.info(f"Error: {response.status_code}, Response: {response.text}")  # Log the response text for debugging
        print(f"Error: {response.status_code}, Response: {response.text}")  # Print the error
        return ""

def main():
    st.title("Google Image Search")
    excel_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    if excel_file is not None:
        # Delete all files in the uploads directory
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove the existing file

        # Save the uploaded file
        file_path = os.path.join(uploads_dir, excel_file.name)
        with open(file_path, "wb") as f:
            f.write(excel_file.getbuffer())  # Write the new file
        logger.info(f"File name: {excel_file.name}, File type: {excel_file.type}, File size: {excel_file.size}")
        print(f"File name: {excel_file.name}, File type: {excel_file.type}, File size: {excel_file.size}")  # Print file info

        # List available sheets
        excel_file_obj = pd.ExcelFile(file_path)  # Create an ExcelFile object
        sheet_names = excel_file_obj.sheet_names  # Get the list of sheet names
        logger.info(f"Available sheets: {sheet_names}")  # Log available sheets
        print(f"Available sheets: {sheet_names}")  # Print available sheets

        # Dropdown for selecting the sheet
        selected_sheet = st.selectbox("Select a sheet to read from:", sheet_names)

        if st.button("Add Image URL"):
            if selected_sheet:  # Check if a sheet is selected
                df = pd.read_excel(file_path, engine='openpyxl', sheet_name=selected_sheet)  # Reads the specified sheet
                logger.info(f"Reading data from sheet: {selected_sheet}")
                print(f"Reading data from sheet: {selected_sheet}")  # Print the sheet being read

                # Check if 'Description' column exists
                if 'Description' not in df.columns:
                    error_message = "Error: 'Description' column not found in the selected sheet."
                    logger.info(error_message)
                    print(error_message)  # Print the error
                    st.error(error_message)  # Display error in Streamlit
                    return  # Exit the function if the column is missing

                image_urls = []  # Use a list to store image URLs for each row
                for description in df['Description']:  # Assuming the column with descriptions is named 'Description'
                    results = run_search(description) 
                    try:
                        results = json.loads(results)  # Search for each description
                        logger.info(f"Results for description '{description}': {results}")
                        print(f"Results for description '{description}': {results}")  # Print results
                        if isinstance(results, list):
                            urls = [item['s3_bucket_image_url'] for item in results]
                            image_urls.append('\n'.join(urls))  # Append the joined URLs with newline to the list
                        else:
                            image_urls.append('')  # Append an empty string if no results
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.info(f"Error processing results for description '{description}': {e}")
                        print(f"Error processing results for description '{description}': {e}")  # Print error
                        image_urls.append('')  # Append an empty string in case of an error
                logger.info(f"Image URLs: {image_urls}")  # Log the last URL processed
                print(f"Image URLs: {image_urls}")  # Print the last URL processed

                # Assign the list of image URLs to the new column in the DataFrame
                df['Image URL'] = image_urls  # Add the new column with image URLs

                # Save the updated DataFrame back to the Excel file
                output_file_path = "updated_" + excel_file.name
                output = io.BytesIO()
                df.to_excel(output, index=False, engine='openpyxl')  # Save the updated DataFrame to the BytesIO object
                output.seek(0)  # Move the cursor to the beginning of the BytesIO object

                # Provide a download button for the updated Excel file
                st.download_button(
                    label="📥 Download Updated Excel File",
                    data=output,
                    file_name="updated_image_urls.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                st.success("Image URLs added. You can download the updated file.")

if __name__ == "__main__":
    main() 