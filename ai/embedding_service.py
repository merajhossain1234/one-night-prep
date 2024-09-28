from sentence_transformers import SentenceTransformer, util

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text):
    # Generate the embedding for the provided text
    embedding = model.encode(text).tolist()  # Convert to list to make it JSON serializable
    return embedding

def compute_similarity(embedding1, embedding2):
    # Compute cosine similarity using Sentence Transformers' util
    similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return similarity.item()  # Return as a scalar value