import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()
BlobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobaccountName = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')

st.title("Cadastro de Produtos")

# FORM | CADASTRO DE PRODUTOS
product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

# SAVE IMAGE TO BLOB STORAGE
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)

    try:
        blob_client.upload_blob(file.read(), overwrite=True)
        return f"https://{blobaccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    except Exception as e:
        st.error(f"Erro ao enviar a imagem: {e}")
        return None

def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)  # Upload the image to Blob Storage
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Produtos (nome, preco, descricao, imagem_url) VALUES (%s, %s, %s, %s)",
                       (product_name, product_price, product_description, image_url))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir produto no banco de dados: {e}")

def list_products():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

def list_products_screen():
    products = list_products()
    if products:
        for product in products:
            st.write(f"**Nome:** {product[1]}")
            st.write(f"**Preço:** R$ {product[2]}")
            st.write(f"**Descrição:** {product[3]}")
            st.image(product[4], use_container_width=True)
            st.markdown("---")
    else:
        st.write("Nenhum produto cadastrado.")

if st.button("Cadastrar Produto"):
    if insert_product(product_name, product_price, product_description, product_image):
        st.success("Produto cadastrado com sucesso!")

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_products_screen()