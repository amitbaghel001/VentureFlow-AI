"""
EXIMIUS AI — Smoke Test
Run with: python test_imports.py
Verifies all core imports work before launching the Streamlit app.
"""

import sys

def test(name: str, fn):
    try:
        fn()
        print(f"  ✓  {name}")
        return True
    except Exception as e:
        print(f"  ✗  {name}: {e}")
        return False

print("\nEXIMIUS AI - Import Validation\n" + "-" * 40)

results = [
    test("streamlit",      lambda: __import__("streamlit")),
    test("openai",         lambda: __import__("openai")),
    test("sqlalchemy",     lambda: __import__("sqlalchemy")),
    test("faiss",          lambda: __import__("faiss")),
    test("pyvis",          lambda: __import__("pyvis")),
    test("networkx",       lambda: __import__("networkx")),
    test("reportlab",      lambda: __import__("reportlab")),
    test("trafilatura",    lambda: __import__("trafilatura")),
    test("dotenv",         lambda: __import__("dotenv")),
    test("core.styles",    lambda: __import__("core.styles")),
    test("core.database",  lambda: __import__("core.database")),
    test("core.ai_engine", lambda: __import__("core.ai_engine")),
    test("core.pdf_export",lambda: __import__("core.pdf_export")),
]

passed = sum(results)
total  = len(results)
print(f"\n{'─'*40}")
print(f"  {passed}/{total} imports successful")

if passed == total:
    print("  ✓  All systems ready. Run: streamlit run app.py\n")
else:
    print("  ✗  Fix the above errors, then run: streamlit run app.py\n")
    sys.exit(1)
