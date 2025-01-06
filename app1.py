import os
import httpx
import streamlit as st
import asyncio
import pandas as pd
import json
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("api_key")
search_engine_id = os.getenv("search_engine_id")

# Asynchronous function for Google Search
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

# Function to make the POST request

def run_search(description):
    url = "https://admin-apis.isometrik.io/v1/gptChatMsg/"
    payload = json.dumps({
        "session_id": "1736157963482",
        "agent_id": "675bd8da356683fa5bc0731f",
        "message": description,
        "file": ""
    })
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJfQUpybXA5cktvcDliZEl4NUNzaEJOUHNCWWNGMTlsWlMzWnBVa1UxUkRVIn0.eyJleHAiOjE3MzYyMjQyOTUsImlhdCI6MTczNjEzNzg5NSwianRpIjoiZGU1MDBkYWMtODgxZS00MjBkLThlNGMtZmI1Y2ZmNDdiM2QxIiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5pc29tZXRyaWsuaW8vcmVhbG1zL21hc3RlciIsImF1ZCI6WyI2NzViZDI3MjA3ZjA3ZmY5MjY5MDIzYTdfYXBpLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNDYzNjE3YjctZjJkYi00NDU5LTk2MDUtZDgzMTE0ZGY2YmY1IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiNjc1YmQyNzIwN2YwN2ZmOTI2OTAyM2E3X2FwaS1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiZjg0NWY2ZDMtMmU5Yi00YjRmLWIyZTEtNWNlMDZhZDJjNmMzIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2tleWNsb2FrLmlzb21ldHJpay5pbyJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiNjc1YmQyNzIwN2YwN2ZmOTI2OTAyM2E3X2FwaS1jbGllbnQiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlLXJlYWxtLW1hc3Rlci1BY2Nlc3MiLCJ1bWFfcHJvdGVjdGlvbiIsIkFkbWluIiwiRGVmYXVsdC1hcHBsaWNhdGlvbi1yb2xlIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiZjg0NWY2ZDMtMmU5Yi00YjRmLWIyZTEtNWNlMDZhZDJjNmMzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJOZWV0aGEgLCIsInByZWZlcnJlZF91c2VybmFtZSI6Im5lZXRoYUBhcHBzY3JpcC5jbyIsImdpdmVuX25hbWUiOiJOZWV0aGEiLCJmYW1pbHlfbmFtZSI6IiwiLCJlbWFpbCI6Im5lZXRoYUBhcHBzY3JpcC5jbyJ9.sMywtqfd_7PmQPZu7Zal3QCd0yjIdVwnILheZo3Df-yNDgl0aUhjEl-p0CVswEqd21VGw1MQfrLOxsgvj6N4QMp2FbE9WU5EAeJGC7saItqQIY1eHB8WY-mxTkJuYN0fdDCTEGfqXVAg-e18yF7nV542SdoZeVd3lwuoNJl6uN5-3rnejRjA-Gq5AKyJi8tR07p-pAn7qwz22HTQCuImoZWWAlxa-6dHZHvIjLSuh6upeT73S2vHxvdIBJz-BMoi0k872lBVQAuiBzu6h1EKBumu9MPtkC5gVfRf_p8Vn1kmUphDJJj5A8izheTvdt_r3XtJCMe-OdpD7DTqpVAyFw',
        'Content-Type': 'application/json'
    }
    response = httpx.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        try:
            return response.json().get('text', '')  # Attempt to parse JSON
        except json.JSONDecodeError as e:
            logger.info(f"JSON decode error: {e}")
            return ""
    else:
        logger.info(f"Error: {response.status_code}, Response: {response.text}")
        return ""

# Main application function
def main():
    st.title("Google Image Search with Excel Integration")
    excel_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    if excel_file is not None:
        # Delete all files in the uploads directory
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Remove existing files

        # Save the uploaded file
        file_path = os.path.join(uploads_dir, excel_file.name)
        with open(file_path, "wb") as f:
            f.write(excel_file.getbuffer())  # Write the new file

        logger.info(f"File uploaded: {excel_file.name}")

        # Load all sheets
        excel_file_obj = pd.ExcelFile(file_path)
        sheet_names = excel_file_obj.sheet_names
        logger.info(f"Available sheets: {sheet_names}")

        # Dropdown for selecting the sheet
        selected_sheet = st.selectbox("Select a sheet to read from:", sheet_names)

        if st.button("Add Image URL"):
            # Load all sheets into a dictionary
            all_sheets = {sheet: excel_file_obj.parse(sheet) for sheet in sheet_names}

            if selected_sheet:  # Check if a sheet is selected
                df = all_sheets[selected_sheet]
                logger.info(f"Reading data from sheet: {selected_sheet}")

                # Check if 'Description' column exists
                if 'Description' not in df.columns:
                    error_message = "Error: 'Description' column not found in the selected sheet."
                    logger.info(error_message)
                    st.error(error_message)
                    return

                image_urls = []
                for description in df['Description']:
                    results = run_search(description)
                    try:
                        results = json.loads(results)
                        logger.info(f"Results for '{description}': {results}")
                        if isinstance(results, list):
                            urls = [item['s3_bucket_image_url'] for item in results][:3]
                            image_urls.append('\n'.join(urls))
                        else:
                            image_urls.append('')
                    except (json.JSONDecodeError, TypeError) as e:
                        logger.info(f"Error processing '{description}': {e}")
                        image_urls.append('')

                df['Image URL'] = image_urls
                print("11111111111",image_urls,'+++++++++++++++++++')
                # Update the modified sheet in the dictionary
                all_sheets[selected_sheet] = df

                # Write back all sheets to the Excel file
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for sheet_name, sheet_data in all_sheets.items():
                        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

                # Provide a download button for the updated Excel file
                st.download_button(
                    label="📥 Download Updated Excel File",
                    data=excel_file.getvalue(),
                    file_name=excel_file.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                st.success("Image URLs added. You can download the updated file.")

if __name__ == "__main__":
    main()
