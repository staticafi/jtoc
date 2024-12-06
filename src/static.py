import logging
import sys

from pathlib import Path


# ========== PATHS SECTION ==========

ROOT = Path(__file__).resolve().parent.parent

SOURCE_DIR = ROOT / 'src'
TEST_DIR = ROOT / 'tests'
BENCHMARKS_DIR = ROOT / 'java_benchmarks'
CAPTURE_DIR = ROOT / 'capture'
COMPILE_DIR = ROOT / 'out'
JBMC = SOURCE_DIR / 'jbmc' / 'jbmc'

CAPTURE_DIR.mkdir(exist_ok=True)
COMPILE_DIR.mkdir(exist_ok=True)

INDENT_WIDTH = 4


# ========== LOGGER SECTION ==========

sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))

logger = logging.getLogger('jtoc')
logger.addHandler(sh)
logger.setLevel(logging.INFO)


# ========== JTOC LIBRARY SECTION ==========

JTOC_LIBRARY_FUNCTIONS = {
    '___java_lang_String__init___',
    '___java_lang_StringBuffer__init_String___',
    '___java_lang_StringBuffer__init___',
    '___java_lang_StringBuilder__init___',
    '___java_lang_StringBuilder__init_I___',
    '___java_lang_StringBuilder__init_CharSequence___',
    '___java_lang_StringBuilder__init_String___',

    'compareTo_java_lang_String__String_I',
    'concat_java_lang_String__String_String',
    'contains_java_lang_String__CharSequence_Z',
    'equals_java_lang_String__Object_Z',
    'endsWith_java_lang_String__String_Z',
    'equalsIgnoreCase_java_lang_String__String_Z',
    'indexOf_java_lang_String__I_I',
    'indexOf_java_lang_String__II_I',
    'indexOf_java_lang_String__String_I',
    'indexOf_java_lang_String__StringI_I',
    'isEmpty_java_lang_String___Z',
    'length_java_lang_String___I',
    'lastIndexOf_java_lang_String__I_I',
    'lastIndexOf_java_lang_String__II_I',
    'lastIndexOf_java_lang_String__String_I',
    'lastIndexOf_java_lang_String__StringI_I',
    'replace_java_lang_String__CC_String',
    'replace_java_lang_String__CharSequenceCharSequence_String',
    'startsWith_java_lang_String__String_Z',
    'startsWith_java_lang_String__StringI_Z',
    'toLowerCase_java_lang_String___String',
    'toString_java_lang_String___String',
    'toUpperCase_java_lang_String___String',
    'trim_java_lang_String___String',

    'append_java_lang_StringBuffer__C_StringBuffer',
    'append_java_lang_StringBuffer__String_StringBuffer',
    'append_java_lang_StringBuffer__StringBuffer_StringBuffer',
    'appendCodePoint_java_lang_StringBuffer__I_StringBuffer',
    'charAt_java_lang_StringBuffer__I_C',
    'codePointAt_java_lang_StringBuffer__I_I',
    'codePointBefore_java_lang_StringBuffer__I_I',
    'codePointCount_java_lang_StringBuffer__II_I',
    'length_java_lang_StringBuffer___I',
    'substring_java_lang_StringBuffer__I_String',
    'toString_java_lang_StringBuffer___String',

    'append_java_lang_StringBuilder__C_StringBuilder',
    'append_java_lang_StringBuilder__CharSequence_StringBuilder',
    'append_java_lang_StringBuilder__String_StringBuilder',
    'append_java_lang_StringBuilder__StringBuffer_StringBuilder',
    'appendCodePoint_java_lang_StringBuilder__I_StringBuilder',
    'charAt_java_lang_StringBuilder__I_C',
    'codePointAt_java_lang_StringBuilder__I_I',
    'codePointBefore_java_lang_StringBuilder__I_I',
    'codePointCount_java_lang_StringBuilder__II_I',
    'length_java_lang_StringBuilder___I',
    'substring_java_lang_StringBuilder__I_String',
    'substring_java_lang_StringBuilder__II_String',
    'toString_java_lang_StringBuilder___String',

    'charAt_java_lang_CharSequence__I_C',
    'length_java_lang_CharSequence___I',
    'toString_java_lang_CharSequence___String',

    'assume_org_sosy_lab_sv_benchmarks_Verifier__Z_V',
    'nondetBoolean_org_sosy_lab_sv_benchmarks_Verifier___Z',
    'nondetByte_org_sosy_lab_sv_benchmarks_Verifier___B',
    'nondetChar_org_sosy_lab_sv_benchmarks_Verifier___C',
    'nondetDouble_org_sosy_lab_sv_benchmarks_Verifier___D',
    'nondetFloat_org_sosy_lab_sv_benchmarks_Verifier___F',
    'nondetInt_org_sosy_lab_sv_benchmarks_Verifier___I',
    'nondetLong_org_sosy_lab_sv_benchmarks_Verifier___J',
    'nondetShort_org_sosy_lab_sv_benchmarks_Verifier___S',
    'nondetString_org_sosy_lab_sv_benchmarks_Verifier___String',

    'println_java_io_PrintStream___V',
    'println_java_io_PrintStream__C_V',
    'println_java_io_PrintStream__D_V',
    'println_java_io_PrintStream__F_V',
    'println_java_io_PrintStream__I_V',
    'println_java_io_PrintStream__J_V',
    'println_java_io_PrintStream__Z_V',
    'println_java_io_PrintStream__Object_V',
    'println_java_io_PrintStream__String_V',
}


