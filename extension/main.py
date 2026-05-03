from .detector import FileDetector
from .parsers.factory import ParserFactory
from .cleaner import DataCleaner  # NEW
from .html_generator import HTMLGenerator  # NEW
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
        
        file_type = FileDetector.detect_type(file_path)
        parser = ParserFactory.get_parser(file_type)
        
        if not parser:
            return {"status": "unsupported", "message": f"No parser for {file_type}"}

        try:
            raw_df = parser.parse(file_path)
            clean_df = DataCleaner.clean(raw_df)
            
            stats = {
                "type": file_type,
                "rows": len(clean_df),
                "size": f"{len(clean_df) * len(clean_df.columns)} cells"
            }
            
            html_content = HTMLGenerator.generate_view(
                clean_df.head(10).to_dict(orient='records'), 
                list(clean_df.columns),
                stats
            )
            
            # Restore the keys expected by the older tests
            return {
                "status": "success",
                "detected_type": file_type,         # Backwards compatibility
                "rows": len(clean_df),               # Backwards compatibility
                "columns": list(clean_df.columns),   # Backwards compatibility
                "preview": clean_df.head(10).to_dict(orient='records'), # Backwards compatibility
                "html": html_content,                # Phase 5 Feature
                "metadata": stats                    # Phase 5 Feature
            }
        except Exception as e:
            logger.error(f"UI Generation failed: {str(e)}")
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
