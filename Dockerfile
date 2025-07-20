# Dockerfile
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta que o Flask usará
EXPOSE 5000

# Comando para rodar o app
CMD ["flask", "run", "--host=0.0.0.0"]
