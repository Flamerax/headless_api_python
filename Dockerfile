FROM python:3.11-slim

# Instala dependências + Chromium + driver + nano
RUN apt-get update && apt-get install -y \
    nano \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libu2f-udev \
    libvulkan1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Define variável de ambiente para o Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/lib/chromium/

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos da aplicação
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir flask selenium

# Expõe a porta da API
EXPOSE 5000

# Comando padrão
CMD ["python", "api.py"]
