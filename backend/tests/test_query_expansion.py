import importlib
import sys
import types


def test_query_expansion_llm_uses_mocked_gcp_sdk(monkeypatch):
    # Create a fake google.generativeai module to avoid real SDK or network calls.
    fake_genai = types.ModuleType("google.generativeai")

    class FakeResponse:
        def __init__(self, text):
            self.text = text

    class FakeGenerativeModel:
        def __init__(self, model_name):
            self.model_name = model_name

        def generate_content(self, prompt):
            return FakeResponse("mock expanded query")

    fake_genai.configure = lambda api_key=None: None
    fake_genai.GenerativeModel = FakeGenerativeModel

    sys.modules["google.generativeai"] = fake_genai

    # Reload the query_expansion module so it binds to the fake SDK module.
    import pkg.services.query_expansion as query_expansion
    importlib.reload(query_expansion)

    expanded_query = query_expansion.query_expansion_llm("How does the system handle peak delivery demand?")

    assert expanded_query == "mock expanded query"
    assert "peak delivery demand" not in expanded_query or isinstance(expanded_query, str)
