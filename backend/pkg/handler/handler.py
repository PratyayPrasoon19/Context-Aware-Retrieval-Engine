from pkg.services.query_expansion import query_expansion
from pkg.services.rag_pipeline import retrieval_pipeline

def handle_search_request(request_data):
    """
    Handler for benchmarking search requests.
    Executes both Strategy A (Standard) and Strategy B (Expanded) 
    and returns a structured comparison JSON.
    """
    query = request_data.get('query', '')
    
    if not query:
        return {"error": "Query is required"}, 400

    # 1. Strategy A: Standard Retrieval
    standard_results = retrieval_pipeline(query)
    
    # 2. Strategy B: AI-Enhanced (Expanded) Retrieval
    expanded_query = query_expansion(query)
    expanded_results = retrieval_pipeline(expanded_query)

    # 3. Format Response to requested JSON Schema
    response_payload = {
        "query": query,
        "result": [
            {
                "type": "regular_result",
                "response": [
                    {
                        "query": res["chunk"], 
                        "rank": i + 1, 
                        "score": round(res["score"], 4)
                    } for i, res in enumerate(standard_results)
                ]
            },
            {
                "type": "expanded_result",
                "response": [
                    {
                        "query": res["chunk"], 
                        "rank": i + 1, 
                        "score": round(res["score"], 4)
                    } for i, res in enumerate(expanded_results)
                ]
            }
        ]
    }

    return response_payload, 200