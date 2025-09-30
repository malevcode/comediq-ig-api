import argparse
import os
from pathlib import Path
from typing import Tuple, Optional

from dotenv import load_dotenv
import instaloader


def ensure_outdir(path: str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def initialize_loader(args: argparse.Namespace) -> Tuple[
  Optional[instaloader.Instaloader], 
  Optional[instaloader.Profile]
]: 
    session_id = os.getenv("IG_SESSIONID")

    if not session_id:
        print("[!] IG_SESSIONID not set in environment/.env. Stories require authentication.")
        return None, None

    L = instaloader.Instaloader(
        download_video_thumbnails=False,
        save_metadata=True,
        download_geotags=False,
        compress_json=False,
        post_metadata_txt_pattern="",
        quiet=False,  
    )

    USER = os.getenv("IG_USER")
    PASSWORD = os.getenv("IG_PASSWORD")

    L.login(USER, PASSWORD)

    # Inject session cookie from browser
    L.context._session.cookies.set("sessionid", session_id, domain=".instagram.com")

    logged_in_as = L.test_login()
    if not logged_in_as:
        print("[!] Session invalid. Provide a valid IG_SESSIONID from your logged-in browser.")
        return None, None

    print(f"Authenticated as: {logged_in_as}")

    try:
        profile = instaloader.Profile.from_username(L.context, args.username)
        return L, profile
    except Exception as e:  # noqa: BLE001
        print(f"[!] Failed to resolve username: {e}")
        return None, None


def download_posts( profile: instaloader.Profile, 
                    loader : instaloader.Instaloader, 
                    args: argparse.Namespace
                  ) -> None:
    posts_target_dir = ensure_outdir(str(Path(args.out) / args.username / "posts"))

    posts_downloaded = 0
    max = args.max
    
    for post in profile.get_posts() :
        loader.download_post(post, target = posts_target_dir)
        posts_downloaded += 1
        max -= 1
        if max == 0: 
            break

    print(f"Posts downloaded: {posts_downloaded}")



def download_stories( profile: instaloader.Profile, 
                      loader : instaloader.Instaloader, 
                      args: argparse.Namespace
                    ) -> None:
    stories_downloaded = 0
    stories_target_dir = ensure_outdir(str(Path(args.out) / args.username / "stories"))
    metadata_target = ensure_outdir(str(Path(args.out) / args.username / "metadata"))
    # Download stories
    for story in loader.get_stories(userids=[profile.userid]):
        for item in story.get_items():
            print(item.caption_mentions)
            loader.save_metadata_json(filename=str(metadata_target), structure=item)
            loader.download_storyitem(item, target=stories_target_dir)
            stories_downloaded += 1
      
    print(f"Stories downloaded: {stories_downloaded}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download active Instagram stories for a user using Instaloader")
    parser.add_argument("--username", required=True, help="Target Instagram username to fetch stories for")
    parser.add_argument("--out", default="downloads", help="Output directory")
    parser.add_argument("--max", default=5, help="Maximum number of latest posts")
    args = parser.parse_args()

    load_dotenv()
    L, profile = initialize_loader(args)
    
    if L is None or profile is None:
        print("[!] Failed to initialize loader or profile. Exiting.")
        return

    # download_posts(profile, L, args)
    download_stories(profile, L, args)
    L.close()


if __name__ == "__main__":
    main()
