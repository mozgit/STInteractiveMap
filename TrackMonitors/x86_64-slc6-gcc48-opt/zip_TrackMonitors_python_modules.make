#-- start of make_header -----------------

#====================================
#  Document zip_TrackMonitors_python_modules
#
#   Generated Wed Nov 12 13:49:13 2014  by ikomarov
#
#====================================

include ${CMTROOT}/src/Makefile.core

ifdef tag
CMTEXTRATAGS = $(tag)
else
tag       = $(CMTCONFIG)
endif

cmt_zip_TrackMonitors_python_modules_has_no_target_tag = 1

#--------------------------------------------------------

ifdef cmt_zip_TrackMonitors_python_modules_has_target_tag

tags      = $(tag),$(CMTEXTRATAGS),target_zip_TrackMonitors_python_modules

TrackMonitors_tag = $(tag)

#cmt_local_tagfile_zip_TrackMonitors_python_modules = $(TrackMonitors_tag)_zip_TrackMonitors_python_modules.make
cmt_local_tagfile_zip_TrackMonitors_python_modules = $(bin)$(TrackMonitors_tag)_zip_TrackMonitors_python_modules.make

else

tags      = $(tag),$(CMTEXTRATAGS)

TrackMonitors_tag = $(tag)

#cmt_local_tagfile_zip_TrackMonitors_python_modules = $(TrackMonitors_tag).make
cmt_local_tagfile_zip_TrackMonitors_python_modules = $(bin)$(TrackMonitors_tag).make

endif

include $(cmt_local_tagfile_zip_TrackMonitors_python_modules)
#-include $(cmt_local_tagfile_zip_TrackMonitors_python_modules)

ifdef cmt_zip_TrackMonitors_python_modules_has_target_tag

cmt_final_setup_zip_TrackMonitors_python_modules = $(bin)setup_zip_TrackMonitors_python_modules.make
#cmt_final_setup_zip_TrackMonitors_python_modules = $(bin)TrackMonitors_zip_TrackMonitors_python_modulessetup.make
cmt_local_zip_TrackMonitors_python_modules_makefile = $(bin)zip_TrackMonitors_python_modules.make

else

cmt_final_setup_zip_TrackMonitors_python_modules = $(bin)setup.make
#cmt_final_setup_zip_TrackMonitors_python_modules = $(bin)TrackMonitorssetup.make
cmt_local_zip_TrackMonitors_python_modules_makefile = $(bin)zip_TrackMonitors_python_modules.make

endif

cmt_final_setup = $(bin)setup.make
#cmt_final_setup = $(bin)TrackMonitorssetup.make

#zip_TrackMonitors_python_modules :: ;

dirs ::
	@if test ! -r requirements ; then echo "No requirements file" ; fi; \
	  if test ! -d $(bin) ; then $(mkdir) -p $(bin) ; fi

javadirs ::
	@if test ! -d $(javabin) ; then $(mkdir) -p $(javabin) ; fi

srcdirs ::
	@if test ! -d $(src) ; then $(mkdir) -p $(src) ; fi

help ::
	$(echo) 'zip_TrackMonitors_python_modules'

binobj = 
ifdef STRUCTURED_OUTPUT
binobj = zip_TrackMonitors_python_modules/
#zip_TrackMonitors_python_modules::
#	@if test ! -d $(bin)$(binobj) ; then $(mkdir) -p $(bin)$(binobj) ; fi
#	$(echo) "STRUCTURED_OUTPUT="$(bin)$(binobj)
endif

ifdef use_requirements
$(use_requirements) : ;
endif

#-- end of make_header ------------------
# ============= call_command_header:begin =============
deps        = $(zip_TrackMonitors_python_modules_deps)
command     = $(zip_TrackMonitors_python_modules_command)
output      = $(zip_TrackMonitors_python_modules_output)

.PHONY: zip_TrackMonitors_python_modules zip_TrackMonitors_python_modulesclean

zip_TrackMonitors_python_modules :: $(output)

zip_TrackMonitors_python_modulesclean ::
	$(cmt_uninstallarea_command) $(output)

$(output):: $(deps)
	$(command)

FORCE:
# ============= call_command_header:end =============
#-- start of cleanup_header --------------

clean :: zip_TrackMonitors_python_modulesclean ;
#	@cd .

ifndef PEDANTIC
.DEFAULT::
	$(echo) "(zip_TrackMonitors_python_modules.make) $@: No rule for such target" >&2
#	@echo "#CMT> Warning: $@: No rule for such target" >&2; exit
	if echo $@ | grep '$(package)setup\.make$$' >/dev/null; then\
	 echo "$(CMTMSGPREFIX)" "(zip_TrackMonitors_python_modules.make): $@: File no longer generated" >&2; exit 0; fi
else
.DEFAULT::
	$(echo) "(zip_TrackMonitors_python_modules.make) PEDANTIC: $@: No rule for such target" >&2
	if echo $@ | grep '$(package)setup\.make$$' >/dev/null; then\
	 echo "$(CMTMSGPREFIX)" "(zip_TrackMonitors_python_modules.make): $@: File no longer generated" >&2; exit 0;\
	 elif test $@ = "$(cmt_final_setup)" -o\
	 $@ = "$(cmt_final_setup_zip_TrackMonitors_python_modules)" ; then\
	 found=n; for s in 1 2 3 4 5; do\
	 sleep $$s; test ! -f $@ || { found=y; break; }\
	 done; if test $$found = n; then\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(zip_TrackMonitors_python_modules.make) PEDANTIC: $@: Seems to be missing. Ignore it for now" >&2; exit 0 ; fi;\
	 elif test `expr $@ : '.*/'` -ne 0 ; then\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(zip_TrackMonitors_python_modules.make) PEDANTIC: $@: Seems to be a missing file. Please check" >&2; exit 2 ; \
	 else\
	 test -z "$(cmtmsg)" ||\
	 echo "$(CMTMSGPREFIX)" "(zip_TrackMonitors_python_modules.make) PEDANTIC: $@: Seems to be a fake target due to some pattern. Just ignore it" >&2 ; exit 0; fi
endif

zip_TrackMonitors_python_modulesclean ::
#-- end of cleanup_header ---------------
