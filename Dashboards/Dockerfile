FROM python:3.11-slim
WORKDIR /app
COPY Dashboards/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY Dashboards/ ./Dashboards/
COPY shared/ ./shared/
ENV PYTHONPATH=/app
EXPOSE 8501
CMD ["streamlit", "run", "Dashboards/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
