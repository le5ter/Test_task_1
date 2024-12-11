FROM python:3.10
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "services.line_provider:app", "--host", "0.0.0.0", "--port", "8000"]
