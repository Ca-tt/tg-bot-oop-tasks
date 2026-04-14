#
#! TODO: improve to use dataclasses
    
class MongoDB:
    def __init__(self, uri):
        self.uri = uri
        self.client = None

    def connect(self):
        # Simulate connecting to MongoDB
        print(f"Connecting to MongoDB at {self.uri}...")
        self.client = "MongoDB Client Connected"
        print("Connected to MongoDB.")

    def disconnect(self):
        # Simulate disconnecting from MongoDB
        if self.client:
            print("Disconnecting from MongoDB...")
            self.client = None
            print("Disconnected from MongoDB.")
        else:
            print("No active MongoDB connection to disconnect.")