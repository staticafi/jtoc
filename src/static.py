import logging
import sys

from pathlib import Path


# ========== PATHS SECTION ==========

ROOT = Path(__file__).resolve().parent.parent

SOURCE_DIR = ROOT / 'src'
TEST_DIR = ROOT / 'tests'
BENCHMARKS_DIR = ROOT / 'java_benchmarks'
JBMC = SOURCE_DIR / 'jbmc' / 'jbmc'
CAPTURE_DIR = SOURCE_DIR / 'capture'
COMPILE_DIR = SOURCE_DIR / 'build'

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
    'java::java.lang.String.<init>:()V',
    'java::java.lang.String.compareTo:(Ljava/lang/String;)I',
    'java::java.lang.String.concat:(Ljava/lang/String;)Ljava/lang/String;',
    'java::java.lang.String.contains:(Ljava/lang/CharSequence;)Z',
    'java::java.lang.String.endsWith:(Ljava/lang/String;)Z',
    'java::java.lang.String.equals:(Ljava/lang/Object;)Z',
    'java::java.lang.String.equalsIgnoreCase:(Ljava/lang/String;)Z',
    'java::java.lang.String.indexOf:(I)I',
    'java::java.lang.String.indexOf:(II)I',
    'java::java.lang.String.indexOf:(Ljava/lang/String;)I',
    'java::java.lang.String.indexOf:(Ljava/lang/String;I)I',
    'java::java.lang.String.isEmpty:()Z',
    'java::java.lang.String.lastIndexOf:(I)I',
    'java::java.lang.String.lastIndexOf:(II)I',
    'java::java.lang.String.lastIndexOf:(Ljava/lang/String;)I',
    'java::java.lang.String.lastIndexOf:(Ljava/lang/String;I)I',
    'java::java.lang.String.length:()I',
    'java::java.lang.String.replace:(CC)Ljava/lang/String;',
    'java::java.lang.String.replace:(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;',
    'java::java.lang.String.startsWith:(Ljava/lang/String;)Z',
    'java::java.lang.String.startsWith:(Ljava/lang/String;I)Z',
    'java::java.lang.String.toLowerCase:()Ljava/lang/String;',
    'java::java.lang.String.toString:()Ljava/lang/String;',
    'java::java.lang.String.toUpperCase:()Ljava/lang/String;',
    'java::java.lang.String.trim:()Ljava/lang/String;',
    'java::java.lang.StringBuilder.<init>:(Ljava/lang/String;)V',
    'java::java.lang.StringBuilder.<init>:(Ljava/lang/CharSequence;)V',
    'java::java.lang.StringBuilder.<init>:()V',
    'java::java.lang.StringBuilder.<init>:(I)V',
    'java::java.lang.StringBuilder.append:(C)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.append:(Ljava/lang/CharSequence;)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.append:(Ljava/lang/StringBuffer;)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.appendCodePoint:(I)Ljava/lang/StringBuilder;',
    'java::java.lang.StringBuilder.charAt:(I)C',
    'java::java.lang.StringBuilder.codePointAt:(I)I',
    'java::java.lang.StringBuilder.codePointBefore:(I)I',
    'java::java.lang.StringBuilder.codePointCount:(II)I',
    'java::java.lang.StringBuilder.length:()I',
    'java::java.lang.StringBuilder.substring:(II)Ljava/lang/String;',
    'java::java.lang.StringBuilder.substring:(I)Ljava/lang/String;',
    'java::java.lang.StringBuilder.toString:()Ljava/lang/String;',
    'java::java.lang.StringBuffer.<init>:(Ljava/lang/String;)V',
    'java::java.lang.StringBuffer.<init>:()V',
    'java::java.lang.StringBuffer.append:(C)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.append:(Ljava/lang/String;)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.append:(Ljava/lang/StringBuffer;)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.appendCodePoint:(I)Ljava/lang/StringBuffer;',
    'java::java.lang.StringBuffer.charAt:(I)C',
    'java::java.lang.StringBuffer.codePointAt:(I)I',
    'java::java.lang.StringBuffer.codePointBefore:(I)I',
    'java::java.lang.StringBuffer.codePointCount:(II)I',
    'java::java.lang.StringBuffer.length:()I',
    'java::java.lang.StringBuffer.substring:(I)Ljava/lang/String;',
    'java::java.lang.StringBuffer.toString:()Ljava/lang/String;',
    'java::java.lang.CharSequence.charAt:(I)C',
    'java::java.lang.CharSequence.toString:()Ljava/lang/String;',
    'java::java.lang.CharSequence.length:()I',

    'java::java.io.PrintStream.println:()V',
    'java::java.io.PrintStream.println:(C)V',
    'java::java.io.PrintStream.println:(D)V',
    'java::java.io.PrintStream.println:(F)V',
    'java::java.io.PrintStream.println:(I)V',
    'java::java.io.PrintStream.println:(J)V',
    'java::java.io.PrintStream.println:(Z)V',
    'java::java.io.PrintStream.println:(Ljava/lang/Object;)V',
    'java::java.io.PrintStream.println:(Ljava/lang/String;)V',
}


JTOC_LIBRARY_STRUCTS = {
    'java_lang_Object',
    'java_lang_AbstractStringBuilder',
    'java_lang_CharSequence',
    'java_lang_String',
    'java_lang_StringBuilder',
    'java_lang_StringBuffer',
    'java_io_PrintStream'
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
]
