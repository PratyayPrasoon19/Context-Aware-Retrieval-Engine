def query_expansion(query):
    """
    Simulates query expansion. In a real scenario, you might use an LLM 
    to generate synonyms or related technical terms.
    """
    # Example: Simple rule-based expansion for logistics
    expansions = {
        "shipping": "shipping freight transport delivery",
        "delay": "delay late arrival disruption bottleneck",
        "warehouse": "warehouse storage inventory fulfillment center"
    }
    
    expanded_query = query
    for word, syn in expansions.items():
        if word in query.lower():
            expanded_query += f" {syn}"
            
    print(f"DEBUG: Expanded query to: '{expanded_query}'")
    return expanded_query