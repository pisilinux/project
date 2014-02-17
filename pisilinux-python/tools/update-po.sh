
python tools/pygettext.py -o po/pardus-python.pot pardus
for lang in po/*.po
do
    msgmerge -U $lang po/pardus-python.pot
done
