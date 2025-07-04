import streamlit as st
import json
import asyncio
import aiohttp
import os
import base64
import tempfile
import io
from typing import Dict, List, Optional, Callable
import random
from PIL import Image
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from rembg import remove
from dotenv import load_dotenv
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import functools
import time


load_dotenv()

# Configuration
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID", "production-ai-461211")

# Valid filename characters
valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"

# Music lists
bg_music_list = [
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/music/bgm-1.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/music/bgm-2.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/music/bgm-3.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/music/bgm-4.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/music/bgm-5.mp3",
]

game_over_music_list = [
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/sfx/lose_1.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/sfx/lose_2.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/sfx/lose_3.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/sfx/lose_4.mp3",
    "https://aicade-ui-assets.s3.amazonaws.com/GameAssets/sfx/lose_5.mp3",
]

# Asset links organized by category
ASSET_LINKS = {
    "backgrounds": [
        "https://aicade-ui-assets.s3.amazonaws.com/game_background.webp/games/6994335331/history/iteration/EMTLoVrleTh0YS5m.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/fantasy_forest_background.webp/games/6994335331/history/iteration/EMTLoVrleTh0YS5m.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/background_scene.webp/games/6994335331/history/iteration/EMTLoVrleTh0YS5m.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/cyberpunk_background.webp/games/6994335331/history/iteration/EMTLoVrleTh0YS5m.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/jungle_background.webp/games/6994335331/history/iteration/EMTLoVrleTh0YS5m.webp",
    ],
    "platforms": [
        "https://aicade-user-store.s3.amazonaws.com/6994335331/games/vCIdKnhkwH3vMsdD/assets/images/extra_platform_1.png_id.png?t=1751615638234",
        "https://aicade-user-store.s3.amazonaws.com/6994335331/games/vCIdKnhkwH3vMsdD/assets/images/extra_platform_2.png_id.png?t=1751615632903",
        "https://aicade-user-store.s3.amazonaws.com/6994335331/games/vCIdKnhkwH3vMsdD/assets/images/extra_platform.png_id.png?t=1751615585126",
        "https://aicade-user-store.s3.amazonaws.com/6994335331/games/vCIdKnhkwH3vMsdD/assets/images/extra_platform.png_id.png?t=1751615585126",
        "https://aicade-user-store.s3.amazonaws.com/6994335331/games/vCIdKnhkwH3vMsdD/assets/images/extra_platform.png_id.png?t=1751615585126",
    ],
    "characters": [
        "https://aicade-ui-assets.s3.amazonaws.com/player_character.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/hero_player.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/knight_player.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/wizard_player.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/archer_player.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
    ],
    "enemies": [
        "https://aicade-ui-assets.s3.amazonaws.com/goblin_enemy.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/orc_enemy.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/skeleton_enemy.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/zombie_enemy.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/dragon_enemy.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
    ],
    "avoidables": [
        "https://aicade-ui-assets.s3.amazonaws.com/spike_obstacle.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/spike_trap_obstacle.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/spike_trap_obstacle.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/spike_trap_obstacle.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/spike_trap_obstacle.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
    ],
    "projectiles": [
        "https://aicade-ui-assets.s3.amazonaws.com/arrow_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/fireball_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/bullet_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/fireball_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/fireball_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
    ],
    "collectibles": [
        "https://aicade-ui-assets.s3.amazonaws.com/golden_coin.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/collectible_gem.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/heart_collectible.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/star_collectible.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/health_potion.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
    ],
    "covers": [
        "https://aicade-ui-assets.s3.amazonaws.com/game_cover_image.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/action_game_cover.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/action_game_cover.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/action_game_cover.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/action_game_cover.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
    ]
}

common_instruction = """Instruction: You are a prompt generator for creating a single game image asset based on Input and #Assets, strictly follow the format and Examples below:
Make sure the singular prompt is short and accurate description for around 50 words.Use the same art-style as mentioned. Ensure the ((())) are kept in the prompt as per placement in the example prompt. Keep the prompt exactly like example for platform
"""

Instruction_Cover = """Instruction: You are a prompt generator for creating a single game image asset based on Input and #Assets, strictly follow the format and Examples below:
The asset name should not change at all. Make sure the prompts are short and accurate descriptions around 50 words each.Use the same art-style everywhere
Follow the Example as closely as possible. This is essential in the prompt shaped as letters to make the word "[name of the game]" in the center of the image"""

# Thread pool for CPU-bound operations
thread_pool = ThreadPoolExecutor(max_workers=4)

def get_asset_link(asset_name: str, category: str) -> str:
    """Get a random asset link for the given category"""
    try:
        # Map categories to asset link categories
        category_map = {
            "background": "backgrounds",
            "platform": "platforms",
            "character": "characters", 
            "enemy": "enemies",
            "avoidable": "avoidables",
            "projectile": "projectiles",
            "collectible": "collectibles",
            "cover_image": "covers"
        }
        
        link_category = category_map.get(category, None)
        
        # Handle misc category by randomly selecting from avoidables, projectiles, or collectibles
        if category == "misc" or link_category is None:
            misc_categories = ["avoidables", "projectiles", "collectibles"]
            link_category = random.choice(misc_categories)
        
        available_links = ASSET_LINKS.get(link_category, ASSET_LINKS["characters"])
        
        # Return a random link from the category
        return random.choice(available_links)
        
    except Exception as e:
        print(f"Error getting asset link for {category}: {e}")
        # Fallback to first character asset
        return ASSET_LINKS["characters"][0]

