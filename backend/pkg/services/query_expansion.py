
import google.generativeai as genai
from config.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

import google.generativeai as genai
from config.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


class MockGenerativeModel:
    """
    Mocked GenerativeModel abstraction
    simulating Vertex AI GenerativeModel behavior.
    """

    def __init__(self, model_name="gemini-2.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()


mock_llm = MockGenerativeModel()


def query_expansion_llm(query: str) -> str:
    """
    Strategy B: AI-Enhanced Retrieval

    Expands incomplete, vague, noisy, or low-context
    user queries into semantically rich retrieval-oriented queries.
    """

    prompt = f"""
You are a semantic query rewriting engine for an enterprise logistics RAG system.

Your objective:
Transform vague, incomplete, short, or low-context user queries into
embedding-optimized retrieval queries for semantic vector search.

CRITICAL REQUIREMENTS:
- Preserve the original query intent exactly
- Do NOT answer the question
- Do NOT explain anything
- Keep the output as a SEARCH QUERY, not an answer
- Output ONLY one rewritten query sentence
- Maintain high semantic similarity with enterprise logistics documentation
- Prefer operational terminology over conversational language
- Avoid generic phrases like:
  "strategies and functionalities"
  "how does the platform improve"
  "what methods are used"
- Use logistics vocabulary likely to appear in technical documentation
- Keep wording dense and retrieval-oriented
- Do NOT introduce unrelated concepts
- Preserve important user keywords where possible

QUERY EXPANSION RULES:
If the query contains concepts related to:
- peak/load/surge → include scaling, backlog, throughput, queue latency
- delivery/route → include adaptive routing, traffic density, driver proximity
- warehouse → include queue balancing, processing lanes, bottleneck prevention
- tracking → include GPS telemetry, barcode scanning, event-driven updates
- customs → include manifest verification, cross-border validation
- api → include rate limiting, throttling, gateway traffic
- forecast → include predictive demand forecasting, capacity planning

KNOWLEDGE MAP:
"peak": "seasonal demand spikes cargo capacity reallocation horizontal scaling nodes backlog prevention throughput optimization queue latency",
"load": "seasonal demand spikes cargo capacity reallocation horizontal scaling nodes backlog prevention throughput optimization queue latency",
"delivery": "last-mile route optimization delivery orchestration adaptive routing traffic density driver proximity",
"route": "last-mile route optimization delivery orchestration adaptive routing traffic density driver proximity",
"customs": "automated customs clearance validation pipelines manifest verification tax declarations cross-border",
"tracking": "real-time shipment tracking GPS telemetry barcode scanning event-driven processing transit hubs",
"warehouse": "warehouse queue balancing processing lanes bottleneck prevention conveyor systems scanning stations",
"api": "API traffic protection rate limiting request throttling gateway clusters flash sale campaigns",
"priority": "priority shipment dispatching medical supplies high-value electronics mission-critical",
"forecast": "demand forecasting machine learning capacity planning historical shipment volume"

GOOD REWRITE EXAMPLE:
User Query:
"How does the system handle peak delivery demand?"

Optimized Retrieval Query:
"How does the logistics platform handle peak delivery demand using dynamic cargo scaling, throughput optimization, queue balancing, shipment backlog prevention, and adaptive last-mile delivery orchestration?"

BAD REWRITE EXAMPLE:
"What strategies and functionalities are used to optimize logistics operations during high traffic periods?"

User Query:
"{query}"

Optimized Retrieval Query:
"""

    try:
        expanded_query = mock_llm.generate_content(prompt)

        expanded_query = " ".join(expanded_query.split())

        print(f"\n[Expanded Query]\n{expanded_query}\n")

        return expanded_query

    except Exception as e:
        print(f"[ERROR] Query Expansion Failed: {e}")
        return query

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
