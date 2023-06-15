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

COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt 

COPY . . 

CMD [ "streamlit", "run", "./Chat_to_SQL.py", "--server.port", "80"]
