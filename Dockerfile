# Use the official Ollama base image
FROM ollama/ollama

# Expose the Ollama API port
EXPOSE 11434

# Start Ollama when the container runs
CMD ["ollama", "serve"]
