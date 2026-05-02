from .detector import FileDetector
from .parsers.factory import ParserFactory
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
        if not file_path:
            return {"status": "error", "message": "No file path provided"}
        
        # Phase 2: Detection
        file_type = FileDetector.detect_type(file_path)
        logger.info(f"Detected: {file_type}")

        # Phase 3: Parsing
        parser = ParserFactory.get_parser(file_type)
        if not parser:
            return {"status": "unsupported", "message": f"No parser for {file_type}"}

        try:
            df = parser.parse(file_path)
            # Return metadata and a preview of the data
            return {
                "status": "success",
                "detected_type": file_type,
                "rows": len(df),
                "columns": list(df.columns),
                "preview": df.head(5).to_dict(orient='records')
            }
        except Exception as e:
            logger.error(f"Parsing failed: {str(e)}")
            return {"status": "error", "message": str(e)}


def activate():
    return ExtensionManager().activate()


def deactivate():
    return ExtensionManager().deactivate()


if __name__ == "__main__":
    # Local CLI testing
    manager = ExtensionManager()
    manager.activate()
    manager.hello_world()
