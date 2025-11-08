@echo off
chcp 65001 >nul
echo ======================================================================
echo 🌿 SmartLeaf - Complete Fix Installation
echo ======================================================================
echo.

echo [Step 1/5] Uninstalling ALL TensorFlow packages...
echo ⏳ This may take 1-2 minutes...
pip uninstall tensorflow tensorflow-cpu tensorflow-intel tensorflowjs keras tf-keras tensorflow-estimator -y

echo.
echo [Step 2/5] Clearing pip cache...
pip cache purge

echo.
echo [Step 3/5] Installing TensorFlow 2.15.0...
echo ⏳ This may take 2-3 minutes...
pip install --no-cache-dir tensorflow==2.15.0

echo.
echo [Step 4/5] Installing TensorFlowJS 4.11.0...
echo ⏳ This may take 1-2 minutes...
pip install --no-cache-dir tensorflowjs==4.11.0

echo.
echo [Step 5/5] Verifying installation...
python -c "import tensorflow as tf; import tensorflowjs as tfjs; print('✅ SUCCESS!'); print('TensorFlow:', tf.__version__); print('TensorFlowJS:', tfjs.__version__)"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Installation failed!
    echo 💡 Try:
    echo    1. Close VS Code completely
    echo    2. Run this script again as Administrator
    echo    3. Or try: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo ✅ Installation Complete!
echo ======================================================================
echo.
echo Next steps:
echo 1. Run: python convert.py
echo 2. Open index.html with Live Server
echo.
pause