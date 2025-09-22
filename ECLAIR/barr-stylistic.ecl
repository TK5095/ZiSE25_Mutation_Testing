-enable=NC3.1.2.a
-enable=NC3.1.3.b
-enable=NC3.1.5.a
-enable=NC3.1.5.b
-enable=NC3.1.6.a
-enable=NC3.2.1.a
-enable=NC3.2.2.a
-enable=NC3.2.2.b
#-enable=NC3.2.2.c
-enable=NC3.2.2.d
#-enable=NC3.2.2.e
#-enable=NC3.2.2.f
#-enable=NC3.2.2.g
-enable=NC3.2.2.h
#-enable=NC3.2.2.i
-enable=NC3.3.1.a
-enable=NC3.3.1.b
-enable=NC3.3.1.c
-enable=NC3.3.1.d
-enable=NC3.3.1.e
-enable=NC3.3.1.f
-enable=NC3.3.1.g
-enable=NC3.3.1.h
-enable=NC3.3.1.i
-enable=NC3.3.1.j
-enable=NC3.3.1.k
-enable=NC3.3.1.l
-enable=NC3.3.1.m
-enable=NC3.3.2.a
-enable=NC3.3.2.b
-enable=NC3.3.2.c
-enable=NC3.3.2.d
-enable=NC3.3.3.a
-enable=NC3.3.3.b
-enable=NC3.3.3.c
-enable=NC3.3.4.a
-enable=NC3.3.4.b
#-enable=NC3.3.4.c
-enable=NC3.3.5.a
-enable=NC3.3.6.a
-enable=NC3.3.6.b
-enable=NC3.4.1.a
#-enable=NC3.4.1.b
-enable=NC3.4.1.c
-enable=NC3.4.1.d
#-enable=NC3.4.3.a
-enable=NC3.4.3.b
-enable=NC3.4.3.c
-enable=NC3.4.3.d
#-enable=NC3.4.3.e
-enable=NC3.4.3.f
-enable=NC3.5.1.a
-enable=NC3.5.1.b
-enable=NC3.5.1.c
-enable=NC3.6.1.e
-enable=NC3.6.1.f
-enable=NC3.6.1.g
#-enable=NC3.6.1.h
#-enable=NC3.6.1.i
#-disable=NC3.6.1.i
-enable=NC3.6.2.a
-enable=NC3.6.2.b
#-enable=NC3.6.4.a
#-enable=NC3.6.5.b
-enable=NC3.7.1.e
-enable=NC3.7.1.f
-enable=NC3.7.1.g
-enable=NC3.7.1.h
#-enable=NC3.7.1.i
-enable=NC3.7.1.j
-enable=NC3.7.1.k
-enable=NC3.7.1.l
#-enable=NC3.7.1.m
-enable=NC3.7.1.n
-enable=NC3.7.1.o
-enable=NC3.7.2.b
-enable=NC3.7.2.c
-enable=NC3.8.2.a
-enable=NC3.8.3.a
-enable=NC3.8.6.a

-doc="Constraints on the number of comments and their length lead to useless comments that are counterproductive."
-disable=NC3.2.2.d

-doc_begin="Disable the stylistic BARR-C guideline on naming conventions
for project entities, as the project has its own naming conventions."
-disable=NC3.5.1.c
-doc_end

-doc_begin="Variables in the project are allowed to be shorter than three characters."
-disable=NC3.7.1.e
-doc_end

-doc="Unit of measure Celsius begins with capital letter: allow to use Cd as an abbreviation of Celsius degrees."
-config=NC3.7.1.f,misnamed_entity_fmt={hide,"any()","^.*Cd.*$","vocab_msg"}

-doc_begin="Extend accepted documentation of casts using comments containing 'valid range'."
-ignored_comments-=__eclair_rtag_comments
-config=NC3.1.6.a,cast_doc_matcher="^(?:\n|.)*valid range(?:\n|.)*$||__document_cast_comments"
-doc_end
