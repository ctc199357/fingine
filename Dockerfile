# Use an official Python runtime as the base image
FROM python:3.10
EXPOSE 8501
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
ENTRYPOINT [ "streamlit", "run" ]
# Run streamlit when the container launches
CMD ["Main_Page.py"]    