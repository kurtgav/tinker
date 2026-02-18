from src.tools.memory_tools import remember, recall, set_current_user
from src.memory.storage import MemoryManager
import os

def test_memory():
    print("Testing M4 Memory Tools...")

    # Mock User
    user_id = "test_user_123"
    set_current_user(user_id)
    
    # Clean previous state if any
    # (Optional, but good for repeatable tests)
    
    # Test 1: Remember
    print("\n[1] Testing Remember...")
    key = "favorite_color"
    value = "blue"
    result = remember(key, value)
    print(f"Result: {result}")
    assert "remembered" in result

    # Test 2: Recall
    print("\n[2] Testing Recall...")
    recall_result = recall(key)
    print(f"Result: {recall_result}")
    assert "blue" in recall_result

    # Test 3: Recall unknown
    print("\n[3] Testing Recall Unknown...")
    unknown = recall("non_existent_key")
    print(f"Result: {unknown}")
    assert "don't have any memory" in unknown

    # Test 4: Persistence (New instance)
    print("\n[4] Testing Persistence...")
    # Since sqlite is persistent on disk, this naturally tests persistence across function calls
    # but let's ensure we are using the singleton correctly or if we re-instantiate
    
    val = MemoryManager.get_instance().get_pref(user_id, key)
    assert val == "blue"

    print("\n✅ M4 Verification Passed!")

if __name__ == "__main__":
    test_memory()
