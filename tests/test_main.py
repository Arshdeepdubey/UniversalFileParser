import pytest
from extension.main import ExtensionManager

@pytest.fixture
def manager():
    # Reset singleton state for testing if necessary, 
    # though usually handled by the pattern
    return ExtensionManager()

def test_singleton_pattern():
    m1 = ExtensionManager()
    m2 = ExtensionManager()
    assert m1 is m2

def test_activation_flow(manager):
    assert manager.activate() is True
    assert manager.active is True

def test_double_activation(manager, caplog):
    manager.active = True
    manager.activate()
    assert "Extension is already active" in caplog.text

def test_deactivation(manager):
    manager.activate()
    manager.deactivate()
    assert manager.active is False

def test_hello_world(manager):
    response = manager.hello_world()
    assert response == "Hello from Universal File Parser!"

def test_parse_file_no_path(manager):
    result = manager.parse_file(None)
    assert result["status"] == "error"

def test_parse_file_with_path(manager):
    result = manager.parse_file("test.csv")
    assert result["status"] == "success"
    assert result["file"] == "test.csv"