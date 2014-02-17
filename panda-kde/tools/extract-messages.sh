#!/bin/sh
BASEDIR="po"    # root of translatable sources
PROJECT="panda-kde"        # project name
WDIR=`pwd`              # working dir

intltool-extract --quiet --type=gettext/ini panda.desktop.template
cat panda.desktop.template.h >> rc.cpp
rm panda.desktop.template.h

echo "Extracting messages"
# see above on sorting
find . -name '*.cpp' -o -name '*.h' -o -name '*.c' | sort > ${WDIR}/infiles.list
echo "rc.cpp" >> infiles.list
cd ${WDIR}
xgettext --from-code=UTF-8 -C -kde -ci18n -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 -ktr2i18n:1 \
	-kI18N_NOOP:1 -kI18N_NOOP2:1c,2 -kaliasLocale -kki18n:1 -kki18nc:1c,2 -kki18np:1,2 -kki18ncp:1c,2,3 -kN_:1 \
	--files-from=infiles.list -D ${BASEDIR} -D ${WDIR} -o ${BASEDIR}/${PROJECT}.pot || { echo "error while calling xgettext. aborting."; exit 1; }
echo "Done extracting messages"


echo "Merging translations"
catalogs=`find . -name '*.po'`
for cat in $catalogs; do
  echo $cat
  msgmerge -o $cat.new $cat ${BASEDIR}/${PROJECT}.pot
  mv $cat.new $cat
done
echo "Done merging translations"

cd ${WDIR}
intltool-merge --quiet --desktop-style ${BASEDIR} panda.desktop.template panda.desktop

echo "Cleaning up"
cd ${WDIR}
rm infiles.list
rm rc.cpp
echo "Done"
