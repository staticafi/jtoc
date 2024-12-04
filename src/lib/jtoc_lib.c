#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

// ========== STRING SECTION ==========

struct java_lang_Object
{
    const char * ___class_identifier___;
};

struct java_lang_AbstractStringBuilder
{
    const char * ___class_identifier___;
};

struct java_lang_CharSequence
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    char* data;
};

struct java_lang_String
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    char* data;
};

struct java_lang_StringBuilder
{
    struct java_lang_AbstractStringBuilder ___java_lang_AbstractStringBuilder___;
    int length;
    char* data;
};

struct java_lang_StringBuffer
{
    struct java_lang_AbstractStringBuilder ___java_lang_AbstractStringBuilder___;
    int length;
    char* data;
};


// ========== STRING STATIC SECTION ==========

int java_lang_String_compareTo__Ljava_lang_String__I_return_value = -1;
struct java_lang_String *java_lang_String_concat__Ljava_lang_String__Ljava_lang_String__return_value = NULL;
int java_lang_String_contains__Ljava_lang_CharSequence__Z_return_value = -1;
int java_lang_String_endsWith__Ljava_lang_String__Z_return_value = -1;
int java_lang_String_equalsIgnoreCase__Ljava_lang_String__Z_return_value = -1;
int java_lang_String_indexOf__I_I_return_value = -1;
int java_lang_String_indexOf__II_I_return_value = -1;
int java_lang_String_indexOf__Ljava_lang_String__I_return_value = -1;
int java_lang_String_indexOf__Ljava_lang_String_I_I_return_value = -1;
int java_lang_String_isEmpty___Z_return_value = -1;
int java_lang_String_lastIndexOf__I_I_return_value = -1;
int java_lang_String_lastIndexOf__II_I_return_value = -1;
int java_lang_String_lastIndexOf__Ljava_lang_String__I_return_value = -1;
int java_lang_String_lastIndexOf__Ljava_lang_String_I_I_return_value = -1;
int java_lang_String_length___I_return_value = -1;
struct java_lang_String *java_lang_String_replace__CC_Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_String_replace__Ljava_lang_CharSequence_Ljava_lang_CharSequence__Ljava_lang_String__return_value = NULL;
int java_lang_String_startsWith__Ljava_lang_String__Z_return_value = -1;
int java_lang_String_startsWith__Ljava_lang_String_I_Z_return_value = -1;
struct java_lang_String *java_lang_String_toLowerCase___Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_String_toString___Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_String_toUpperCase___Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_String_trim___Ljava_lang_String__return_value = NULL;

struct java_lang_StringBuilder *java_lang_StringBuilder_append__C_Ljava_lang_StringBuilder__return_value = NULL;
struct java_lang_StringBuilder *java_lang_StringBuilder_append__Ljava_lang_CharSequence__Ljava_lang_StringBuilder__return_value = NULL;
struct java_lang_StringBuilder *java_lang_StringBuilder_append__Ljava_lang_String__Ljava_lang_StringBuilder__return_value = NULL;
struct java_lang_StringBuilder *java_lang_StringBuilder_append__Ljava_lang_StringBuffer__Ljava_lang_StringBuilder__return_value = NULL;
struct java_lang_StringBuilder *java_lang_StringBuilder_appendCodePoint__I_Ljava_lang_StringBuilder__return_value = NULL;
int java_lang_StringBuilder_codePointAt__I_I_return_value = -1;
int java_lang_StringBuilder_codePointBefore__I_I_return_value = -1;
int java_lang_StringBuilder_codePointCount__II_I_return_value = -1;
char java_lang_StringBuilder_charAt__I_C_return_value = '\0';
int java_lang_StringBuilder_length___I_return_value = -1;
struct java_lang_String *java_lang_StringBuilder_substring__I_Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_StringBuilder_substring__II_Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_StringBuilder_toString___Ljava_lang_String__return_value = NULL;