JTOC_LIBRARY_STRUCTS = {
    'java_lang_Object',
    'java_lang_AbstractStringBuilder',
    'java_lang_CharSequence',
    'java_lang_String',
    'java_lang_StringBuilder',
    'java_lang_StringBuffer',
    'java_io_PrintStream',
    'org_sosy_lab_sv_benchmarks_Verifier'
}


JTOC_LIBRARY_STATIC = [
    'java_lang_CharSequence_charAt__I_C_return_value',
    'java_lang_CharSequence_length___I_return_value',
    'java_lang_CharSequence_toString___Ljava_lang_String__return_value',
    'java_lang_StringBuffer_appendCodePoint__I_Ljava_lang_StringBuffer__return_value',
    'java_lang_StringBuffer_append__C_Ljava_lang_StringBuffer__return_value',
    'java_lang_StringBuffer_append__Ljava_lang_StringBuffer__Ljava_lang_StringBuffer__return_value',
    'java_lang_StringBuffer_append__Ljava_lang_String__Ljava_lang_StringBuffer__return_value',
    'java_lang_StringBuffer_charAt__I_C_return_value',
    'java_lang_StringBuffer_codePointAt__I_I_return_value',
    'java_lang_StringBuffer_codePointBefore__I_I_return_value',
    'java_lang_StringBuffer_codePointCount__II_I_return_value',
    'java_lang_StringBuffer_length___I_return_value',
    'java_lang_StringBuffer_substring__I_Ljava_lang_String__return_value',
    'java_lang_StringBuffer_toString___Ljava_lang_String__return_value',
    'java_lang_StringBuilder_appendCodePoint__I_Ljava_lang_StringBuilder__return_value',
    'java_lang_StringBuilder_append__C_Ljava_lang_StringBuilder__return_value',
    'java_lang_StringBuilder_append__Ljava_lang_CharSequence__Ljava_lang_StringBuilder__return_value',
    'java_lang_StringBuilder_append__Ljava_lang_StringBuffer__Ljava_lang_StringBuilder__return_value',
    'java_lang_StringBuilder_append__Ljava_lang_String__Ljava_lang_StringBuilder__return_value',
    'java_lang_StringBuilder_charAt__I_C_return_value',
    'java_lang_StringBuilder_codePointAt__I_I_return_value',
    'java_lang_StringBuilder_codePointBefore__I_I_return_value',
    'java_lang_StringBuilder_codePointCount__II_I_return_value',
    'java_lang_StringBuilder_length___I_return_value',
    'java_lang_StringBuilder_substring__II_Ljava_lang_String__return_value',
    'java_lang_StringBuilder_substring__I_Ljava_lang_String__return_value',
    'java_lang_StringBuilder_toString___Ljava_lang_String__return_value',
    'java_lang_String_compareTo__Ljava_lang_String__I_return_value',
    'java_lang_String_concat__Ljava_lang_String__Ljava_lang_String__return_value',
    'java_lang_String_contains__Ljava_lang_CharSequence__Z_return_value',
    'java_lang_String_endsWith__Ljava_lang_String__Z_return_value',
    'java_lang_String_equals__Ljava_lang_Object__Z_return_value',
    'java_lang_String_equalsIgnoreCase__Ljava_lang_String__Z_return_value',
    'java_lang_String_indexOf__II_I_return_value',
    'java_lang_String_indexOf__I_I_return_value',
    'java_lang_String_indexOf__Ljava_lang_String_I_I_return_value',
    'java_lang_String_indexOf__Ljava_lang_String__I_return_value',
    'java_lang_String_isEmpty___Z_return_value',
    'java_lang_String_lastIndexOf__II_I_return_value',
    'java_lang_String_lastIndexOf__I_I_return_value',
    'java_lang_String_lastIndexOf__Ljava_lang_String_I_I_return_value',
    'java_lang_String_lastIndexOf__Ljava_lang_String__I_return_value',
    'java_lang_String_length___I_return_value',
    'java_lang_String_replace__CC_Ljava_lang_String__return_value',
    'java_lang_String_replace__Ljava_lang_CharSequence_Ljava_lang_CharSequence__Ljava_lang_String__return_value',
    'java_lang_String_startsWith__Ljava_lang_String_I_Z_return_value',
    'java_lang_String_startsWith__Ljava_lang_String__Z_return_value',
    'java_lang_String_toLowerCase___Ljava_lang_String__return_value',
    'java_lang_String_toString___Ljava_lang_String__return_value',
    'java_lang_String_toUpperCase___Ljava_lang_String__return_value',
    'java_lang_String_trim___Ljava_lang_String__return_value',

    'org_sosy_lab_sv_benchmarks_Verifier_nondetBoolean___Z_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetByte___B_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetChar___C_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetDouble___D_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetFloat___F_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetInt___I_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetLong___J_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetShort___S_return_value',
    'org_sosy_lab_sv_benchmarks_Verifier_nondetString___Ljava_lang_String__return_value',
]
