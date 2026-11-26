"""Regression: non-ASCII attribution headers broke live OpenRouter calls."""
import httpx
import app_core


def test_openrouter_attribution_is_serializable_as_http_headers():
    # httpx performs the same header encoding used by the OpenAI transport.
    headers = httpx.Headers(app_core.API_PROVIDERS['openrouter']['headers'])
    assert headers['X-Title'] == 'Ofensiva Trafego IA'
