# overwatch-2-stats

Collects stats from Overwatch 2 games. Currently using tesseract to read the stats from screenshots of the scoreboard at the end of the game.

# Getting started

1. python -m venv .env
2. source .env/Scripts/activate # might be in .env/bin instead
3. pip install -r requirements.txt
4. Install tesseract. pytesseract doesn't actually contain the binary, so you have to install it separately.
   Windows: https://github.com/UB-Mannheim/tesseract/wiki
