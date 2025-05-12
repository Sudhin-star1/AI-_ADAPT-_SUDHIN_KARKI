from app import create_app

# Create an instance of the Flask application
app = create_app()

# Entry point at which the app is run
if __name__ == "__main__":
    # Runs the app on all available network interfaces at port 5055
    app.run(host="0.0.0.0", port=5055, debug=True)