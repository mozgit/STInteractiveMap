#-- start of make_header -----------------

#====================================
#  Document TrackMonitorsRootMap
#
#   Generated Wed Nov 12 13:48:57 2014  by ikomarov
#
#====================================

include ${CMTROOT}/src/Makefile.core

ifdef tag
CMTEXTRATAGS = $(tag)
else
tag       = $(CMTCONFIG)
endif

cmt_TrackMonitorsRootMap_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_TrackMonitorsRootMap_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_TrackMonitorsRootMap

TrackMonitors_tag = $(tag)

#cmt_local_tagfile_TrackMonitorsRootMap = $(TrackMonitors_tag)_TrackMonitorsRootMap.make
cmt_local_tagfile_TrackMonitorsRootMap = $(bin)$(TrackMonitors_tag)_TrackMonitorsRootMap.make

else

tags      = $(tag),$(CMTEXTRATAGS)

TrackMonitors_tag = $(tag)

#cmt_local_tagfile_TrackMonitorsRootMap = $(TrackMonitors_tag).make
cmt_local_tagfile_TrackMonitorsRootMap = $(bin)$(TrackMonitors_tag).make

endif

include $(cmt_local_tagfile_TrackMonitorsRootMap)
#-include $(cmt_local_tagfile_TrackMonitorsRootMap)

ifdef cmt_TrackMonitorsRootMap_has_target_tag

cmt_final_setup_TrackMonitorsRootMap = $(bin)setup_TrackMonitorsRootMap.make
#cmt_final_setup_TrackMonitorsRootMap = $(bin)TrackMonitors_TrackMonitorsRootMapsetup.make
cmt_local_TrackMonitorsRootMap_makefile = $(bin)TrackMonitorsRootMap.make

else

cmt_final_setup_TrackMonitorsRootMap = $(bin)setup.make
#cmt_final_setup_TrackMonitorsRootMap = $(bin)TrackMonitorssetup.make
cmt_local_TrackMonitorsRootMap_makefile = $(bin)TrackMonitorsRootMap.make

endif

cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)TrackMonitorssetup.make

#TrackMonitorsRootMap :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'TrackMonitorsRootMap'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = TrackMonitorsRootMap/
#TrackMonitorsRootMap::
#	@if test ! -d $(bin)$(binobj) ; then $(mkdir) -p $(bin)$(binobj) ; fi
#	$(echo) "STRUCTURED_OUTPUT="$(bin)$(binobj)
endif

ifdef use_requirements
$(use_requirements) : ;
endif

#-- end of make_header ------------------
##
rootmapfile = TrackMonitors.rootmap
ROOTMAP_DIR = ../$(tag)
fulllibname = libTrackMonitors.$(shlibsuffix)

TrackMonitorsRootMap :: ${ROOTMAP_DIR}/$(rootmapfile)
	@:

${ROOTMAP_DIR}/$(rootmapfile) :: $(bin)$(fulllibname)
	@echo 'Generating rootmap file for $(fulllibname)'
	cd ../$(tag);$(genmap_cmd) -i $(fulllibname) -o ${ROOTMAP_DIR}/$(rootmapfile) $(TrackMonitorsRootMap_genmapflags)

install :: TrackMonitorsRootMapinstall
TrackMonitorsRootMapinstall :: TrackMonitorsRootMap

uninstall :: TrackMonitorsRootMapuninstall
TrackMonitorsRootMapuninstall :: TrackMonitorsRootMapclean

TrackMonitorsRootMapclean ::
	@echo 'Deleting $(rootmapfile)'
	@rm -f ${ROOTMAP_DIR}/$(rootmapfile)

#-- start of cleanup_header --------------

clean :: TrackMonitorsRootMapclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(TrackMonitorsRootMap.make) $@: No rule for such target" >&2
#	@echo "#CMT> Warning: $@: No rule for such target" >&2; exit
	if echo $@ | grep '$(package)setup\.make$$' >/dev/null; then\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsRootMap.make): $@: File no longer generated" >&2; exit 0; fi
else
.DEFAULT::
	$(echo) "(TrackMonitorsRootMap.make) PEDANTIC: $@: No rule for such target" >&2
	if echo $@ | grep '$(package)setup\.make$$' >/dev/null; then\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsRootMap.make): $@: File no longer generated" >&2; exit 0;\
	 elif test $@ = "$(cmt_final_setup)" -o\
	 $@ = "$(cmt_final_setup_TrackMonitorsRootMap)" ; then\
	 found=n; for s in 1 2 3 4 5; do\
	 sleep $$s; test ! -f $@ || { found=y; break; }\
	 done; if test $$found = n; then\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsRootMap.make) PEDANTIC: $@: Seems to be missing. Ignore it for now" >&2; exit 0 ; fi;\
	 elif test `expr $@ : '.*/'` -ne 0 ; then\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsRootMap.make) PEDANTIC: $@: Seems to be a missing file. Please check" >&2; exit 2 ; \
	 else\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsRootMap.make) PEDANTIC: $@: Seems to be a fake target due to some pattern. Just ignore it" >&2 ; exit 0; fi
endif

TrackMonitorsRootMapclean ::
#-- end of cleanup_header ---------------
