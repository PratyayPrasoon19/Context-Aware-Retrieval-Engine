
### Similarity Metric Choice

**Cosine Similarity** is used because:
- Embeddings are normalized, making cosine similarity equivalent to dot product in FAISS.
- Cosine is better suited for high-dimensional text embeddings because it measures angular similarity rather than raw distance.
- It reduces the impact of vector magnitude and focuses on semantic direction.
- It is the standard choice for text retrieval and semantic search tasks.

**Euclidean Distance** is less ideal for this use case because:
- It is sensitive to vector magnitude differences unless embeddings are carefully normalized.
- In high dimensions, Euclidean distance can become less meaningful and harder to compare.
- Cosine similarity better captures semantic closeness for text embeddings.