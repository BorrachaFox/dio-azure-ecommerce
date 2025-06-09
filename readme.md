# E-commerce Azure - Cadastro de Produtos

Este projeto é uma aplicação web para cadastro e listagem de produtos, utilizando Streamlit, Azure Blob Storage e SQL Server hospedado no Azure.

## Funcionalidades

- Cadastro de produtos com nome, preço, descrição e imagem.
- Upload de imagens para o Azure Blob Storage.
- Armazenamento das informações dos produtos em um banco SQL Server.
- Listagem dos produtos cadastrados com exibição das imagens.

## Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/)
- [Azure SQL Database](https://azure.microsoft.com/en-us/products/azure-sql/)
- [Python](https://www.python.org/)

## Estrutura do Projeto

- `main.py` — Código principal da aplicação Streamlit.
- `requirements.txt` — Dependências do projeto.
- `.env.example` — Exemplo de configuração de variáveis de ambiente.
- `info.txt` — Script SQL para criação da tabela de produtos.

## Passos de Configuração no Azure

### 1. Criar Grupo de Recursos

No portal Azure, crie um Resource Group, por exemplo:  
`LAB-DIO-ECOMMERCE`

### 2. Criar Azure SQL Database

- Crie um servidor SQL e um banco de dados.
- Anote o nome do servidor, banco, usuário e senha.
- Libere o acesso ao seu IP nas configurações de firewall do SQL Server.

### 3. Criar Azure Blob Storage

- Crie uma conta de armazenamento e um container (por exemplo: `produtos`).
- Anote a connection string da conta de armazenamento.

### 4. Criar a Tabela no Banco de Dados

No Azure SQL, execute o script abaixo (corrija os erros de digitação do arquivo `info.txt`):

```sql
CREATE TABLE Produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(255),
    descricao NVARCHAR(MAX),
    preco DECIMAL(18, 2),
    imagem_url NVARCHAR(2083)
)
```
