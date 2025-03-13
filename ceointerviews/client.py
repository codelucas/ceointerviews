import requests
import json
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode


DEFAULT_PAGE_SIZE = 10


class APIResults:
    def __init__(
        self,
        results: List[Dict],
        page_has_previous: bool,
        page_has_next: bool,
        page_num: int,
        http_status: int,
    ):
        self.results = results
        self.page_has_previous = page_has_previous
        self.page_has_next = page_has_next
        self.page_num = page_num

        self.num_results = len(results)
        self.http_status = http_status

    def __str__(self):
        return json.dumps(
            {
                "results": self.results,
                "page_has_previous": self.page_has_previous,
                "page_has_next": self.page_has_next,
                "page_num": self.page_num,
                "num_results": self.num_results,
                "http_status": self.http_status,
            },
            indent=4,
        )


class CEOInterviews:
    def __init__(self, api_key: str, base_url: str = "https://ceointerviews.ai"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-Key": api_key}

    def get_entities(
        self,
        keyword: Optional[str] = None,
        page_num: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> APIResults:
        params = {"keyword": keyword, "page_num": page_num, "page_size": page_size}
        url = f"{self.base_url}/api/get_entities/?{urlencode(params)}"
        response = requests.get(url, headers=self.headers)

        response.raise_for_status()
        jsondict = response.json()
        return APIResults(
            results=jsondict["results"],
            page_has_previous=jsondict["page_has_previous"],
            page_has_next=jsondict["page_has_next"],
            page_num=jsondict["page_num"],
            http_status=response.status_code,
        )

    def get_feed(
        self,
        entity_id: Optional[int] = None,
        keyword: Optional[str] = None,
        company_id: Optional[int] = None,
        page_num: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> APIResults:
        params = {
            "entity_id": entity_id,
            "keyword": keyword,
            "company_id": company_id,
            "page_num": page_num,
            "page_size": page_size,
        }
        url = f"{self.base_url}/api/get_feed/?{urlencode(params)}"
        response = requests.get(url, headers=self.headers)

        response.raise_for_status()
        jsondict = response.json()
        return APIResults(
            results=jsondict["results"],
            page_has_previous=jsondict["page_has_previous"],
            page_has_next=jsondict["page_has_next"],
            page_num=jsondict["page_num"],
            http_status=response.status_code,
        )

    def get_companies(
        self,
        keyword: Optional[str] = None,
        page_num: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> APIResults:
        """
        Args:
            keyword: Search by company name or ticker
            page_num: Page number for pagination (default: 1)
            page_size: Number of results per page (default: 10)

        Returns:
            APIResults object containing the results and pagination info
        """
        params = {
            "page_num": page_num,
            "page_size": page_size,
        }
        if keyword:
            params["keyword"] = keyword

        url = f"{self.base_url}/api/get_companies/"
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        jsondict = response.json()
        return APIResults(
            results=jsondict["results"],
            page_has_previous=jsondict["page_has_previous"],
            page_has_next=jsondict["page_has_next"],
            page_num=jsondict["page_num"],
            http_status=response.status_code,
        )

    def get_quotes(
        self,
        entity_id: Optional[int] = None,
        post_id: Optional[int] = None,
        keyword: Optional[str] = None,
        is_notable: Optional[bool] = None,
        is_controversial: Optional[bool] = None,
        is_financial_policy: Optional[bool] = None,
        page_num: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> APIResults:
        """
        Args:
            entity_id: Filter quotes by entity ID
            post_id: Filter quotes by post ID
            keyword: Search quotes by keyword
            is_notable: Filter by notable quotes
            is_controversial: Filter by controversial quotes
            is_financial_policy: Filter by financial policy quotes
            page_num: Page number for pagination (default: 1)
            page_size: Number of results per page (default: 10)

        Returns:
            APIResults object containing the results and pagination info
        """
        params = {
            "page_num": page_num,
            "page_size": page_size,
        }

        if entity_id is not None:
            params["entity_id"] = entity_id

        if post_id is not None:
            params["post_id"] = post_id

        if keyword:
            params["keyword"] = keyword

        if is_notable is not None:
            params["is_notable"] = str(is_notable).lower()

        if is_controversial is not None:
            params["is_controversial"] = str(is_controversial).lower()

        if is_financial_policy is not None:
            params["is_financial_policy"] = str(is_financial_policy).lower()

        url = f"{self.base_url}/api/get_quotes/"
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        jsondict = response.json()
        return APIResults(
            results=jsondict["results"],
            page_has_previous=jsondict["page_has_previous"],
            page_has_next=jsondict["page_has_next"],
            page_num=jsondict["page_num"],
            http_status=response.status_code,
        )


def pretty_print(response: Dict[str, Any]) -> None:
    print(json.dumps(response, indent=4))


def test_get_entities(client: CEOInterviews):
    david_sacks = client.get_entities(keyword="david sa")
    print(david_sacks)

    malaysia = client.get_entities(keyword="malaysia", page_num=1, page_size=5)
    print(malaysia)

    null_state = client.get_entities()
    print("############### NULL STATE ENTITIES LIST ############")
    print(null_state)

    # Test two pages
    page_1 = client.get_entities(page_num=1, page_size=3)
    page_2 = client.get_entities(page_num=2, page_size=3)
    print("############### PAGE 1 ############")
    print(page_1)
    print("############### PAGE 2 ############")
    print(page_2)


def test_get_feed(client: CEOInterviews):
    resp = client.get_entities(keyword="donald trump")
    trump = resp.results[0]
    trump_feed = client.get_feed(entity_id=trump["id"])
    print(trump_feed.results)

    trump_softbank_feed = client.get_feed(
        entity_id=trump["id"],
        keyword="softbank ceo",
    )
    print(f"Num results: {len(trump_softbank_feed.results)}")

    elon_musk = client.get_entities(keyword="elon musk").results[0]
    musk_page_3 = client.get_feed(entity_id=elon_musk["id"], page_num=3)
    print(f"Number of results: {len(musk_page_3.results)}")


def test_get_companies(client: CEOInterviews):
    # Test getting companies
    companies = client.get_companies(keyword="tesla")
    pretty_print(companies)

    # Test pagination
    companies_page_2 = client.get_companies(keyword="tesla", page_num=2)
    pretty_print(companies_page_2)


def test_get_quotes(client: CEOInterviews):
    # Test basic quotes retrieval
    quotes = client.get_quotes()
    print(f"Total quotes found: {len(quotes.results)}")
    if len(quotes.results) >= 2:
        print("Example quotes:")
        pretty_print(quotes.results[:2])
    print("-" * 50)

    # Test getting quotes for a specific entity (Elon Musk)
    entities = client.get_entities(keyword="elon musk")
    if entities.results:
        entity_id = entities.results[0]["id"]
        entity_quotes = client.get_quotes(entity_id=entity_id)
        print(f"Elon Musk quotes found: {len(entity_quotes.results)}")
        if len(entity_quotes.results) >= 2:
            print("Example Elon Musk quotes:")
            pretty_print(entity_quotes.results[:2])
        print("-" * 50)

        # Test AND query: Elon Musk AND is_notable
        notable_elon_quotes = client.get_quotes(entity_id=entity_id, is_notable=True)
        print(f"Notable Elon Musk quotes found: {len(notable_elon_quotes.results)}")
        if len(notable_elon_quotes.results) >= 2:
            print("Example notable Elon Musk quotes:")
            pretty_print(notable_elon_quotes.results[:2])
        print("-" * 50)

        # Test AND query: Elon Musk AND is_controversial
        controversial_elon_quotes = client.get_quotes(
            entity_id=entity_id, is_controversial=True
        )
        print(
            f"Controversial Elon Musk quotes found: {len(controversial_elon_quotes.results)}"
        )
        if len(controversial_elon_quotes.results) >= 2:
            print("Example controversial Elon Musk quotes:")
            pretty_print(controversial_elon_quotes.results[:2])
        print("-" * 50)

    # Test getting notable quotes
    notable_quotes = client.get_quotes(is_notable=True)
    print(f"Notable quotes found: {len(notable_quotes.results)}")
    if len(notable_quotes.results) >= 2:
        print("Example notable quotes:")
        pretty_print(notable_quotes.results[:2])
    print("-" * 50)

    # Test getting financial policy quotes
    financial_quotes = client.get_quotes(is_financial_policy=True)
    print(f"Financial policy quotes found: {len(financial_quotes.results)}")
    if len(financial_quotes.results) >= 2:
        print("Example financial policy quotes:")
        pretty_print(financial_quotes.results[:2])
    print("-" * 50)

    # Test keyword search
    keyword_quotes = client.get_quotes(keyword="innovation")
    print(f"Innovation quotes found: {len(keyword_quotes.results)}")
    if len(keyword_quotes.results) >= 2:
        print("Example innovation quotes:")
        pretty_print(keyword_quotes.results[:2])
    print("-" * 50)

    # Test pagination
    page_1 = client.get_quotes(page_num=1, page_size=5)
    page_2 = client.get_quotes(page_num=2, page_size=5)
    print("============ QUOTES PAGE 1 ============")
    print(f"Page 1 quotes count: {len(page_1.results)}")
    if len(page_1.results) >= 2:
        print("Example page 1 quotes:")
        pretty_print(page_1.results[:2])

    print("============ QUOTES PAGE 2 ============")
    print(f"Page 2 quotes count: {len(page_2.results)}")
    if len(page_2.results) >= 2:
        print("Example page 2 quotes:")
        pretty_print(page_2.results[:2])

    # Verify different results between pages
    page_1_ids = [quote["id"] for quote in page_1.results]
    page_2_ids = [quote["id"] for quote in page_2.results]
    unique_ids = set(page_1_ids + page_2_ids)
    print(f"Total unique quotes across pages: {len(unique_ids)}")
    print(
        f"Are pages different? {len(unique_ids) == len(page_1_ids) + len(page_2_ids)}"
    )


if __name__ == "__main__":
    api_key = "YOUR_API_KEY_HERE"
    client = CEOInterviews(api_key)
    test_get_entities(client)
    test_get_feed(client)
    test_get_companies(client)
    test_get_quotes(client)
