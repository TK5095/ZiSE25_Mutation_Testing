# Architectural constraints for the temp_alert application

-doc_begin="Define all components of the project."

# BUZZER
-file_tag+={buzzer, "^.*/src/buzzer\\.c$"}
-file_tag+={buzzer, "^.*/inc/buzzer\\.h$"}
-config=B.INDEPENDENCE,component_files+=
  {BUZZER,"buzzer"}
-config=B.INDEPENDENCE,component_entities+=
  {BUZZER,content,"any_decl(loc(top(file(buzzer))))"}
-config=B.INDEPENDENCE,component_macros+=
  {BUZZER,macro_file,"loc(top(file(buzzer)))"}

# DISPLAY
-file_tag+={display, "^.*/src/(display|tm1637)\\.c$"}
-file_tag+={display, "^.*/inc/(display|tm1637)\\.h$"}
-config=B.INDEPENDENCE,component_files+=
  {DISPLAY,"display"}
-config=B.INDEPENDENCE,component_entities+=
  {DISPLAY,content,"any_decl(loc(top(file(display))))"}
-config=B.INDEPENDENCE,component_macros+=
  {DISPLAY,macro_file,"loc(top(file(display)))"}

# LEDS
-file_tag+={leds, "^.*/src/leds\\.c$"}
-file_tag+={leds, "^.*/inc/leds\\.h$"}
-config=B.INDEPENDENCE,component_files+=
  {LEDS,"leds"}
-config=B.INDEPENDENCE,component_entities+=
  {LEDS,content,"any_decl(loc(top(file(leds))))"}
-config=B.INDEPENDENCE,component_macros+=
  {LEDS,macro_file,"loc(top(file(leds)))"}

# APPLICATION
-file_tag+={application, "^.*/src/main\\.c$"}
-config=B.INDEPENDENCE,component_files+=
  {APPLICATION,"application"}
-config=B.INDEPENDENCE,component_entities+=
  {APPLICATION,content,"any_decl(loc(top(file(application))))"}
-config=B.INDEPENDENCE,component_macros+=
  {APPLICATION,macro_file,"loc(top(file(application)))"}

# UTILS
-file_tag+={utils, "^.*/inc/utils\\.h$"}
-config=B.INDEPENDENCE,component_files+=
  {UTILS,"utils"}
-config=B.INDEPENDENCE,component_entities+=
  {UTILS,content,"any_decl(loc(top(file(utils))))"}
-config=B.INDEPENDENCE,component_macros+=
  {UTILS,macro_file,"loc(top(file(utils)))"}

