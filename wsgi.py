"""Main Flask application entry point."""

import os
from backend import create_app

# Create Flask application
app = create_app()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("FLASK_PORT", 5000))
    
    # Run development server with debug enabled
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
