import gkeepapi
import os
from dotenv import load_dotenv

_keep_client = None

def get_client():
    """
    Get or initialize the Google Keep client.
    This ensures we only authenticate once and reuse the client.
    
    Returns:
        gkeepapi.Keep: Authenticated Keep client
    """
    global _keep_client
    
    if _keep_client is not None:
        return _keep_client
    
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    email = os.getenv('GOOGLE_EMAIL')
    master_token = os.getenv('GOOGLE_MASTER_TOKEN')
    
    if not email or not master_token:
        raise ValueError("Missing credentials in environment variables")
    
    # Initialize the Keep API
    keep = gkeepapi.Keep()
    
    # Authenticate
    keep.authenticate(email, master_token)
    
    # Store the client for reuse
    _keep_client = keep
    
    return keep 