struct java_lang_StringBuffer *java_lang_StringBuffer_append__C_Ljava_lang_StringBuffer__return_value = NULL;
struct java_lang_StringBuffer *java_lang_StringBuffer_append__Ljava_lang_String__Ljava_lang_StringBuffer__return_value = NULL;
struct java_lang_StringBuffer *java_lang_StringBuffer_append__Ljava_lang_StringBuffer__Ljava_lang_StringBuffer__return_value = NULL;
struct java_lang_StringBuffer *java_lang_StringBuffer_appendCodePoint__I_Ljava_lang_StringBuffer__return_value = NULL;
int java_lang_StringBuffer_codePointAt__I_I_return_value = -1;
int java_lang_StringBuffer_codePointBefore__I_I_return_value = -1;
int java_lang_StringBuffer_codePointCount__II_I_return_value = -1;
int java_lang_StringBuffer_length___I_return_value = -1;
struct java_lang_String *java_lang_StringBuffer_substring__I_Ljava_lang_String__return_value = NULL;
struct java_lang_String *java_lang_StringBuffer_toString___Ljava_lang_String__return_value = NULL;

char java_lang_CharSequence_charAt__I_C_return_value = '\0';
int java_lang_CharSequence_length___I_return_value = -1;
struct java_lang_String *java_lang_CharSequence_toString___Ljava_lang_String__return_value = NULL;


void ___java_lang_String__init___(struct java_lang_String *this)
{
    char *content = malloc(1);
    *content = '\0';
    *(this) = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, 0, content };
}


int compareTo_java_lang_String__String_I(struct java_lang_String *this, struct java_lang_String *other)
{
    int result = strcmp(this->data, other->data);
    java_lang_String_compareTo__Ljava_lang_String__I_return_value = result;
    return result;
}


struct java_lang_String *concat_java_lang_String__String_String(struct java_lang_String *this, struct java_lang_String *other)
{
    char *dest = malloc(this->length + other->length + 1);
    char *copy = strcpy(dest, this->data);
    char *content = strcat(dest, other->data);

    int length = this->length + other->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_String_concat__Ljava_lang_String__Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


bool contains_java_lang_String__CharSequence_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq) 
{
    bool result = strstr(this->data, seq->data) != NULL;
    java_lang_String_contains__Ljava_lang_CharSequence__Z_return_value = (int) result;
    return result;
}


bool endsWith_java_lang_String__String_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq) 
{
    bool result = false;
    if (this->length < seq->length) {
        result = false;
    } else {
        result = strcmp(this->data + this->length - seq->length, seq->data) == 0;
    }
    
    java_lang_String_endsWith__Ljava_lang_String__Z_return_value = (int) result;
    return result;
}


