#!/usr/bin/env bash
# scripts/search_arxiv.sh
QUERY=$1
COUNT=${2:-5}
ENCODED_QUERY=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))' "$QUERY")
# Use curl to query ArXiv API
curl -sL "https://export.arxiv.org/api/query?search_query=all:$ENCODED_QUERY&start=0&max_results=$COUNT&sortBy=submittedDate&sortOrder=descending"
