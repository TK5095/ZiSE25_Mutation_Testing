-setq=data_dir,getenv('ECLAIR_DATA_DIR')

-enable=B.REPORT.ECB
-config=B.REPORT.ECB,output=join_paths(data_dir,"FRAME.@FRAME@.ecb")
-config=B.REPORT.ECB,tags=show

-enable=B.GCOV

-doc="Zephyr thread functions are designed to run indefinitely and never return.
Zero return coverage is expected and correct behavior."
-config=B.GCOV,reports+={deliberate,"any_area(^.*?function .*?_thread_fn called \\d+ returned 0.*$)"}
