"""
Quick check for pyscisci. Run from anywhere after installing the package:

  cd python_packages/pyscisci
  pip install -e .

Use ONE Python environment (conda *or* .venv — not both active). If both
`(pyscisci_env)` and `(.venv)` appear in your prompt, `python` may point at
whichever was activated last; run:  which python
"""
import sys
import traceback


def test_installations():
    print("--- pyscisci Installation Check ---")
    print(f"Python: {sys.executable}\n")

    # 1) Bare package (metadata only)
    try:
        import pyscisci

        print(
            f"✅ import pyscisci: OK (version {getattr(pyscisci, '__version__', 'unknown')})"
        )
    except ImportError as e:
        print("❌ import pyscisci: FAILED — package not installed in this interpreter.")
        print(f"   ({e})")
        print(
            "\n   Fix: cd python_packages/pyscisci && pip install -e .\n"
            "   (Use the same env you use for Jupyter / tenure_net.)"
        )
        return

    # 2) Full API (pulls in numpy, pandas, dask, numba, datasources, …)
    try:
        import pyscisci.all as pss  # noqa: F401

        print("✅ import pyscisci.all: OK (full stack)")
    except ImportError:
        print("❌ import pyscisci.all: FAILED — missing dependency for submodules.")
        print("   Underlying error:")
        traceback.print_exc()
        print(
            "\n   Typical fix: pip install pandas numpy scipy scikit-learn nameparser\n"
            "   lxml requests unidecode tqdm dask numba\n"
            "   (or: pip install -e . from python_packages/pyscisci)"
        )
        return

    # 3) Optional extras (setup.py extras_require)
    try:
        import tables

        print("✅ HDF support (tables): OK")
    except ImportError:
        print("⚠️  HDF support (tables): not installed — optional (pip install tables)")

    try:
        import spacy

        print("✅ NLP (spacy): OK")
    except ImportError:
        print("⚠️  NLP (spacy): not installed — optional for some examples")

    print("\n--- Done ---")


if __name__ == "__main__":
    test_installations()
