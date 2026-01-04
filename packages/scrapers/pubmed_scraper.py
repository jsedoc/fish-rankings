"""
PubMed Research Paper Scraper
Collects academic papers related to food safety, contaminants, and nutrition
Uses the free NCBI E-utilities API
"""
import httpx
from typing import List, Dict
import asyncio
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

PUBMED_SEARCH_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

async def search_pubmed(query: str, max_results: int = 100, days_back: int = 365) -> List[str]:
    """
    Search PubMed for papers matching query
    Returns list of PMIDs (PubMed IDs)
    """
    print(f"🔬 Searching PubMed for: {query}")

    # Calculate date range (last N days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
        "mindate": start_date.strftime("%Y/%m/%d"),
        "maxdate": end_date.strftime("%Y/%m/%d")
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(PUBMED_SEARCH_BASE, params=params)
        response.raise_for_status()
        data = response.json()

    pmids = data.get("esearchresult", {}).get("idlist", [])
    print(f"  Found {len(pmids)} papers")

    return pmids


async def fetch_pubmed_details(pmids: List[str]) -> List[Dict]:
    """
    Fetch detailed information for a list of PMIDs
    """
    if not pmids:
        return []

    print(f"📄 Fetching details for {len(pmids)} papers...")

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(PUBMED_FETCH_BASE, params=params)
        response.raise_for_status()

    # Parse XML response
    root = ET.fromstring(response.content)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        try:
            # Extract article data
            medline = article.find(".//MedlineCitation")
            pmid = medline.find(".//PMID").text

            article_node = medline.find(".//Article")
            title = article_node.find(".//ArticleTitle").text or ""

            # Authors
            authors = []
            author_list = article_node.find(".//AuthorList")
            if author_list is not None:
                for author in author_list.findall(".//Author"):
                    last_name = author.find(".//LastName")
                    fore_name = author.find(".//ForeName")
                    if last_name is not None and fore_name is not None:
                        authors.append(f"{fore_name.text} {last_name.text}")

            # Abstract
            abstract_node = article_node.find(".//Abstract/AbstractText")
            abstract = abstract_node.text if abstract_node is not None else ""

            # Journal
            journal_node = article_node.find(".//Journal/Title")
            journal = journal_node.text if journal_node is not None else ""

            # Publication date
            pub_date = article_node.find(".//Journal/JournalIssue/PubDate")
            year = pub_date.find(".//Year")
            month = pub_date.find(".//Month")
            pub_date_str = None
            if year is not None:
                year_str = year.text
                month_str = month.text if month is not None else "01"
                try:
                    pub_date_str = f"{year_str}-{month_str}-01"
                except:
                    pub_date_str = f"{year_str}-01-01"

            # DOI
            doi = None
            article_ids = article.find(".//ArticleIdList")
            if article_ids is not None:
                for aid in article_ids.findall(".//ArticleId"):
                    if aid.get("IdType") == "doi":
                        doi = aid.text

            papers.append({
                "pmid": pmid,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "journal": journal,
                "publication_date": pub_date_str,
                "doi": doi,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })

        except Exception as e:
            print(f"  Error parsing article: {e}")
            continue

    print(f"✅ Parsed {len(papers)} papers successfully")
    return papers


async def collect_food_safety_papers(max_per_topic: int = 50) -> List[Dict]:
    """
    Collect papers on various food safety topics
    """
    print("📚 Collecting food safety research papers...")

    topics = [
        "mercury contamination fish",
        "microplastics food",
        "pesticide residues produce",
        "food safety contaminants",
        "heavy metals seafood",
        "foodborne pathogens",
        "nutrition food safety",
        "PCBs fish consumption"
    ]

    all_papers = []
    pmid_set = set()  # Avoid duplicates

    for topic in topics:
        pmids = await search_pubmed(topic, max_results=max_per_topic, days_back=730)  # 2 years
        new_pmids = [pmid for pmid in pmids if pmid not in pmid_set]
        pmid_set.update(new_pmids)

        if new_pmids:
            papers = await fetch_pubmed_details(new_pmids[:20])  # Limit API calls
            all_papers.extend(papers)

        # Be polite to NCBI servers
        await asyncio.sleep(0.5)

    print(f"✅ Total unique papers collected: {len(all_papers)}")
    return all_papers


if __name__ == "__main__":
    # Test the scraper
    papers = asyncio.run(collect_food_safety_papers(max_per_topic=10))
    print(f"\nCollected {len(papers)} papers")
    if papers:
        print("\nSample paper:")
        print(f"Title: {papers[0]['title']}")
        print(f"Authors: {', '.join(papers[0]['authors'][:3])}")
        print(f"PMID: {papers[0]['pmid']}")
