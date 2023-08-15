cd ..
echo "Creating virtual python environment"
python -m venv $(pwd)
echo "Upgrading pip"
bin/pip install --upgrade pip
echo "Installing dependencies"
bin/pip install pyinstaller simple-term-menu