import httpx


def fetch_url(url: str, timeout: float = 20.0) -> str:
    headers = {
        "User-Agent": "FDE-CLI/0.1 research ingestion tool"
    }

    response = httpx.get(
        url,
        headers=headers,
        timeout=timeout,
        follow_redirects=True,
    )

    response.raise_for_status()
    return response.text