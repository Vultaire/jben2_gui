######################################################################
# For Python, we rely on setup.py for doing the right thing.  The    #
# targets here correspond to "make" and "make install" respectively, #
# and basically just function as passthroughs.                       #
######################################################################

# "build" seems unnecessary since "install" calls build again
# anyway...  So I'm commenting this out to save a little bit of build
# time.

#all-local:
#	python setup.py build

install-exec-local:
	python setup.py install

# We also need to tell Automake to include all the Python sources in
# the dist tarball.  Here's where we do that.
EXTRA_DIST = \
	setup.py \
	jben/__init__.py jben/alphanum.py jben/app.py jben/console.py \
	jben/dict.py jben/dict_downloader.py jben/download_thread.py \
	jben/global_refs.py jben/jben_globals.py jben/main.py \
	jben/preferences.py \
	jben/interface/__init__.py \
	jben/interface/console/__init__.py \
	jben/interface/gtk/__init__.py \
	jben/interface/gtk/dict_manager.py \
	jben/interface/gtk/dialog/__init__.py \
	jben/interface/gtk/dialog/dict_mirror_select.py \
	jben/interface/gtk/dialog/vocablisteditor.py \
	jben/interface/gtk/dialog/dict_download.py \
	jben/interface/gtk/dialog/kanjilisteditor.py \
	jben/interface/gtk/dialog/preferences/__init__.py \
	jben/interface/gtk/dialog/preferences/tab_prefsfonts.py \
	jben/interface/gtk/dialog/preferences/tab_prefskanjidict.py \
	jben/interface/gtk/dialog/preferences/tab_prefskanjitest.py \
	jben/interface/gtk/dialog/preferences/tab_prefsother.py \
	jben/interface/gtk/widget/__init__.py \
	jben/interface/gtk/widget/infomessage.py \
	jben/interface/gtk/widget/search_frame.py \
	jben/interface/gtk/widget/worddict.py \
	jben/interface/gtk/widget/hwpad.py \
	jben/interface/gtk/widget/kanjidict.py \
	jben/interface/gtk/widget/storedsize.py \
	jben/interface/gtk/widget/yesnodialog.py \
	jben/interface/gtk/window/__init__.py \
	jben/interface/gtk/window/kanjihwsearch.py \
	jben/interface/gtk/window/main.py \
	jben/test/__init__.py jben/test/test_dict_downloader.py \
	jben/test/test_dict.py \
	py2exe/jben.py \
	scripts/jben_launcher.py
