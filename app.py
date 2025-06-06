# app.py

import os
from flask import Flask, request, render_template, redirect
from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from db import insert_metadata

app = Flask(__name__)
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file, overwrite=True)
        url = blob_client.url
        insert_metadata(file.filename, url)
        return redirect('/view')
    return render_template('index.html')

@app.route('/view')
def view_files():
    blobs = container_client.list_blobs()
    return render_template('view.html', blobs=blobs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
