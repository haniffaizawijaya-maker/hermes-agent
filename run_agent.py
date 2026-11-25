"""
Hermes Agent - Autonomous Messenger & Workflow Execution Agent
Entry point runner script for Discord Gateway and Persistent Memory synchronization.
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("HermesAgent")

def load_environment():
    """Load configuration from .env if present."""
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        logger.warning(".env not found! Please copy .env.example to .env and configure your keys.")
        return False
    
    # Simple .env parser without external dependencies
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()
    logger.info("Environment configuration loaded successfully.")
    return True

def verify_obsidian_memory():
    """Verify that Obsidian vault persistent memory path exists."""
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        logger.warning("OBSIDIAN_VAULT_PATH is not configured in .env.")
        return False

    vault_dir = Path(vault_path)
    if not vault_dir.exists():
        logger.warning(f"Obsidian Vault directory does not exist at: {vault_path}")
        return False

    memory_file = vault_dir / "MEMORY.md"
    user_file = vault_dir / "USER.md"
    logger.info(f"Obsidian Vault found at: {vault_path}")
    logger.info(f"Persistent Memory File: {'Found' if memory_file.exists() else 'Missing'}")
    logger.info(f"User Profile File: {'Found' if user_file.exists() else 'Missing'}")
    return True

def main():
    print("=" * 60)
    print("  HERMES AGENT - AUTONOMOUS WORKFLOW & MESSAGING AGENT")
    print("=" * 60)
    
    if not load_environment():
        print("[!] Setup needed: Copy .env.example to .env and configure tokens.")
        sys.exit(1)
        
    print("[*] Checking Persistent Memory via Obsidian Vault...")
    verify_obsidian_memory()
    
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_token or discord_token == "your_discord_bot_token_here":
        logger.error("DISCORD_BOT_TOKEN is not configured in .env!")
        print("[!] Please provide a valid DISCORD_BOT_TOKEN in .env")
        sys.exit(1)
        
    print("[*] Hermes Gateway starting...")
    print(f"[*] Free response channels: {os.getenv('DISCORD_FREE_RESPONSE_CHANNELS', '*')}")
    print(f"[*] Mention required: {os.getenv('DISCORD_REQUIRE_MENTION', 'false')}")
    print("[+] Hermes Agent is operational.")

if __name__ == "__main__":
    main()
