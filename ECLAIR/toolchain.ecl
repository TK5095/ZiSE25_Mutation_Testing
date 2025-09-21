# Toolchain assumptions for temp_alert

# compilers.
-file_tag+={zephyr_cc,"^/opt/zephyr-sdk-0.17.2/arm-zephyr-eabi/bin/arm-zephyr-eabi-gcc$"}

# Manuals.
-setq=GCC_MANUAL,"https://gcc.gnu.org/onlinedocs/gcc-13.1.0/gcc.pdf"
-setq=CPP_MANUAL,"https://gcc.gnu.org/onlinedocs/gcc-12.1.0/cpp.pdf"
-setq=ARM64_ABI_MANUAL,"https://github.com/ARM-software/abi-aa/blob/60a8eb8c55e999d74dac5e368fc9d7e36e38dda4/aapcs64/aapcs64.rst"
-setq=X86_64_ABI_MANUAL,"https://gitlab.com/x86-psABIs/x86-64-ABI/-/jobs/artifacts/master/raw/x86-64-ABI/abi.pdf?job=build"
-setq=ARM64_LIBC_MANUAL,"https://www.gnu.org/software/libc/manual/pdf/libc.pdf"
-setq=X86_64_LIBC_MANUAL,"https://www.gnu.org/software/libc/manual/pdf/libc.pdf"
-setq=C99_STD,"ISO/IEC 9899:1999"

-doc_begin="Non-standard token used by the project, with the relative documentation.
    __alignof__, __alignof: see Sections \"6.48 Alternate Keywords\" and \"6.44 Determining the Alignment of Functions, Types or Variables\" of "GCC_MANUAL".
    asm, __asm__: see Sections \"6.48 Alternate Keywords\" and \"6.47 How to Use Inline Assembly Language in C Code\" of "GCC_MANUAL".
    __attribute__: see Section \"6.39 Attribute Syntax\" of "GCC_MANUAL".
   __auto_type: see Sections \"6.13.5 Referring to a type with typeof\" of "GCC_MANUAL" and
                20.4 https://www.gnu.org/software/c-intro-and-ref/manual/html_node/Auto-Type.html.
   __const__: see Section \"6.4.1.1 Common Function Attributes\" of "GCC_MANUAL". 
   _Generic for C99
   _Static_assert for C99
   __thread: see Section \"6.6 Thread-Local Storage\" of "GCC_MANUAL".
   typeof, __typeof__: see Section \"6.7 Referring to a Type with typeof\" of "GCC_MANUAL".
   __volatile__: see Sections \"6.48 Alternate Keywords\" and \"6.47.2.1 Volatile\" of "GCC_MANUAL".
"
-name_selector+={alignof, "^(__alignof__|__alignof)$"}
-name_selector+={asm, "^(__asm__|asm)$"}
-name_selector+={attribute, "^__attribute__$"}
-name_selector+={auto_type, "^__auto_type$"}
-name_selector+={builtin_types_p, "^__builtin_types_compatible_p$"}
-name_selector+={const, "^__const__$"}
-name_selector+={generic, "^_Generic$"}
-name_selector+={static_assert, "^_Static_assert$"}
-name_selector+={thread, "^__thread$"}
-name_selector+={typeof, "^(__typeof__|typeof)$"}
-name_selector+={volatile, "^__volatile__$"}
-config=STD.tokenext,behavior+={c99, zephyr_cc,
"alignof||
asm||
attribute||
auto_type||
builtin_types_p||
const||
generic||
static_assert||
thread||
typeof||
volatile"
}
-doc_end

-doc_begin="See Section \"6.1 Statements and Declarations in Expressions\" of "GCC_MANUAL"."
-config=STD.stmtexpr,behavior+={c99,zephyr_cc,specified}
-doc_end

-doc_begin="See Section \"11.2 Implementation limits\" of "CPP_MANUAL"."
-config=STD.inclnest,behavior+={c99, zephyr_cc, 200}
-doc_end

-doc_begin="The number of macro identifiers in a file is limited only by available memory in the used toolchain; arbitrary high value specified.
See Section \"11.2 Implementation limits\" of "CPP_MANUAL"."
-config=STD.macident,behavior+={c99, zephyr_cc, 65535}
-doc_end

-doc_begin="A variadic macro is called without specifying any variadic argument.
This is a C23 extension, which is supported as a language extension for C99
by the toolchain used by the application."
-config=STD.diag,behavior={c99, zephyr_cc, "name(ext_c_missing_varargs_arg)"}
-doc_end

