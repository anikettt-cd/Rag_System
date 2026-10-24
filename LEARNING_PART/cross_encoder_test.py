from sentence_transformers import CrossEncoder


model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

query = "What is the role of the application layer in an IoT system?"

chunks = [
    "The application layer serves as the user interface to the IoT system. It allows users to monitor the system's status, control devices, and visualize or analyze data.",
    "The perception layer consists of sensors and actuators that collect information from the physical environment.",
    "The transport layer is responsible for transmitting collected data between different components of the IoT system.",
]

pairs = [(query, chunk) for chunk in chunks]

scores = model.predict(pairs)

for chunk, score in zip(chunks, scores):
    print(f"\nScore: {score:.4f}")
    print(chunk)