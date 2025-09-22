# Requirements set definitions.

# Load the configuration template
-eval_file=""install_dir"/share/config/recipes/REQMAN.ecl"

-eval_file="temp_alert.sdoc.ecl"

-doc_begin="Coverage targets for each requirement set and implementation coverage.
This configuration specifies where the requirements for a given set and coverage should be expected."
-config=MC4.D3.1,coverage_target+={"target(kind(object)&&^.*?(build|twister-out.*?)/.*/app\\.dir/.*/(src|inc)/.*$)","set(SRS)&&cov(IMPLEMENT)"}
-doc_end

-doc_begin="Coverage targets for each requirement set and testing coverage.
This configuration specifies where the requirements for a given set and coverage should be expected."
-config=MC4.D3.1,coverage_target+={
    "target(kind(object)&&^.*?(build|twister-out.*?)/.*/app\\.dir/test_.*$)",
    "set(SRS)&&cov(TEST)"
}
-doc_end

-doc_begin="Covering constructs for each requirement set and coverage.
This configuration specifies the code constructs that are expected to be associated to requirements."
-file_tag+={App, "^.*(src|inc)/.*\\.(c|h)$"}
-config=MC4.D3.1,covering_construct+={
    decl,
    "loc(file(App))&&kind(function)",
    "set(SRS)&&cov(IMPLEMENT)"
}

-file_tag+={App_UT, "^.*?tests/test_temp_alert/.*\\.c$"}
-config=MC4.D3.1,covering_construct+={
    decl,
    "loc(any_exp(file(App_UT)))&&kind(var)&&^z_ztest_unit_test_stats_.*$",
    "set(SRS)&&cov(TEST)"
}
-doc_end

-doc_begin="Doxygen comments (either single-line or multi-line) are
parsed to extract requirement identifiers."
-config=MC4.D3.1,requirement_replacer+=doxygen_comment
-config=MC4.D3.1,requirement_replacer+=doxygen_line_comment
-doc_end
