# Project-wide deviations for temp_alert

## General deviations

-file_tag+={application_files,"^.*/ZiSe25/ZiSe25/(src|inc)/.*$"}
-source_files+={hide, "!application_files"}

-reports+={adopted, "all_area(all_loc(file(!application_files)))"}

## Guideline-specific tailoring

-config=MC4.R5.10,reports+={adopted, "any_area(any_loc(any_exp(macro(name(LOG_MODULE_DECLARE||Z_LOG2)))))"}

-doc_begin="Allow pointers of non-character type as long as the pointee is const-qualified."
-config=MC4.R7.4,same_pointee=false
-doc_end

-doc_begin="Allow Zephyr macros to be not MISRA compliant."
-config=MC4.R10.1,reports+={adopted, "any_area(any_loc(any_exp(macro(name(LOG_MODULE_DECLARE||LOG_ERR||z_tmcvt_divisor)))))"}
-doc_end

-config=MC4.R20.7,arg_expansion={safe, safe}

-remap_rtag={adopted, hide}
