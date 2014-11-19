#-- start of make_header -----------------

#====================================
#  Document TrackMonitorsMergeMap
#
#   Generated Wed Nov 12 13:48:59 2014  by ikomarov
#
#====================================

include ${CMTROOT}/src/Makefile.core

ifdef tag
CMTEXTRATAGS = $(tag)
else
tag       = $(CMTCONFIG)
endif

cmt_TrackMonitorsMergeMap_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_TrackMonitorsMergeMap_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_TrackMonitorsMergeMap

TrackMonitors_tag = $(tag)

#cmt_local_tagfile_TrackMonitorsMergeMap = $(TrackMonitors_tag)_TrackMonitorsMergeMap.make
cmt_local_tagfile_TrackMonitorsMergeMap = $(bin)$(TrackMonitors_tag)_TrackMonitorsMergeMap.make

else

tags      = $(tag),$(CMTEXTRATAGS)

TrackMonitors_tag = $(tag)

#cmt_local_tagfile_TrackMonitorsMergeMap = $(TrackMonitors_tag).make
cmt_local_tagfile_TrackMonitorsMergeMap = $(bin)$(TrackMonitors_tag).make

endif

include $(cmt_local_tagfile_TrackMonitorsMergeMap)
#-include $(cmt_local_tagfile_TrackMonitorsMergeMap)

ifdef cmt_TrackMonitorsMergeMap_has_target_tag

cmt_final_setup_TrackMonitorsMergeMap = $(bin)setup_TrackMonitorsMergeMap.make
#cmt_final_setup_TrackMonitorsMergeMap = $(bin)TrackMonitors_TrackMonitorsMergeMapsetup.make
cmt_local_TrackMonitorsMergeMap_makefile = $(bin)TrackMonitorsMergeMap.make

else

cmt_final_setup_TrackMonitorsMergeMap = $(bin)setup.make
#cmt_final_setup_TrackMonitorsMergeMap = $(bin)TrackMonitorssetup.make
cmt_local_TrackMonitorsMergeMap_makefile = $(bin)TrackMonitorsMergeMap.make

endif

cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)TrackMonitorssetup.make

#TrackMonitorsMergeMap :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'TrackMonitorsMergeMap'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = TrackMonitorsMergeMap/
#TrackMonitorsMergeMap::
#	@if test ! -d $(bin)$(binobj) ; then $(mkdir) -p $(bin)$(binobj) ; fi
#	$(echo) "STRUCTURED_OUTPUT="$(bin)$(binobj)
endif

ifdef use_requirements
$(use_requirements) : ;
endif

#-- end of make_header ------------------
# File: cmt/fragments/merge_rootmap_header
# Author: Sebastien Binet (binet@cern.ch)

# Makefile fragment to merge a <library>.rootmap file into a single
# <project>.rootmap file in the (lib) install area
# If no InstallArea is present the fragment is dummy


.PHONY: TrackMonitorsMergeMap TrackMonitorsMergeMapclean

# default is already '#'
#genmap_comment_char := "'#'"

rootMapRef    := ../$(tag)/TrackMonitors.rootmap

ifdef CMTINSTALLAREA
rootMapDir    := ${CMTINSTALLAREA}/$(tag)/lib
mergedRootMap := $(rootMapDir)/$(project).rootmap
stampRootMap  := $(rootMapRef).stamp
else
rootMapDir    := ../$(tag)
mergedRootMap := 
stampRootMap  :=
endif

TrackMonitorsMergeMap :: $(stampRootMap) $(mergedRootMap)
	@:

.NOTPARALLEL : $(stampRootMap) $(mergedRootMap)

$(stampRootMap) $(mergedRootMap) :: $(rootMapRef)
	@echo "Running merge_rootmap  TrackMonitorsMergeMap" 
	$(merge_rootmap_cmd) --do-merge \
         --input-file $(rootMapRef) --merged-file $(mergedRootMap)

TrackMonitorsMergeMapclean ::
	$(cleanup_silent) $(merge_rootmap_cmd) --un-merge \
         --input-file $(rootMapRef) --merged-file $(mergedRootMap) ;
	$(cleanup_silent) $(remove_command) $(stampRootMap)
libTrackMonitors_so_dependencies = ../x86_64-slc6-gcc48-opt/libTrackMonitors.so
#-- start of cleanup_header --------------

clean :: TrackMonitorsMergeMapclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(TrackMonitorsMergeMap.make) $@: No rule for such target" >&2
#	@echo "#CMT> Warning: $@: No rule for such target" >&2; exit
	if echo $@ | grep '$(package)setup\.make$$' >/dev/null; then\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsMergeMap.make): $@: File no longer generated" >&2; exit 0; fi
else
.DEFAULT::
	$(echo) "(TrackMonitorsMergeMap.make) PEDANTIC: $@: No rule for such target" >&2
	if echo $@ | grep '$(package)setup\.make$$' >/dev/null; then\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsMergeMap.make): $@: File no longer generated" >&2; exit 0;\
	 elif test $@ = "$(cmt_final_setup)" -o\
	 $@ = "$(cmt_final_setup_TrackMonitorsMergeMap)" ; then\
	 found=n; for s in 1 2 3 4 5; do\
	 sleep $$s; test ! -f $@ || { found=y; break; }\
	 done; if test $$found = n; then\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsMergeMap.make) PEDANTIC: $@: Seems to be missing. Ignore it for now" >&2; exit 0 ; fi;\
	 elif test `expr $@ : '.*/'` -ne 0 ; then\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsMergeMap.make) PEDANTIC: $@: Seems to be a missing file. Please check" >&2; exit 2 ; \
	 else\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(TrackMonitorsMergeMap.make) PEDANTIC: $@: Seems to be a fake target due to some pattern. Just ignore it" >&2 ; exit 0; fi
endif

TrackMonitorsMergeMapclean ::
#-- end of cleanup_header ---------------
