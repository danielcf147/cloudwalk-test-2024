# FROM python:3.9-slim

# WORKDIR /app

# # Copia o arquivo de requisitos e instala as dependências
# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Copia o código do aplicativo e os templates
# COPY app1.py app1.py
# COPY templates/ templates/

# # Comando para iniciar o aplicativo
# CMD ["python", "app1.py"]

FROM python:3.9-slim

WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do aplicativo e os templates
COPY app1.py app1.py
COPY templates/ templates/

# Expõe a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar o aplicativo
CMD ["python", "app1.py"]