# ZEPHYR ATOMIC
-file_tag+={zep_atomic, "^.*include/zephyr/.*atomic.*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/ATOMIC,"zep_atomic"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/ATOMIC,content,"any_decl(loc(top(file(zep_atomic))))"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/ATOMIC,macro_file,"loc(top(file(zep_atomic)))"}

# ZEPHYR MMIO
-file_tag+={zep_mmio, "^.*include/zephyr/.*(gpio|mmio).*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/MMIO,"zep_mmio"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/MMIO,content,"any_decl(loc(top(file(zep_mmio))))"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/MMIO,macro_file,"loc(top(file(zep_mmio)))"}

# ZEPHYR SENSOR
-file_tag+={zep_sensor, "^.*include/zephyr/.*sensor.*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/SENSOR,"zep_sensor"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/SENSOR,content,"any_decl(loc(top(file(zep_sensor))))"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/SENSOR,macro_file,"loc(top(file(zep_sensor)))"}

# ZEPHYR DEVICE_TREE
-file_tag+={zep_device_tree, "^.*include/zephyr/.*device.*tree.*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/DEVICE_TREE,"zep_device_tree"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/DEVICE_TREE,content,"any_decl(loc(top(file(zep_device_tree))))"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/DEVICE_TREE,macro_file,"loc(top(file(zep_device_tree)))"}

# ZEPHYR LOGGING
-file_tag+={zep_logging, "^.*include/zephyr/logging.*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/LOGGING,"zep_logging"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/LOGGING,content,"any_decl(loc(top(file(zep_logging))))"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/LOGGING,macro_file,"loc(top(file(zep_logging)))"}

# ZEPHYR THREADING
-file_tag+={zep_threading, "^.*include/zephyr/.*thread.*$"}
-entity_selector+={zep_threading_decls, "any_decl(loc(top(file(^.*include/zephyr/kernel.*$)))&&^.*(thread|THREAD).*$)"}
-macro_selector+={zep_threading_macros, "loc(top(file(^.*include/zephyr/kernel.*$)))&&^.*(thread|THREAD).*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/THREADING,"zep_threading"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/THREADING,content,"zep_threading_decls"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/THREADING,macro_file,"zep_threading_macros"}

# ZEPHYR TIMING
-file_tag+={zep_timing, "^.*include/zephyr/.*time.*$"}
-entity_selector+={zep_timing_decls, "any_decl(loc(top(file(^.*include/zephyr/kernel.*$)))&&^.*k_(sleep|busy_wait).*$)"}
-macro_selector+={zep_timing_macros, "loc(top(file(^.*include/zephyr/kernel.*$)))&&^.*K_(M|U)?SEC.*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/TIMING,"zep_timing"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/TIMING,content,"zep_timing_decls"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/TIMING,macro_file,"zep_timing_macros"}

# ZEPHYR KERNEL
-file_tag+={zep_kernel, "^.*include/zephyr/kernel.*$"}
-config=B.INDEPENDENCE,component_files+=
  {ZEP/KERNEL,"zep_kernel"}
-config=B.INDEPENDENCE,component_entities+=
  {ZEP/KERNEL,content,"any_decl(loc(top(file(zep_kernel))))&&!(zep_threading_decls||zep_timing_decls)"}
-config=B.INDEPENDENCE,component_macros+=
  {ZEP/KERNEL,macro_file,"loc(top(file(zep_kernel)))&&!(zep_threading_macros||zep_timing_macros )"}

-doc_begin="Keep all the variables and functions under check."
-config=B.INDEPENDENCE,all_component_entities+="kind(var||function)"
-doc_end

-doc_begin="All user-defined macros are interesting"
-config=B.INDEPENDENCE,all_component_macros+="loc(top(file(kind(user||main_file))))"
-doc_end

# LAYERING

-doc="APPLICATION can use BUZZER, DISPLAY and LEDS components."
-config=B.INDEPENDENCE,component_allows+=
  "from(APPLICATION)&&to(BUZZER||DISPLAY||LEDS)&&action(include||call||expand||read)"

-doc="APPLICATION can include and call ZEP/SENSOR to read temperature."
-config=B.INDEPENDENCE,component_allows+=
  "from(APPLICATION)&&to(ZEP/SENSOR)&&action(include||call)"

# TODO maybe this belongs to interface visibility
-doc="APPLICATION can include the ZEP/KERNEL headers."
-config=B.INDEPENDENCE,component_allows+=
  "from(APPLICATION)&&to(ZEP/KERNEL)&&action(include)"

# Hardware access isolation

-doc="BUZZER, DISPLAY LEDS can include ZEP/MMIO component."
-config=B.INDEPENDENCE,component_allows+=
  "from(BUZZER||DISPLAY||LEDS)&&to(ZEP/MMIO)&&action(include||expand||call)"

-doc="BUZZER, DISPLAY and LEDS use Devicetree component."
-config=B.INDEPENDENCE,component_allows+=
  "from(BUZZER||DISPLAY||LEDS)&&to(ZEP/DEVICE_TREE)&&action(include||expand||call)"

# Data ownership

# TODO implement only \verb|APPLICATION| (\texttt{temp\_thread\_fn}) may write
# the shared temperature and alarm flag; \verb|BUZZER| and \verb|LEDS|
# may only read.

# Interface visibiliry

-doc="APPLICATION, BUZZER, DISPLAY and LEDS make use of threading, timing and logging."
-config=B.INDEPENDENCE,component_allows+=
  "from(APPLICATION||BUZZER||DISPLAY||LEDS)&&to(ZEP/THREADING||ZEP/TIMING||ZEP/LOGGING)&&action(expand||call||include)"

-doc="BUZZER and LEDS use atomic operations."
-config=B.INDEPENDENCE,component_allows+=
  "from(APPLICATION||BUZZER||LEDS)&&to(ZEP/ATOMIC)&&action(include||expand||call)"

-doc="BUZZER and LEDS can use UTILS component."
-config=B.INDEPENDENCE,component_allows+=
  "from(APPLICATION||BUZZER||LEDS)&&to(UTILS)&&action(include||expand)"

# Other

-doc="Allow zephyr components to use each other."
-config=B.INDEPENDENCE,component_allows+=
  "from(ZEP/ATOMIC||ZEP/MMIO||ZEP/SENSOR||ZEP/DEVICE_TREE||ZEP/LOGGING||ZEP/KERNEL||ZEP/THREADING||ZEP/TIMING)",
  "to(ZEP/ATOMIC||ZEP/MMIO||ZEP/SENSOR||ZEP/DEVICE_TREE||ZEP/LOGGING||ZEP/KERNEL||ZEP/THREADING||ZEP/TIMING)&&!from(APPLICATION||BUZZER||DISPLAY||LEDS||UTILS)"

-config=B.INDEPENDENCE,show_component_files+="undefined"
-config=B.INDEPENDENCE,show_component_entities+="any()"
-config=B.INDEPENDENCE,show_component_macros+="any()"