# main.py
import argparse, time, getpass
from datetime import timezone
import instaloader, pandas as pd
from instaloader.exceptions import ConnectionException

def collect(handle: str, out: str, delay: float, limit: int, login_user: str | None):
    L = instaloader.Instaloader(download_pictures=False, download_videos=False)

    # Login (recommended to avoid rate limits)
    if login_user:
        try:
            # use saved session if available
            L.load_session_from_file(login_user)
        except Exception:
            # first time: interactive login then save session
            pwd = getpass.getpass(f"Password for {login_user}: ")
            L.login(login_user, pwd)
            L.save_session_to_file()

    profile = instaloader.Profile.from_username(L.context, handle)

    rows, count = [], 0
    for post in profile.get_posts():
        rows.append({
            "shortcode": post.shortcode,
            "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
            "date_utc": post.date_utc.replace(tzinfo=timezone.utc).isoformat(),
            "likes": post.likes, "comments": post.comments,
            "is_video": post.is_video,
            "caption": (post.caption or "").replace("\n", " ").strip(),
            "hashtags": ",".join(post.caption_hashtags or []),
        })
        count += 1
        if limit and count >= limit:
            break
        time.sleep(delay)  # be polite (e.g., 2.5s)

    df = pd.DataFrame(rows).sort_values("date_utc")
    # handy features
    df["date_utc"] = pd.to_datetime(df["date_utc"], utc=True)
    df["hour"] = df["date_utc"].dt.tz_convert("US/Pacific").dt.hour
    df["day"] = df["date_utc"].dt.day_name()
    df["n_hashtags"] = df["hashtags"].str.count(",").fillna(0).astype(int) + (df["hashtags"]!="").astype(int)
    df["caption_len"] = df["caption"].str.len().fillna(0).astype(int)
    df["engagement"] = df["likes"] + df["comments"]
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows → {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", required=True)
    ap.add_argument("--out", default="club_dataset_public.csv")
    ap.add_argument("--delay", type=float, default=2.5)   # slower by default
    ap.add_argument("--limit", type=int, default=100)     # cap requests
    ap.add_argument("--login", dest="login_user", default=None, help="your IG username (not password)")
    args = ap.parse_args()
    collect(args.handle, args.out, args.delay, args.limit, args.login_user)