struct java_lang_String *toLowerCase_java_lang_String___String(struct java_lang_String *this)
{
    char *content = malloc(this->length + 1);
    int length = this->length;
    for (size_t index = 0; index <= this->length; index++) {
        int converted = tolower(this->data[index]);
        content[index] = (char) converted;
    }

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_String_toLowerCase___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


struct java_lang_String *toUpperCase_java_lang_String___String(struct java_lang_String *this)
{
    char *content = malloc(this->length + 1);
    int length = this->length;
    for (size_t index = 0; index <= this->length; index++) {
        int converted = toupper(this->data[index]);
        content[index] = (char) converted;
    }

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_String_toUpperCase___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


bool equalsIgnoreCase_java_lang_String__String_Z(struct java_lang_String *this, struct java_lang_CharSequence *other)
{
    struct java_lang_String *lowered_this = toLowerCase_java_lang_String___String(this);
    struct java_lang_String *lowered_other = toLowerCase_java_lang_String___String((struct java_lang_String *) other);

    bool result = strcmp(lowered_this->data, lowered_other->data) == 0;
    java_lang_String_equalsIgnoreCase__Ljava_lang_String__Z_return_value = (int) result;
    return result;
}


int indexOf_java_lang_String__I_I(struct java_lang_String *this, int ch)
{    
    char substr[2] = {ch, '\0'};
    char *pos = strstr(this->data, substr);
    int result = -1;

    if (pos == NULL) {
        result = -1;
    } else {
        result = pos - this->data;
    }

    java_lang_String_indexOf__I_I_return_value = result;
    return result;
}


int indexOf_java_lang_String__II_I(struct java_lang_String *this, int ch, int start_from)
{   
    int result = -1;

    if (start_from > this->length) {
        java_lang_String_indexOf__II_I_return_value = result;
        return -1;
    }

    char substr[2] = {ch, '\0'};
    char *pos = strstr(this->data + start_from, substr);
    if (pos == NULL) {
        result = -1;
    } else {
        result = pos - this->data;
    }

    java_lang_String_indexOf__II_I_return_value = result;
    return result;
}


int indexOf_java_lang_String__String_I(struct java_lang_String *this, struct java_lang_String *other)
{
    int result = -1;
    char *pos = strstr(this->data, other->data);
    if (pos == NULL) {
        result = -1;
    } else {
        result = pos - this->data;
    }

    java_lang_String_indexOf__Ljava_lang_String__I_return_value = result;
    return result;
}


int indexOf_java_lang_String__StringI_I(struct java_lang_String *this, struct java_lang_String *other, int start_from)
{
    int result = -1;

    if (start_from > this->length) {
        java_lang_String_indexOf__Ljava_lang_String_I_I_return_value = result;
        return -1;
    }

    char *pos = strstr(this->data + start_from, other->data);
    if (pos == NULL) {
        result = -1;
    } else {
        result = pos - this->data;
    }

    java_lang_String_indexOf__Ljava_lang_String_I_I_return_value = result;
    return result;
}


bool isEmpty_java_lang_String___Z(struct java_lang_String *this)
{
    bool result = strlen(this->data) == 0;
    java_lang_String_isEmpty___Z_return_value = (int) result;
    return result;
}


int lastIndexOf_java_lang_String__I_I(struct java_lang_String *this, int ch)
{
    char substr[2] = {ch, '\0'};
    char *last;
    char *pos = this->data;
    do {
        last = pos;
        pos = strstr(pos, substr);
    } while (pos != NULL);

    int result = -1;
    if (last == NULL) {
        result = -1;
    } else {
        result = last - this->data;
    }

    java_lang_String_lastIndexOf__I_I_return_value = result;
    return result; 
}


int lastIndexOf_java_lang_String__II_I(struct java_lang_String *this, int ch, int end_at)
{
    if (end_at > this->length) {
        java_lang_String_lastIndexOf__II_I_return_value = -1;
        return -1;
    }

    char replaced_letter = this->data[end_at + 1];
    this->data[end_at + 1] = '\0';

    char substr[2] = {ch, '\0'};
    char *last;
    char *pos = this->data;
    do {
        last = pos;
        pos = strstr(pos, substr);
    } while (pos != NULL);

    this->data[end_at + 1] = replaced_letter;
    
    int result = -1;
    if (last == NULL) {
        result = -1;
    } else {
        result = last - this->data;
    }

    java_lang_String_lastIndexOf__II_I_return_value = result;
    return result; 
}


int lastIndexOf_java_lang_String__String_I(struct java_lang_String *this, struct java_lang_String *other)
{
    char *last;
    char *pos = this->data;
    do {
        last = pos;
        pos = strstr(pos, other->data);
    } while (pos != NULL);

    int result = -1;
    if (last == NULL) {
        result = -1;
    } else {
        result = last - this->data;
    }

    java_lang_String_lastIndexOf__Ljava_lang_String__I_return_value = result;
    return result;
}


int lastIndexOf_java_lang_String__StringI_I(struct java_lang_String *this, struct java_lang_String *other, int end_at)
{
    if (end_at > this->length) {
        java_lang_String_lastIndexOf__Ljava_lang_String_I_I_return_value = -1;
        return -1;
    }

    char replaced_letter = this->data[end_at + 1];
    this->data[end_at + 1] = '\0';

    char *last;
    char *pos = this->data;
    do {
        last = pos;
        pos = strstr(pos, other->data);
    } while (pos != NULL);

    this->data[end_at + 1] = replaced_letter;
    
    int result = -1;
    if (last == NULL) {
        result = -1;
    } else {
        result = last - this->data;
    }

    java_lang_String_lastIndexOf__Ljava_lang_String_I_I_return_value = result;
    return result;
}


int length_java_lang_String___I(struct java_lang_String *this)
{
    java_lang_String_length___I_return_value = this->length;
    return this->length;
}


struct java_lang_String *replace_java_lang_String__CC_String(struct java_lang_String *this, char old, char new)
{
    int length = this->length;
    char *replaced = malloc(this->length + 1);
    strcpy(replaced, this->data);