def run_in_thread(func):
    """Decorator to run sync functions in thread pool"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(thread_pool, functools.partial(func, *args, **kwargs))
    return wrapper

async def init_vertex_credentials():
    """Initialize Google Cloud credentials asynchronously"""
    creds_json_str = os.getenv("GOOGLE_APPLICATIONS_CREDENTIALS_JSON")
    if not creds_json_str:
        raise ValueError("GOOGLE_APPLICATIONS_CREDENTIALS_JSON environment variable not set")
    
    # Create temp file asynchronously
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    temp_path = temp_file.name
    temp_file.close()
    
    async with aiofiles.open(temp_path, 'w') as f:
        await f.write(creds_json_str)
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_path
    return temp_path

@run_in_thread
def _get_access_token():
    """Sync function to get access token (runs in thread)"""
    try:
        print("DEBUG: Getting access token...")
        creds_json_str = os.getenv("GOOGLE_APPLICATIONS_CREDENTIALS_JSON")
        if not creds_json_str:
            print("DEBUG: GOOGLE_APPLICATIONS_CREDENTIALS_JSON not found")
            raise ValueError("GOOGLE_APPLICATIONS_CREDENTIALS_JSON environment variable not set")
        
        print("DEBUG: Parsing credentials JSON...")
        creds_info = json.loads(creds_json_str)
        credentials = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        print("DEBUG: Refreshing credentials...")
        request = Request()
        credentials.refresh(request)
        
        print("DEBUG: Access token obtained successfully")
        return credentials.token
    except Exception as e:
        print(f"DEBUG: Error getting access token: {e}")
        import traceback
        traceback.print_exc()
        return None

async def get_access_token():
    """Get Google Cloud access token asynchronously"""
    return await _get_access_token()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe usage"""
    filename = filename.replace(" ", "_")
    filename = "".join(c for c in filename if c in valid_chars)
    return filename[:50]

def extract_category(filename: str) -> str:
    """Extract category from filename"""
    filename_lower = filename.lower()
    if "background" in filename_lower or "bg" in filename_lower:
        return "background"
    elif "platform" in filename_lower:
        return "platform"
    elif "player" in filename_lower or "character" in filename_lower:
        return "character"
    elif "enemy" in filename_lower:
        return "enemy"
    elif "avoidable" in filename_lower:
        return "avoidable"
    elif "projectile" in filename_lower:
        return "projectile"
    elif "collectible" in filename_lower:
        return "collectible"
    elif "cover" in filename_lower:
        return "cover_image"
    else:
        return "misc"


@run_in_thread




async def process_single_asset(
    session: aiohttp.ClientSession,
    asset_key: str,
    asset_descriptor: str,
    game_data: Dict,
    user_id: str,
    game_id: str,
    s3_service: Optional[object],
    upload_to_s3: bool
) -> Optional[str]:
    """Process a single asset using predefined links"""
    try:
        print(f"DEBUG: Getting asset link for {asset_key}")
        
        category = extract_category(asset_key)
        asset_link = get_asset_link(asset_key, category)
        
        print(f"DEBUG: Selected asset link for {asset_key}: {asset_link}")
        return asset_link
        
    except Exception as e:
        print(f"DEBUG: Error processing {asset_key}: {e}")
        return None
    
async def generate_and_process_assets(
    config_data: Dict, 
    game_data: Dict,
    user_id: str,
    game_id: str,
    upload_to_s3: bool = True
) -> Dict:
    """Generate asset links for all assets in config"""
    
    image_loader = config_data.get("imageLoader", {})
    if not image_loader:
        print("DEBUG: No imageLoader found in config")
        return config_data
    
    print(f"DEBUG: Processing {len(image_loader)} assets")
    
    updated_config = config_data.copy()
    
    # Process each asset (no async needed now)
    for asset_key, asset_descriptor in image_loader.items():
        print(f"DEBUG: Processing asset: {asset_key}")
        
        category = extract_category(asset_key)
        asset_link = get_asset_link(asset_key, category)
        
        updated_config["imageLoader"][asset_key] = asset_link
        print(f"DEBUG: Assigned {asset_key} -> {asset_link}")
    
    # Add random background music (keep this)
    if "audioLoader" not in updated_config:
        updated_config["audioLoader"] = {}
    
    updated_config["audioLoader"]["backgroundMusic"] = random.choice(bg_music_list)
    updated_config["audioLoader"]["gameOverMusic"] = random.choice(game_over_music_list)
    
    print(f"DEBUG: Final config has {len(updated_config.get('imageLoader', {}))} assets")
    return updated_config

