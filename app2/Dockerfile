# FROM python:3.9-slim

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# COPY app2.py app2.py
# COPY alert.py alert.py
# COPY templates/ templates/

# CMD ["python", "app2.py"]


FROM python:3.9-slim

WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do aplicativo e os templates
COPY app2.py app2.py
COPY templates/ templates/

# Expõe a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar o aplicativo
CMD ["python", "app2.py"]
