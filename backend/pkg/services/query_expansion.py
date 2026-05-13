
import google.generativeai as genai
from config.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def query_expansion_heuristic(query: str) -> str:
    """
    Strategy B: Contextual Bridge Expansion.
    Uses 'Keyphrase Injection' to align the query vector with 
    the technical density of the logistics document.
    """
    query_lower = query.lower()

    # Dictionary of "Vector Magnets" - these are the exact technical 
    # phrases from your paragraphs.
    knowledge_map = {
        "peak": "seasonal demand spikes cargo capacity reallocation horizontal scaling nodes backlog prevention",
        "load": "seasonal demand spikes cargo capacity reallocation horizontal scaling nodes backlog prevention",
        "delivery": "last-mile route optimization delivery orchestration adaptive routing traffic density driver proximity",
        "route": "last-mile route optimization delivery orchestration adaptive routing traffic density driver proximity",
        "customs": "automated customs clearance validation pipelines manifest verification tax declarations cross-border",
        "tracking": "real-time shipment tracking GPS telemetry barcode scanning event-driven processing transit hubs",
        "warehouse": "warehouse queue balancing processing lanes bottleneck prevention conveyor systems scanning stations",
        "api": "API traffic protection rate limiting request throttling gateway clusters flash sale campaigns",
        "priority": "priority shipment dispatching medical supplies high-value electronics mission-critical",
        "forecast": "demand forecasting machine learning capacity planning historical shipment volume"
    }

    # Find matches
    expansion_parts = []
    for key, phrases in knowledge_map.items():
        if key in query_lower:
            expansion_parts.append(phrases)

    if not expansion_parts:
        # Fallback to a domain-wide technical context
        expansion = "logistics infrastructure operational data synchronization distributed databases"
    else:
        expansion = " ".join(expansion_parts)

    # REFINEMENT: Instead of adding the query, return ONLY the dense keywords.
    # This removes the "noise" of the original query and focuses 100% on the semantic target.
    return f"{query} {expansion}"


def query_expansion_llm(query: str) -> str:
    """
    Strategy B: AI-Enhanced Retrieval.
    Uses Gemini to expand the query into a technically dense 
    Hypothetical Document (HyDE).
    """
    
    prompt = f"""
    You are an AI assistant optimizing search queries for a logistics RAG system.
    The user is asking: "{query}"
    
    Rewrite this query into a short paragraph (2-3 sentences) that 
    predicts what a technical answer would look like in the knowledge base.
    Use terms like 'latency', 'throughput', 'scaling', and 'optimization'.
    Return ONLY the rewritten paragraph.
    """
    
    try:
        response = model.generate_content(prompt)
        expanded_query = response.text.strip()
        print(f"[DEBUG] Gemini Expansion: {expanded_query}")
        return expanded_query
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        # Fallback to original query if API fails
        return query