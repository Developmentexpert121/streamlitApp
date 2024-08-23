import weaviate

# Create a client instance
client = weaviate.Client("http://localhost:8501")  # Replace with your Weaviate instance URL

# Check if connection is successful
print("Connected to Weaviate:", client.is_ready())