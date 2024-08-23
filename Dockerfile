# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Scrapy project into the container
COPY . .

# Set the entrypoint for the container to run the Scrapy spider
ENTRYPOINT ["scrapy", "crawl"]

CMD ["yok_spider" , "-o" , "results.json"]