    for (size_t index = 0; index < length; index++) {
        if (replaced[index] == old) {
            replaced[index] = new;
        }
    }

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, replaced };
    java_lang_String_replace__CC_Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


struct java_lang_String *replace_java_lang_String__CharSequenceCharSequence_String(struct java_lang_String *this, struct java_lang_CharSequence *old, struct java_lang_CharSequence *new)
{   
    int count = 0;
    const char *temp = this->data;
    while ((temp = strstr(temp, old->data)) != NULL) {
        count++;
        temp += old->length;
    }

    size_t new_str_len = this->length + count * (new->length - old->length) + 1;
    char *result = malloc(new_str_len);

    const char *current = this->data;
    char *dest = result;
    while ((temp = strstr(current, old->data)) != NULL) {
        size_t segment_len = temp - current;
        memcpy(dest, current, segment_len);
        dest += segment_len;
        
        memcpy(dest, new->data, new->length);
        dest += new->length;

        current = temp + old->length;
    }
    strcpy(dest, current);
    
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, new_str_len, result };
    java_lang_String_replace__Ljava_lang_CharSequence_Ljava_lang_CharSequence__Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


struct java_lang_String *toString_java_lang_String___String(struct java_lang_String *this)
{
    char *new_str = malloc(this->length + 1);
    strcpy(new_str, this->data);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, this->length, new_str };
    java_lang_String_toString___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


bool startsWith_java_lang_String__StringI_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq, int offset) 
{
    if (this->length - offset < seq->length) {
        java_lang_String_startsWith__Ljava_lang_String_I_Z_return_value = (int) false;
        return false;
    }

    struct java_lang_String *new_this = toString_java_lang_String___String(this);

    char replaced_letter = new_this->data[seq->length + offset];
    new_this->data[seq->length + offset] = '\0';

    bool result = strcmp(new_this->data + offset, seq->data) == 0;

    new_this->data[seq->length + offset] = replaced_letter;

    java_lang_String_startsWith__Ljava_lang_String_I_Z_return_value = (int) result;
    return result;
}


bool startsWith_java_lang_String__String_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq) 
{
    bool result = startsWith_java_lang_String__StringI_Z(this, seq, 0);

    java_lang_String_startsWith__Ljava_lang_String__Z_return_value = (int) result;
    return result;
}


struct java_lang_String *trim_java_lang_String___String(struct java_lang_String *this)
{
    struct java_lang_String *new_this = toString_java_lang_String___String(this);

    int start = 0;
    int end = new_this->length;

    while (new_this->data[start] == ' ') {
        start++;
    }

    while (new_this->data[end] == ' ' || new_this->data[end] == '\0') {
        end--;
    }

