from .detector import FileDetector
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ExtensionManager")


class ExtensionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExtensionManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        self.initialized = True
        self.active = False
        logger.info("Universal File Parser Extension Manager Initialized.")

    def activate(self):
        """Called when the extension is activated."""
        if self.active:
            logger.warning("Extension is already active.")
            return
        self.active = True
        logger.info("Extension Activated Successfully.")
        return True

    def deactivate(self):
        """Called when the extension is deactivated."""
        self.active = False
        logger.info("Extension Deactivated.")

    def hello_world(self):
        """Test command handler."""
        message = "Hello from Universal File Parser!"
        logger.info(message)
        return message

    def parse_file(self, file_path=None):
        """Main parsing entry point (Phase 2 Scaffold)."""
        if not file_path:
            logger.error("No file path provided for parsing.")
            return {"status": "error", "message": "No file path provided"}

        logger.info(f"Parsing requested for: {file_path}")
        # Logic for Phase 2 goes here
        return {"status": "success", "file": file_path}
    
    def parse_file(self, file_path=None):
        """Main parsing entry point with Phase 2 Detection."""
        if not file_path:
            logger.error("No file path provided.")
            return {"status": "error", "message": "No file path provided"}
        
        file_type = FileDetector.detect_type(file_path)
        logger.info(f"Detected File Type: {file_type} for {file_path}")

        if file_type == "UNKNOWN":
            return {"status": "unsupported", "message": f"Unsupported format for {file_path}"}

        # Logic for Phase 3 (Actual Parsers) will go here
        return {
            "status": "success", 
            "detected_type": file_type, 
            "path": file_path
        }


def activate():
    return ExtensionManager().activate()


def deactivate():
    return ExtensionManager().deactivate()


if __name__ == "__main__":
    # Local CLI testing
    manager = ExtensionManager()
    manager.activate()
    manager.hello_world()
