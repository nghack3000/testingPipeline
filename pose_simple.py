import streamlit as st
import json
import random
from typing import Dict

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
    ],
    "projectiles": [
        "https://aicade-ui-assets.s3.amazonaws.com/arrow_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/fireball_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
        "https://aicade-ui-assets.s3.amazonaws.com/bullet_projectile.webp/games/6994335331/history/iteration/vCIdKnhkwH3vMsdD.webp",
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
    ]
}

def extract_category(filename: str) -> str:
    """Extract category from filename"""
    filename_lower = filename.lower()
    if "background" in filename_lower or "bg" in filename_lower:
        return "background"
    elif "platform" in filename_lower:
        return "platform"
    elif "player" in filename_lower or "character" in filename_lower or "hero" in filename_lower:
        return "character"
    elif "enemy" in filename_lower or "monster" in filename_lower or "boss" in filename_lower:
        return "enemy"
    elif "avoidable" in filename_lower or "obstacle" in filename_lower or "trap" in filename_lower:
        return "avoidable"
    elif "projectile" in filename_lower or "bullet" in filename_lower or "arrow" in filename_lower:
        return "projectile"
    elif "collectible" in filename_lower or "coin" in filename_lower or "gem" in filename_lower or "power" in filename_lower:
        return "collectible"
    elif "cover" in filename_lower:
        return "cover_image"
    else:
        return "misc"

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

def process_assets(config_data: Dict) -> Dict:
    """Process all assets and assign links"""
    image_loader = config_data.get("imageLoader", {})
    if not image_loader:
        return config_data
    
    updated_config = config_data.copy()
    
    # Process each asset
    for asset_key, asset_descriptor in image_loader.items():
        category = extract_category(asset_key)
        asset_link = get_asset_link(asset_key, category)
        updated_config["imageLoader"][asset_key] = asset_link
    
    # Add random background music
    if "audioLoader" not in updated_config:
        updated_config["audioLoader"] = {}
    
    updated_config["audioLoader"]["backgroundMusic"] = random.choice(bg_music_list)
    updated_config["audioLoader"]["gameOverMusic"] = random.choice(game_over_music_list)
    
    return updated_config

def main():
    st.set_page_config(
        page_title="Game Asset Generator", 
        page_icon="🎮", 
        layout="wide"
    )
    
    st.title("🎮 Game Asset Generator")
    st.markdown("**Upload your config.json → Get it back with curated game assets!**")
    
    # Add sample config download
    st.markdown("### 📥 Don't have a config file? Download a sample:")
    sample_config = {
        "imageLoader": {
            "player_character": "",
            "background_forest": "",
            "platform_stone": "",
            "enemy_goblin": "",
            "collectible_coin": "",
            "projectile_arrow": "",
            "obstacle_spike": ""
        }
    }
    
    st.download_button(
        "📥 Download Sample Config",
        data=json.dumps(sample_config, indent=2),
        file_name="sample_config.json",
        mime="application/json"
    )
    
    st.markdown("---")
    
    # Initialize session state
    if 'generated_config' not in st.session_state:
        st.session_state.generated_config = None
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload Configuration")
        
        # File upload
        uploaded_file = st.file_uploader("Choose a config.json file", type=['json'])
        
        if uploaded_file is not None:
            try:
                config_data = json.load(uploaded_file)
                st.success("✅ Config file loaded successfully!")
                
                # Display current assets
                image_loader = config_data.get("imageLoader", {})
                if image_loader:
                    st.write("### 📋 Assets Found")
                    st.write(f"**Total Assets:** {len(image_loader)}")
                    
                    # Show asset preview
                    for idx, (asset_key, asset_value) in enumerate(image_loader.items(), 1):
                        category = extract_category(asset_key)
                        st.write(f"**{idx}.** `{asset_key}` → *{category}*")
                    
                    # Store data in session state
                    st.session_state.config_data = config_data
                    
                else:
                    st.warning("⚠️ No 'imageLoader' section found in config.")
                    
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON file. Please upload a valid config.json.")
            except Exception as e:
                st.error(f"❌ Error loading file: {e}")
    
    with col2:
        st.header("🚀 Generate Assets")
        
        # Check if ready to generate
        ready_to_generate = hasattr(st.session_state, 'config_data')
        
        if st.button("🎨 Assign Asset Links", disabled=not ready_to_generate):
            if not ready_to_generate:
                st.error("Please upload a config file first!")
                return
            
            with st.spinner("🔄 Assigning asset links..."):
                updated_config = process_assets(st.session_state.config_data)
                st.session_state.generated_config = updated_config
                st.success("🎉 Asset links assigned successfully!")
    
    # Results section
    if st.session_state.generated_config:
        st.markdown("---")
        st.header("✅ Results")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("### 📄 Updated Configuration")
            
            # Show summary
            image_loader = st.session_state.generated_config.get("imageLoader", {})
            audio_loader = st.session_state.generated_config.get("audioLoader", {})
            
            st.info(f"✅ {len(image_loader)} assets assigned\n✅ {len(audio_loader)} audio files added")
            
            # Show config preview
            with st.expander("🔍 View Full Config JSON", expanded=False):
                st.json(st.session_state.generated_config)
            
            # Download button
            st.download_button(
                label="⬇️ Download Updated Config.json",
                data=json.dumps(st.session_state.generated_config, indent=2),
                file_name="updated_config.json",
                mime="application/json",
                help="Download the configuration file with assigned asset URLs"
            )

        with col2:
            st.write("### 🖼️ Asset Preview")
            
            if image_loader:
                # Show first few assets as preview
                preview_count = min(3, len(image_loader))
                for i, (asset_name, asset_url) in enumerate(list(image_loader.items())[:preview_count]):
                    st.write(f"**{asset_name}**")
                    try:
                        st.image(asset_url, width=150)
                    except:
                        st.write("Preview unavailable")
                
                if len(image_loader) > preview_count:
                    st.write(f"... and {len(image_loader) - preview_count} more assets")
            else:
                st.info("No assets to preview yet.")
    
    # Usage instructions
    st.markdown("---")
    st.markdown("### 📚 How to Use")
    st.markdown("""
    1. **Upload** your `config.json` file with an `imageLoader` section
    2. **Click** "Assign Asset Links" to populate with curated assets
    3. **Download** the updated config file
    4. **Use** the updated config in your game!
    
    **Asset Categories:** backgrounds, platforms, characters, enemies, obstacles, projectiles, collectibles, covers
    """)

if __name__ == "__main__":
    main()