    int length = end - start;
    char *content = malloc(length + 1);
    new_this->data[end + 1] = '\0';
    strcpy(content, new_this->data + start);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_String_trim___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


// StringBuilder:


void ___java_lang_StringBuilder__init___(struct java_lang_StringBuilder *this)
{
    char *content = malloc(1);
    *content = '\0';
    int length = 0;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}

void ___java_lang_StringBuilder__init_I___(struct java_lang_StringBuilder *this, int capacity)
{
    // capacity arg is not used
    char *content = malloc(1);
    *content = '\0';
    int length = 0;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}

void ___java_lang_StringBuilder__init_String___(struct java_lang_StringBuilder *this, struct java_lang_String *str)
{

    char *content = malloc(str->length + 1);
    strcpy(content, str->data);
    int length = str->length;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}


void ___java_lang_StringBuilder__init_CharSequence___(struct java_lang_StringBuilder *this, struct java_lang_CharSequence *seq)
{
    char *content = malloc(seq->length + 1);
    strcpy(content, seq->data);
    int length = seq->length;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}


struct java_lang_StringBuilder *append_java_lang_StringBuilder__C_StringBuilder(struct java_lang_StringBuilder * this, char ch)
{
    int new_length = this->length + 1;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    new_str[this->length] = ch;
    new_str[this->length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuilder_append__C_Ljava_lang_StringBuilder__return_value = this;
    return this;
}


struct java_lang_StringBuilder *append_java_lang_StringBuilder__String_StringBuilder(struct java_lang_StringBuilder *this, struct java_lang_String *str)
{
    int new_length = this->length + str->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, str->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuilder_append__Ljava_lang_String__Ljava_lang_StringBuilder__return_value = this;
    return this;
}


struct java_lang_StringBuilder *append_java_lang_StringBuilder__CharSequence_StringBuilder(struct java_lang_StringBuilder *this, struct java_lang_CharSequence *seq)
{
    int new_length = this->length + seq->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, seq->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuilder_append__Ljava_lang_CharSequence__Ljava_lang_StringBuilder__return_value = this;
    return this;
}


struct java_lang_StringBuilder *append_java_lang_StringBuilder__StringBuffer_StringBuilder(struct java_lang_StringBuilder *this, struct java_lang_StringBuffer *buf)
{
    int new_length = this->length + buf->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, buf->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuilder_append__Ljava_lang_StringBuffer__Ljava_lang_StringBuilder__return_value = this;
    return this;
}


struct java_lang_StringBuilder *appendCodePoint_java_lang_StringBuilder__I_StringBuilder(struct java_lang_StringBuilder * this, int code_point)
{
    char ch;
    if (code_point & 0xff > 255) {
        // we do not support Unicode
        ch = code_point & 0xff;
    } else {
        ch = (char) code_point;
    }
    int new_length = this->length + 1;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    new_str[this->length] = ch;
    new_str[this->length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuilder_appendCodePoint__I_Ljava_lang_StringBuilder__return_value = this;
    return this;
}


char charAt_java_lang_StringBuilder__I_C(struct java_lang_StringBuilder *this, int index)
{
    if (index < 0 || index > this->length) {
        java_lang_StringBuilder_charAt__I_C_return_value = '\0';
        return '\0';
    }

    char result = this->data[index];
    java_lang_StringBuilder_charAt__I_C_return_value = result;
    return result;
}


char codePointAt_java_lang_StringBuilder__I_I(struct java_lang_StringBuilder *this, int index)
{
    if (index < 0 || index > this->length) {
        java_lang_StringBuilder_codePointAt__I_I_return_value = '\0';
        return '\0';
    }

    java_lang_StringBuilder_codePointAt__I_I_return_value = this->data[index];
    return this->data[index];
}


char codePointBefore_java_lang_StringBuilder__I_I(struct java_lang_StringBuilder *this, int index)
{
    if (index - 1 < 0 || index - 1 > this->length) {
        java_lang_StringBuilder_codePointBefore__I_I_return_value = '\0';
        return '\0';
    }

    java_lang_StringBuilder_codePointBefore__I_I_return_value = this->data[index - 1];
    return this->data[index - 1];
}


int codePointCount_java_lang_StringBuilder__II_I(struct java_lang_StringBuilder *this, int begin, int end)
{
    if (begin < 0 || end > this->length || begin > end) {
        java_lang_StringBuilder_codePointCount__II_I_return_value = '\0';
        return '\0';
    }

    java_lang_StringBuilder_codePointCount__II_I_return_value = end - begin;
    return end - begin;
}


int length_java_lang_StringBuilder___I(struct java_lang_StringBuilder *this)
{
    java_lang_StringBuilder_length___I_return_value = this->length;
    return this->length;
}


struct java_lang_String *substring_java_lang_StringBuilder__I_String(struct java_lang_StringBuilder *this, int begin)
{
    if (begin < 0 || begin > this->length) {
        java_lang_StringBuilder_substring__I_Ljava_lang_String__return_value = NULL;
        return NULL;
    }

