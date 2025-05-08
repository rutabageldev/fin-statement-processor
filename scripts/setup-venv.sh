#!/bin/bash

set -e

echo "🐍 Setting up Python virtual environment..."

python3 -m venv .venv
source .venv/bin/activate

# === 1. Install dependencies ===
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# === 2. Run smoke test ===
echo "🧪 Running smoke test..."
if python3 -m src.main; then
    echo "✅ Smoke test passed"
else
    echo "❌ Smoke test failed"
    exit 1
fi

# === 3. Run tests ===
echo "🧪 Running unit tests..."
if pytest; then
    echo "✅ All tests passed"
else
    echo "❌ Some tests failed"
    exit 1
fi

# === 4. Run Coverage report ===
echo "📊 Running coverage report..."
pytest --cov=src --cov-report=term

# === 5. Install pre-commit hooks ===
echo "🔧 Installing pre-commit hooks..."
pre-commit install

echo "🎉 Environment ready. Activate with: source .venv/bin/activate"
