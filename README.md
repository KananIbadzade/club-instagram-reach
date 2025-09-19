# Club Instagram Reach

Small project to analyze a public Instagram account’s posts and learn what works
(best days/hours, caption length, hashtags, engagement).  
We only use **public metadata** (likes, comments, caption, timestamp).

## What’s inside
- `main.py` – collects public post data with Instaloader → `club_dataset_public.csv` (git-ignored)
- `club-instagram-eda.ipynb` – notebook for cleaning + quick EDA
- `requirements.txt` – Python deps
- `.gitignore` – keeps data and `.venv/` out of the repo

## Quickstart
```bash
# 1) Setup
python -m venv .venv
source .venv/bin/activate           # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# 2) Login to Instagram once (creates a local session file)
instaloader -l <YOUR_IG_USERNAME>   # enter password + 2FA

# 3) Collect public posts from the club account
python main.py --handle ai.ml.club.sjsu --login <YOUR_IG_USERNAME> --limit 40 --delay 4.0

# 4) Open the notebook and explore
#   -> club-instagram-eda.ipynb
