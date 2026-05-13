# Retrieval Benchmark

This file captures the sample results comparing Strategy A (Raw Vector Search) and Strategy B (AI-Enhanced Retrieval with query enhancement).

## Sample Query Comparison

| Query | Strategy A score | Strategy B score | Improvement |
|---|---|---|---|
| How does the system handle peak delivery demand? | 0.5354 | 0.7009 | +0.1655 |
| What happens if a warehouse becomes overloaded | 0.5329 | 0.6953 | +0.1624 |
| How are fleet resources dynamically allocated during demand surges | 0.5470 | 0.6455 | +0.0985 |
| How does the system maintain real-time shipment visibility | 0.4581 | 0.6496 | +0.1915 |
| How are API overloads and traffic spikes handled | 0.4722 | 0.6194 | +0.1472 |
| How does the system maintain synchronization across distributed regions | 0.4384 | 0.6259 | +0.1875 |

### Average Improvement

- Average Strategy B improvement over Strategy A: **+0.1588**

## Notes

- Strategy A uses the original query directly for vector embedding and search.
- Strategy B applies query enhancement before embedding, improving semantic retrieval alignment with the logistics knowledge base.