    int length = this->length - begin;
    char *content = malloc(length + 1);
    strcpy(content, this->data + begin);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_StringBuilder_substring__I_Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


struct java_lang_String *substring_java_lang_StringBuilder__II_String(struct java_lang_StringBuilder *this, int begin, int end)
{
    if (begin < 0 || begin > this->length || end < 0 || end > this->length || begin > end) {
        java_lang_StringBuilder_substring__II_Ljava_lang_String__return_value = NULL;
        return NULL;
    }

    int length = end - begin;
    char *content = malloc(length + 1);
    char ch = this->data[end];
    this->data[end] = '\0';
    strcpy(content, this->data + begin);
    this->data[end] = ch;

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_StringBuilder_substring__II_Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


struct java_lang_String *toString_java_lang_StringBuilder___String(struct java_lang_StringBuilder *this)
{
    char *content = this->data;
    int length = this->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_StringBuilder_toString___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


// StringBuffer:


void ___java_lang_StringBuffer__init___(struct java_lang_StringBuffer *this)
{
    char *content = malloc(1);
    *content = '\0';
    int length = 0;
    *(this) = (struct java_lang_StringBuffer) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuffer" }, length, content };
}

void ___java_lang_StringBuffer__init_String___(struct java_lang_StringBuffer *this, struct java_lang_String *str)
{

    char *content = malloc(str->length + 1);
    strcpy(content, str->data);
    int length = str->length;
    *(this) = (struct java_lang_StringBuffer) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuffer" }, length, content };
}


struct java_lang_StringBuffer *append_java_lang_StringBuffer__C_StringBuffer(struct java_lang_StringBuffer * this, char ch)
{
    int new_length = this->length + 1;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    new_str[this->length] = ch;
    new_str[this->length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuffer_append__C_Ljava_lang_StringBuffer__return_value = this;
    return this;
}


struct java_lang_StringBuffer *append_java_lang_StringBuffer__String_StringBuffer(struct java_lang_StringBuffer *this, struct java_lang_String *str)
{
    int new_length = this->length + str->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, str->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuffer_append__Ljava_lang_String__Ljava_lang_StringBuffer__return_value = this;
    return this;
}


struct java_lang_StringBuffer *append_java_lang_StringBuffer__StringBuffer_StringBuffer(struct java_lang_StringBuffer *this, struct java_lang_StringBuffer *buf)
{
    int new_length = this->length + buf->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, buf->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuffer_append__Ljava_lang_StringBuffer__Ljava_lang_StringBuffer__return_value = this;
    return this;
}


struct java_lang_StringBuffer *appendCodePoint_java_lang_StringBuffer__I_StringBuffer(struct java_lang_StringBuffer * this, int code_point)
{
    char ch;
    if (code_point & 0xff > 255) {
        // we do not support Unicode
        ch = code_point & 0xff;
    } else {
        ch = (char) code_point;
    }
    int new_length = this->length + 1;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    new_str[this->length] = ch;
    new_str[this->length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    java_lang_StringBuffer_appendCodePoint__I_Ljava_lang_StringBuffer__return_value = this;
    return this;
}


char codePointAt_java_lang_StringBuffer__I_I(struct java_lang_StringBuffer *this, int index)
{
    if (index < 0 || index > this->length) {
        java_lang_StringBuffer_codePointAt__I_I_return_value = '\0';
        return '\0';
    }

    java_lang_StringBuffer_codePointAt__I_I_return_value = this->data[index];
    return this->data[index];
}


char codePointBefore_java_lang_StringBuffer__I_I(struct java_lang_StringBuffer *this, int index)
{
    if (index - 1 < 0 || index - 1 > this->length) {
        java_lang_StringBuffer_codePointBefore__I_I_return_value = '\0';
        return '\0';
    }

    java_lang_StringBuffer_codePointBefore__I_I_return_value = this->data[index - 1];
    return this->data[index - 1];
}


int codePointCount_java_lang_StringBuffer__II_I(struct java_lang_StringBuffer *this, int begin, int end)
{
    if (begin < 0 || end > this->length || begin > end) {
        java_lang_StringBuffer_codePointCount__II_I_return_value = '\0';
        return '\0';
    }

    java_lang_StringBuffer_codePointCount__II_I_return_value = end - begin;
    return end - begin;
}


int length_java_lang_StringBuffer___I(struct java_lang_StringBuffer *this)
{
    java_lang_StringBuffer_length___I_return_value = this->length;
    return this->length;
}


struct java_lang_String *substring_java_lang_StringBuffer__I_String(struct java_lang_StringBuffer *this, int begin)
{
    if (begin < 0 || begin > this->length) {
        java_lang_StringBuffer_substring__I_Ljava_lang_String__return_value = NULL;
        return NULL;
    }

