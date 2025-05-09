# Используем официальный образ Python
FROM python:3.11-slim

# Принудительно обновляем index и ставим gcc (нужно для pkg_resources, setuptools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем код
COPY . /app

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir \
    pandas \
    networkx \
    pyvis \
    jinja2

# UTF-8 по-умолчанию
ENV PYTHONIOENCODING=utf-8

CMD ["python", "graph.py"]
