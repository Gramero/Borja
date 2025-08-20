name: Update RSS

on:
  schedule:
    - cron: "0 * * * *"   # cada hora
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: pip install requests feedparser

      - name: Run script
        run: python scripts/update_rss.py

      - name: Commit and push
        run: |
          git config --local user.email "actions@github.com"
          git config --local user.name "GitHub Actions"
          git add docs/feed.xml
          git commit -m "Update RSS feed" || echo "No changes to commit"
          git push