    int length = this->length - begin;
    char *content = malloc(length + 1);
    strcpy(content, this->data + begin);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_StringBuffer_substring__I_Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


struct java_lang_String *toString_java_lang_StringBuffer___String(struct java_lang_StringBuffer *this)
{
    char *content = this->data;
    int length = this->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_StringBuffer_toString___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;   
}


// CharSequence:


char charAt_java_lang_CharSequence__I_C(struct java_lang_CharSequence *this, int index)
{
    if (index < 0 || index > this->length) {
        java_lang_CharSequence_charAt__I_C_return_value = '\0';
        return '\0';
    }

    java_lang_CharSequence_charAt__I_C_return_value = this->data[index];
    return this->data[index];
}


int length_java_lang_CharSequence___I(struct java_lang_CharSequence *this)
{
    java_lang_CharSequence_length___I_return_value = this->length;
    return this->length;
}


struct java_lang_String *toString_java_lang_CharSequence___String(struct java_lang_CharSequence *this)
{
    char *content = this->data;
    int length = this->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    java_lang_CharSequence_toString___Ljava_lang_String__return_value = malloc_site;
    return malloc_site;
}


// ========== PRINTF SECTION ==========


struct java_io_PrintStream {
    const char * ___class_identifier___;
};


void println_java_io_PrintStream___V(struct java_io_PrintStream *this) {
    printf("\n");
}


void println_java_io_PrintStream__I_V(struct java_io_PrintStream * this, int output)
{
    printf("%d\n", output);
}


void println_java_io_PrintStream__C_V(struct java_io_PrintStream *this, char output)
{
    printf("%c\n", output);
}


void println_java_io_PrintStream__String_V(struct java_io_PrintStream *this, struct java_lang_String *output)
{
    printf("%s\n", output->data);
}


void println_java_io_PrintStream__D_V(struct java_io_PrintStream *this, double output)
{
    printf("%lf\n", output);
}


void println_java_io_PrintStream__F_V(struct java_io_PrintStream *this, float output)
{
    printf("%f\n", output);
}


void println_java_io_PrintStream__J_V(struct java_io_PrintStream *this, long long output)
{
    printf("%lld\n", output);
}


void println_java_io_PrintStream__Object_V(struct java_io_PrintStream *this, struct java_lang_Object *output)
{
    printf("%s\n", output->___class_identifier___);
}


void println_java_io_PrintStream__Z_V(struct java_io_PrintStream *this, bool output)
{
    printf("%s\n", (output) ? "true": "false");
}