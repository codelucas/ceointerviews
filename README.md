# CEOInterviews Python Client

A Python client library for the [CEOInterviews.AI](https://ceointerviews.ai) API. We are the largest database of insights from global leaders.

Access millions of verified quotes and precise transcripts from CEOs, Executives, Presidents, and Public Officials across more than 100,000 carefully vetted interviews, podcasts, and public appearances.

[![PyPI version](https://badge.fury.io/py/ceointerviews.svg)](https://badge.fury.io/py/ceointerviews)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### Why trust CEOInterviews?

- Our rigorous AI verification process ensures you receive only authentic statements from influential figures—CEOs, Presidents, and Public Officials.
- When you search for Elon Musk, **you get his exact words**—not someone else's interpretation.
- Accuracy matters. Get direct insights from verified sources.

<table>
  <tr>
    <td width="50%"><img src="https://ceointerviews.ai/static/images/examples/example_failed_3.png" alt="Low quality sources with red X"></td>
    <td width="50%"><img src="https://ceointerviews.ai/static/images/examples/example_elon_verified.png" alt="CEOInterviews AI Verified with green checkmark"></td>
  </tr>
  <tr>
    <td><em>Other sources: Low quality with inaccuracies</em></td>
    <td><em>CEOInterviews: AI-verified authentic quotes</em></td>
  </tr>
</table>

## Installation

```bash
pip install ceointerviews
```

## Authentication

To use this library, you need an API key from CEOInterviews.AI

View our: [API Docs](https://ceointerviews.ai/api_docs/) and [API Purchase link](https://ceointerviews.ai/api_settings/)


```python
from ceointerviews import CEOInterviews
client = CEOInterviews(api_key="your_api_key_here")
```

## Quick Start Examples

### Get controversial quotes from Elon Musk on AI

```python
from ceointerviews import CEOInterviews
api_key = "your_api_key_here"
client = CEOInterviews(api_key)

# Get controversial quotes from Elon Musk on AI
elon_resp = client.get_entities(keyword="elon musk")
elon_id = elon_resp.results[0]["id"]
elon_ai_quotes = client.get_quotes(
    entity_id=elon_id, is_controversial=True, keyword="artificial intelligence"
)

# Print the first quote
if elon_ai_quotes.results:
    quote = elon_ai_quotes.results[0]
    print(f"Quote: \"{quote['text']}\"")

# Get financial policy quotes across all entities and topics
financial_policy_quotes = client.get_quotes(is_financial_policy=True)
```

### Fetch entity data and conversations

```python
# Get Elon Musk's entity data
elon_resp = client.get_entities(keyword="elon musk")
elon_obj = elon_resp.results[0]

# Fetch Elon Musk's conversations
elon_feed = client.get_feed(entity_id=elon_obj["id"]).results

# Inspect results
first_item = elon_feed[0]
print(first_item["title"])
# Example: "LA wildfire: Tesla CEO Elon Musk speaks to fire command team in Los Angeles"

print(first_item["ai_summary"])
# Example: "Elon Musk: discusses the ongoing investigation into the cause of the Palisades fire..."
```

## Core Concepts

The CEOInterviews API is built around several key resources:

### Entities

An `Entity` represents an influential individual such as a CEO, politician, or executive. Each entity has an ID, name, title, and associated organization information.

### Feed Items (Conversations)

Transcribed interviews, podcasts, and appearances where entities have spoken. Each feed item includes an AI-generated summary, title, full transcript, attached Quote objects from the transcript, and metadata.

### Quotes

Notable statements extracted from feed items. These can be filtered by attributes like "controversial" or "financial policy." Each Quote is attached to both an Entity and a Feed Item.

### Companies

Organizations associated with entities, including both public companies (with tickers) and private institutions. Each Company has a list of Entities linked to it, usually the C-suite.

## API Reference

[Click to see the full CEOInterviews API Docs](https://ceointerviews.ai/api_docs)

### Get Entities

```python
# Search for entities by keyword
entities = client.get_entities(keyword="elon musk")
print(entities.results)

# Pagination
page_2 = client.get_entities(keyword="david", page_num=2, page_size=10)

# Get all entities in the database
all_entities = []
for page_num in range(1, 500):
    resp = client.get_entities(page_num=page_num, page_size=100)
    all_entities.extend(resp.results)
    if not resp.page_has_next:
        break
```

### Get Feed (Conversations)

```python
# Get feed posts for a specific entity
entities = client.get_entities(keyword="elon musk")
entity_id = entities.results[0]["id"]
feed = client.get_feed(entity_id=entity_id)

# Search within an entity's feed
keyword_feed = client.get_feed(entity_id=entity_id, keyword="tesla")

# Get all conversations from the database
all_convos = []
for page_num in range(1, 100):
    resp = client.get_feed(page_num=page_num, page_size=50)
    all_convos.extend(resp.results)
    if not resp.page_has_next:
        break
```

### Get Companies

```python
# Search for companies
companies = client.get_companies(keyword="tesla")

# Pagination for companies
companies_page_2 = client.get_companies(page_num=2, page_size=20)
```

### Get Quotes

```python
# Get all quotes
quotes = client.get_quotes()

# Get quotes for a specific entity
entity_quotes = client.get_quotes(entity_id=123)

# Get notable quotes
notable_quotes = client.get_quotes(is_notable=True)

# Get controversial quotes
controversial_quotes = client.get_quotes(is_controversial=True)

# Get financial policy quotes
financial_quotes = client.get_quotes(is_financial_policy=True)

# Search quotes by keyword
keyword_quotes = client.get_quotes(keyword="innovation")

# Get all quotes from the database
all_quotes = []
for page_num in range(1, 500):
    resp = client.get_quotes(page_num=page_num, page_size=100)
    all_quotes.extend(resp.results)
    if not resp.page_has_next:
        break
```

## Use Case Examples

### Investment Research Platform

Build a dashboard that monitors financial policy statements from Federal Reserve officials and track sentiment changes over time:

```python
# Get all Federal Reserve officials
fed_officials = client.get_entities(keyword="federal reserve")
fed_ids = [official["id"] for official in fed_officials.results]

# For each official, get their financial policy statements
all_statements = []
for official_id in fed_ids:
    statements = client.get_quotes(
        entity_id=official_id,
        is_financial_policy=True
    )
    all_statements.extend(statements.results)

# Sort statements by date for timeline analysis
sorted_statements = sorted(all_statements, key=lambda x: x["created_at"])
```

### Competitive Intelligence Tool

Monitor what competitors are saying about your product category or industry trends:

```python
competitor_names = ["Competitor A", "Competitor B", "Competitor C"]
product_keywords = ["product category", "industry trend", "technology"]
insights = {}

for competitor in competitor_names:
    # Get entity IDs for company executives
    execs = client.get_entities(keyword=competitor)
    exec_ids = [exec["id"] for exec in execs.results]

    competitor_insights = []
    for exec_id in exec_ids:
        for keyword in product_keywords:
            # Get relevant statements
            statements = client.get_feed(
                entity_id=exec_id,
                keyword=keyword
            )
            competitor_insights.extend(statements.results)

    insights[competitor] = competitor_insights
```

### AI-Powered Financial Newsletter

Automatically generate a weekly newsletter summarizing what key financial leaders said about important topics.

```python
# Get quotes from the past week
from datetime import datetime, timedelta

one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()

# Get notable financial quotes from the past week
financial_quotes = client.get_quotes(
    is_financial_policy=True,
    is_notable=True
    # Filter by date in your processing logic
)

# Organize by topic for your newsletter
topics = {}
for quote in financial_quotes.results:
    for topic in quote.get("topics", []):
        if topic not in topics:
            topics[topic] = []
        topics[topic].append(quote)

# Generate newsletter content
newsletter_content = "# This Week in Finance\n\n"
for topic, quotes in topics.items():
    newsletter_content += f"## {topic.title()}\n\n"
    # Top 3 quotes per topic
    for quote in quotes[:3]:
        newsletter_content += f"**{quote['entity']['name']}** ({quote['entity']['title']}): \"{quote['text']}\"\n\n"

# Send your generated newsletter to subscribers
```

### Political Stance Analyzer

Track how politicians' stated positions on key issues evolve over time.

```python
# Define politicians and issues to track
politicians = ["Politician A", "Politician B"]
issues = ["healthcare", "taxes", "immigration", "climate change"]

stance_data = {}
for politician in politicians:
    # Get politician entity
    pol_resp = client.get_entities(keyword=politician)
    pol_id = pol_resp.results[0]["id"]

    stance_data[politician] = {}
    for issue in issues:
        # Get all statements on this issue
        statements = client.get_feed(
            entity_id=pol_id,
            keyword=issue
        )

        # Store chronologically for timeline analysis
        stance_data[politician][issue] = sorted(
            statements.results,
            key=lambda x: x["publish_date"]
        )

# Analyze how positions evolved over time for each politician and issue
```

### Market Sentiment Analysis

Track CEO sentiment about economic conditions across different sectors.

```python
# Define sectors to analyze
sectors = {
    "Technology": ["Apple", "Microsoft", "Google", "Meta"],
    "Banking": ["JP Morgan", "Bank of America", "Goldman Sachs"],
    "Energy": ["Exxon", "Chevron", "Shell"]
}

economic_keywords = ["recession", "inflation", "growth", "outlook"]
sentiment_by_sector = {}

for sector, companies in sectors.items():
    sector_sentiment = []

    for company in companies:
        # Get the CEO entity
        company_execs = client.get_entities(keyword=company)
        ceo = [e for e in company_execs.results if "CEO" in e["title"]][0]

        # Get statements about economic conditions
        for keyword in economic_keywords:
            statements = client.get_quotes(
                entity_id=ceo["id"],
                keyword=keyword
            )
            for statement in statements.results:
                sector_sentiment.append({
                    "company": company,
                    "statement": statement["text"],
                    "date": statement["created_at"],
                    "keyword": keyword
                })

    sentiment_by_sector[sector] = sector_sentiment

# Compare sentiment across sectors to identify economic trend signals
```

## Response Format

All API methods return an `APIResults` object with the following properties:

- `results`: List of results
- `page_has_previous`: Boolean indicating if there are previous pages
- `page_has_next`: Boolean indicating if there are more pages
- `page_num`: Current page number
- `num_results`: Number of results in the current page
- `http_status`: HTTP status code of the response

Example:

```python
response = client.get_entities(keyword="elon")
print(f"Found {response.num_results} results")
print(f"Current page: {response.page_num}")
print(f"Has next page: {response.page_has_next}")
```

## Error Handling

The library uses the `requests` module's exception handling. If an API request fails, a `requests.exceptions.HTTPError` will be raised.

```python
import requests

try:
    response = client.get_entities(keyword="elon")
except requests.exceptions.HTTPError as e:
    print(f"API request failed: {e}")
```

## Rate Limits

- **API Tier**: 100 requests per minute, 100,000 requests per month
- **Custom Tier**: Unlimited requests, custom rate limits based on needs

## License

MIT License