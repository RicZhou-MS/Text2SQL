# "build a Docker image from a Dockerfile, assume the Dockerfile is in the current directory, assume docker desktop is running at localhost"
# docker build ./ -t rz-txt2sql-azure-openai:0.1
# docker run -it --name txt2sql-azure-openai -p80:80 rz-txt2sql-azure-openai:0.1

# "login to Azure Container Registry"
# docker login -u <user> -p <password> acr0612.azurecr.cn
# "create a new tag for a Docker image with repository name"
# docker tag rz-txt2sql-azure-openai:0.1 acr0612.azurecr.cn/rz-txt2sql-azure-openai:0.1
# "push a Docker image to a container registry"
# docker push acr0612.azurecr.cn/rz-txt2sql-azure-openai:0.1

# "create Azure app service and choose linux docker container"
# "choose above container registry and image, linux docker by default uses 80 port"

FROM python:3.11 

WORKDIR /usr/src/app 

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    unzip \
    unixodbc \
    unixodbc-dev 

# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql17
RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

CMD [ "streamlit", "run", "./Chat_to_SQL.py", "--server.port", "80"]