# Streamlit async wrapper
def run_async(coro):
    """Run coroutine in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

# Progress tracking class that's safe for Streamlit
class ProgressTracker:
    def __init__(self, progress_bar, status_text):
        self.progress_bar = progress_bar
        self.status_text = status_text
        self.current = 0
        self.total = 0
        self.current_message = ""
    
    def update(self, current: int, total: int, message: str):
        """Thread-safe progress update"""
        self.current = current
        self.total = total
        self.current_message = message
        
        # Update UI in main thread
        try:
            progress = current / total if total > 0 else 0
            self.progress_bar.progress(progress)
            self.status_text.text(f"{message} ({current}/{total})")
        except Exception as e:
            # Ignore Streamlit context errors
            print(f"Progress update error (can be ignored): {e}")

def main():
    st.set_page_config(
        page_title="Game Asset Generator", 
        page_icon="🎮", 
        layout="wide"
    )
    
    st.title("🎮 One-Step Game Asset Generator")
    st.write("Upload your config.json → Get it back with generated images!")
    
    # Initialize session state
    if 'generated_config' not in st.session_state:
        st.session_state.generated_config = None
    if 'generation_in_progress' not in st.session_state:
        st.session_state.generation_in_progress = False
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload & Configure")
        
        # File upload
        uploaded_file = st.file_uploader("Choose a config.json file", type=['json'])
        
        if uploaded_file is not None:
            try:
                config_data = json.load(uploaded_file)
                st.success("Config file loaded successfully!")
                
                # Display current assets
                image_loader = config_data.get("imageLoader", {})
                if image_loader:
                    st.write("### 📋 Assets to Generate")
                    st.write(f"**Total Assets:** {len(image_loader)}")
                    
                    for idx, (asset_key, asset_value) in enumerate(image_loader.items(), 1):
                        category = extract_category(asset_key)
                        st.write(f"**{idx}.** `{asset_key}` → *{category}*")
                    
                    # Game configuration
                    st.write("### 🎯 Game Settings")
                    
                    upload_to_s3 = True 
                    
                    if upload_to_s3:
                        user_id = st.text_input("User ID", value="default_user", help="User ID for S3 path organization")
                        game_id = st.text_input("Game ID", value="default_game", help="Game ID for S3 path organization")
                    else:
                        user_id = "default_user"
                        game_id = "default_game"
                    
                    # Store data
                    st.session_state.config_data = config_data
                    st.session_state.user_id = user_id
                    st.session_state.game_id = game_id
                    st.session_state.upload_to_s3 = upload_to_s3
                    
                else:
                    st.warning("No 'imageLoader' section found in config.")
                    
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid config.json.")
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    with col2:
        st.header("🚀 Generate Assets")
        
        # Check if ready to generate
        ready_to_generate = (
            hasattr(st.session_state, 'config_data') and 
            hasattr(st.session_state, 'user_id') and
            hasattr(st.session_state, 'game_id') and
            not st.session_state.generation_in_progress
        )
        
        if st.button("🎨 Assign Asset Links", disabled=not ready_to_generate):
            if not ready_to_generate:
                st.error("Please upload a config file first!")
                return
                
            with st.spinner("Generating all assets..."):
                updated_config = run_async(generate_and_process_assets(
                st.session_state.config_data,
                {},
                st.session_state.user_id,
                st.session_state.game_id,
                False  # No S3 upload needed
                ))
            
                st.session_state.generated_config = updated_config
                st.success("🎉 Asset links assigned successfully!")
    
    # Results section
    if st.session_state.generated_config:
        st.header("✅ Generated Config")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### 📄 Updated Configuration")
            
            # Show config preview
            with st.expander("View Config JSON", expanded=False):
                st.json(st.session_state.generated_config, expanded=False)
            # Download button
            st.download_button(
                label="⬇️ Download Updated Config.json",
                data=json.dumps(st.session_state.generated_config, indent=2),
                file_name="updated_config.json",
                mime="application/json",
                help="Download the configuration file with generated asset URLs or base64 data."
            )

        with col2:
            st.write("### 🖼️ Generated Assets Preview")
            if st.session_state.generated_config and st.session_state.generated_config.get("imageLoader"):
                image_loader = st.session_state.generated_config["imageLoader"]
                
                # Create columns for a grid-like display
                cols = st.columns(2) # Adjust number of columns as needed
                col_idx = 0

                for asset_name, asset_url_or_b64 in image_loader.items():
                    # Display the asset in a column
                    with cols[col_idx]:
                        st.subheader(f"🎨 {asset_name}")
                        if asset_url_or_b64 and (asset_url_or_b64.startswith("http") or asset_url_or_b64.startswith("data:image")):
                            st.image(asset_url_or_b64, caption=asset_name, use_column_width=True)
                        else:
                            st.info("Image not available or failed to load.")
                        
                    col_idx = (col_idx + 1) % len(cols) # Cycle through columns

            else:
                st.info("No generated assets to display yet. Upload a config and click 'Generate All Assets'.")

if __name__ == "__main__":
    main()
