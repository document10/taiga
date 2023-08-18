cd ..
echo "Creating virtual python environment"
python3 -m venv $(pwd)
echo "Upgrading pip"
bin/pip install --upgrade pip
echo "Installing dependencies"
bin/pip install pyinstaller simple-term-menu
echo "Environment created.To compile the binary using the local environment use the build_from_env.sh script."