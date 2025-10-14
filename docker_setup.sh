#!/bin/bash
# Docker environment setup script for gLayout testing

echo "=== Docker Environment Setup for gLayout ==="

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $python_version"

# Check gdsfactory version
gdsfactory_version=$(python3 -c "import gdsfactory; print(gdsfactory.__version__)" 2>/dev/null || echo "Not installed")
echo "gdsfactory version: $gdsfactory_version"

# Check Pydantic version
pydantic_version=$(python3 -c "import pydantic; print(pydantic.__version__)" 2>/dev/null || echo "Not installed")
echo "Pydantic version: $pydantic_version"

echo ""
echo "=== Fixing compatibility issues ==="

# Fix gdsfactory version if needed
if [[ "$python_version" == "3.9" ]] || [[ "$python_version" == "3.8" ]]; then
    echo "Installing compatible gdsfactory version for Python $python_version..."
    pip install "gdsfactory==6.116.0"
else
    echo "Python version $python_version should work with latest gdsfactory"
fi

# Fix Pydantic version if needed
if python3 -c "import pydantic; from pydantic import validate_call" 2>/dev/null; then
    echo "✓ Pydantic V2 detected - validate_call available"
else
    echo "Pydantic V1 detected - using validate_arguments compatibility"
fi

echo ""
echo "=== Testing imports ==="

# Test basic imports
python3 -c "
try:
    from gdsfactory.grid import grid
    print('✓ gdsfactory import successful')
except Exception as e:
    print(f'✗ gdsfactory import failed: {e}')

try:
    from pydantic import validate_call
    print('✓ Pydantic V2 validate_call available')
except ImportError:
    try:
        from pydantic import validate_arguments
        print('✓ Pydantic V1 validate_arguments available')
    except ImportError as e:
        print(f'✗ Pydantic import failed: {e}')
"

echo ""
echo "=== Setup complete ==="
echo "You can now run:"
echo "  python src/glayout/primitives/fet.py"
echo "  python src/glayout/primitives/polyres.py"
echo "  python3 test_primitive_netlisting.py"
