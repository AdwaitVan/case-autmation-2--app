import asyncio
from ecourts.core import ECourt

async def test_library():
    print("⏳ Testing openjustice-in library...")
    
    # 1. Initialize the Bombay High Court object
    # '1' is usually the code for Bombay High Court
    court = ECourt(code="1", state_code="1") 
    
    try:
        # 2. Try to search for a case (Writ Petition 1234/2025)
        # Note: The library methods for 'search_case' are currently experimental
        results = await court.search_case(
            case_type="WP", 
            case_number="1234", 
            year="2025"
        )
        
        print(f"✅ Result: {results}")
        
    except AttributeError:
        print("❌ TEST FAILED: The method 'search_case' does not exist yet.")
    except Exception as e:
        print(f"❌ TEST FAILED with error: {e}")
        print("💡 This confirms the feature is 'Work In Progress' and not ready.")

# Run the async test
if __name__ == "__main__":
    asyncio.run(test_library())