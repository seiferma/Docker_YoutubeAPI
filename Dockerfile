FROM python:3-alpine

WORKDIR /app

# Install requirements
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

# Add application
ADD app.py .

# Expose port
EXPOSE 5000

# Start webserver
CMD ["waitress-serve", "--port=5000", "app:app"]