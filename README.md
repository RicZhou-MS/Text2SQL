# Chat to SQL

This project is made to demo Azure openAI capability (gpt-4, gpt-turbo, gpt-4-32k) for text to SQL. It can grab DB schema (table and columns) from specific SQL database for composing appropriate prompt. The streamlit GUI supports user to ask question, and then it calles GPT to return SQL statement based on DB table definition for user question. it supports multi turn conversation.
![image](https://user-images.githubusercontent.com/75886466/235889811-72df9218-b64a-467d-b89d-9c73d5346aee.png)

## Prepare Azure SQL DB
1. Prepare your existing business Azure SQL DB, or [create a sample Azure SQL database](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms#deploy-new-sample-database) for demo
2. Collect the SQL DB server name, database name, user and password for later use
3. Make sure your SQL DB firewall settings allow access from your application

## Application Installation
1. Install Python runtime (This repo is developed with Python 3.11.2)
2. Clone the project onto your local, install the python dependencies:
```
pip install -r ./requirements.txt
```
3. Create your Azure OpenAI service and get your `OPENAI_API_BASE` and `OPENAI_API_KEY`.
4. [Deploy OpenAI models](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model), deploy one of or all of these three models (`gpt-4` and `gpt-4-32k`, `gpt-35-turbo`). if your gpt model deployment name is different, you need to change the source code at function `Initialize_SideBar()` of file `Chat_to_SQL.py` accorddingly.
5. Create a .env file at the project folder, and provide all necessary environment variables you get from above steps as below example.
```
OPENAI_API_KEY=00000000000000000000000000000000
OPENAI_BASE=https://<youroai>.openai.azure.com/
DB_SERVER=<your Azure SQL DB server name, e.g contoso.database.windows.net>
DB_NAME=<your Azure SQL DB database name, e.g. AdventureWorks>
DB_USER=<your Azure SQL DB user name>
DB_USER_PASS=<your Azure SQL DB user password>
```

## Prepare DB Schema
1. Open your project folder with VS code
2. Run `ExportDBSchema.py`, it will access your Azure SQL DB and grab all tables and columns, the table definition will be saved as `DBSchema.txt` at same folder.

## Run Application
**Option 1 - Run locally**: Run command `streamlit run Chat_to_SQL.py`, it will start browser and access corresponding url automatically.

**Option 2 - Run inside Azure VM**: If you host the application inside an Auzre IaaS VM which has public IP attached, you can use `streamlit run .\Chat_to_SQL.py --server.headless=true` to start the application with internet accessible via the public IP. 

**Option 3 - Run with github codespace**: If you run the application with Github codespace, you can use `streamlit run Chat_to_SQL.py --server.enableCORS=false --server.enableXsrfProtection=false`
**NOTE:** When using github codespace, follow [the KB](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces) to configure predefined dev container. and alos follow [this](https://github.com/mkleehammer/pyodbc/wiki/Install#debian-stretch) to install pyodbc dependency in Linux environment.

**Option 4**: You can search and refer to articles on internet if you want to publish streamlit to Azure app service or other hostings.
