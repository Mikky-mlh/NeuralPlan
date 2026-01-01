"""Helper to load and encode logo for display."""
import base64
from pathlib import Path

def get_logo_base64():
    """Load logo and convert to base64 for embedding in HTML."""
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_logo_html():
    """Return HTML for clickable logo in sidebar."""
    logo_b64 = get_logo_base64()
    return f"""
    <a href="/" target="_self" style="text-decoration: none;">
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_b64}" alt="Neural Plan Logo" 
                 style="width: 120px; border-radius: 12px; box-shadow: 0 4px 15px rgba(46, 49, 146, 0.3); 
                        transition: transform 0.3s ease; cursor: pointer;" 
                 onmouseover="this.style.transform='scale(1.05)'" 
                 onmouseout="this.style.transform='scale(1)'">
        </div>
    </a>
    """
