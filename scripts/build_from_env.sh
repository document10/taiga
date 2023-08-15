cd ..
echo "Removing previous binary"
rm -rf taiga
echo "Compiling executable"
bin/pyinstaller taiga.py -F
echo "Cleaning up"
mv dist/taiga taiga
rm -rf build
rm -rf dist
rm -rf taiga.spec