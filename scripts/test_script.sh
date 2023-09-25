#!/bin/bash

# create directories
mkdir ./Documents
mkdir ./Downloads
mkdir ./Pictures

# create files in Documents directory and write random text to them
echo "Lorem ipsum dolor sit amet" > ./Documents/file1.exe
echo "Sed in mauris quis sem tempor" > ./Documents/file2.docx
echo "Phasellus faucibus luctus nisl, eu" > ./Documents/file3.pdf
echo "Maecenas rhoncus lobortis orci non" > ./Documents/file4.txt
echo "Sed in mauris quis sem tempor" > ./Documents/file5.xlsx

# create files in Downloads directory and write random text to them
echo "Curabitur fermentum, mauris vel dictum" > ./Downloads/file1.exe
echo "Vivamus luctus consectetur quam" > ./Downloads/file2.docx
echo "Nam non sapien ac orci aliquet" >./Downloads/file3.pdf
echo "Fusce vestibulum nisl et odio" > ./Downloads/file4.txt
echo "Vivamus luctus consectetur quam" > ./Downloads/file5.xlsx

# create files in Pictures directory and write random text to them
echo "Pellentesque habitant morbi tristique senectus" > ./Pictures/file1.exe
echo "Cras vel tellus efficitur, euismod" > ./Pictures/file2.docx
echo "In finibus sapien vel purus" > ./Pictures/file3.pdf
echo "Integer nec ex vel augue" > ./Pictures/file4.txt
echo "Cras vel tellus efficitur, euismod" > ./Pictures/file5.xlsx

python service.py