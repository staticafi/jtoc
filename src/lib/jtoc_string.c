#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>


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
    struct java_lang_Object ___java_lang_Object___;
    int length;
    char* data;
};



void ___String_init___(struct java_lang_String *this)
{
    char *content = malloc(1);
    *content = '\0';
    *(this) = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, 0, content };
}


int compareTo_String_String_I(struct java_lang_String *this, struct java_lang_String *other)
{
    return strcmp(this->data, other->data);
}


struct java_lang_String *concat_String_String_String(struct java_lang_String *this, struct java_lang_String *other)
{
    char *dest = malloc(this->length + other->length + 1);
    char *copy = strcpy(dest, this->data);
    char *content = strcat(copy, other->data);

    int length = this->length + other->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;
}


bool contains_String_CharSequence_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq) 
{
    return strstr(this->data, seq->data) != NULL;
}


bool endsWith_String_String_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq) 
{
    if (this->length < seq->length) {
        return false;
    }

    return strcmp(this->data + this->length - seq->length, seq->data) == 0;
}


struct java_lang_String *toLowerCase_String__String(struct java_lang_String *this)
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
    return malloc_site;
}


struct java_lang_String *toUpperCase_String__String(struct java_lang_String *this)
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
    return malloc_site;
}


bool equalsIgnoreCase_String_String_Z(struct java_lang_String *this, struct java_lang_CharSequence *other)
{
    struct java_lang_String *lowered_this = toLowerCase(this);
    struct java_lang_String *lowered_other = toLowerCase(other);

    return strcmp(lowered_this->data, lowered_other->data) == 0;
}


int indexOf_String_I_I(struct java_lang_String *this, int ch)
{    
    char substr[2] = {ch, '\0'};
    char *pos = strstr(this->data, substr);
    if (pos == NULL) {
        return -1;
    }

    return this->data - pos;
}


int indexOf_String_II_I(struct java_lang_String *this, int ch, int start_from)
{    
    if (start_from > this->length) {
        return -1;
    }

    char substr[2] = {ch, '\0'};
    char *pos = strstr(this->data + start_from, substr);
    if (pos == NULL) {
        return -1;
    }

    return this->data - pos;
}


int indexOf_String_String_I(struct java_lang_String *this, struct java_lang_String *other)
{
    char *pos = strstr(this->data, other->data);
    if (pos == NULL) {
        return -1;
    }

    return this->data - pos;
}


int indexOf_String_StringI_I(struct java_lang_String *this, struct java_lang_String *other, int start_from)
{
    if (start_from > this->length) {
        return -1;
    }

    char *pos = strstr(this->data + start_from, other->data);
    if (pos == NULL) {
        return -1;
    }

    return this->data - pos;
}


bool isEmpty_String__Z(struct java_lang_String *this)
{
    return strlen(this->data) == 0;
}


int lastIndexOf_String_I_I(struct java_lang_String *this, int ch)
{
    char substr[2] = {ch, '\0'};
    char *last;
    char *pos = this->data;
    do {
        last = pos;
        pos = strstr(pos, substr);
    } while (pos != NULL);

    if (last == NULL) {
        return -1;
    }

    return this->data - last;
}


int lastIndexOf_String_II_I(struct java_lang_String *this, int ch, int end_at)
{
    if (end_at > this->length) {
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
    
    if (last == NULL) {
        return -1;
    }

    return this->data - last;
}


int lastIndexOf_String_String_I(struct java_lang_String *this, struct java_lang_String *other)
{
    char *last;
    char *pos = this->data;
    do {
        last = pos;
        pos = strstr(pos, other->data);
    } while (pos != NULL);

    if (last == NULL) {
        return -1;
    }

    return this->data - last;
}


int lastIndexOf_String_StringI_I(struct java_lang_String *this, struct java_lang_String *other, int end_at)
{
    if (end_at > this->length) {
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
    
    if (last == NULL) {
        return -1;
    }

    return this->data - last;
}


int length_String__I(struct java_lang_String *this)
{
    return this->length;
}


struct java_lang_String *replace_String_CC_String(struct java_lang_String *this, char old, char new)
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
    return malloc_site;
}


struct java_lang_String *replace_String_CharSequenceCharSequence_String(struct java_lang_String *this, struct java_lang_CharSequence *old, struct java_lang_CharSequence *new)
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
    return malloc_site;
}


bool startsWith_String_String_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq) 
{
    if (this->length < seq->length) {
        return false;
    }

    char replaced_letter = this->data[seq->length];
    this->data[seq->length] = '\0';

    bool result = strcmp(this->data, seq->data) == 0;

    this->data[seq->length] = replaced_letter;

    return result;
}


bool startsWith_String_StringI_Z(struct java_lang_String *this, struct java_lang_CharSequence *seq, int offset) 
{
    if (this->length - offset < seq->length) {
        return false;
    }

    char replaced_letter = this->data[seq->length + offset];
    this->data[seq->length + offset] = '\0';

    bool result = strcmp(this->data + offset, seq->data) == 0;

    this->data[seq->length + offset] = replaced_letter;

    return result;
}


struct java_lang_String *toString_String__String(struct java_lang_String *this)
{
    return this;
}


struct java_lang_String *trim_String__String(struct java_lang_String *this)
{
    int start = 0;
    int end = this->length;

    while (this->data[start] == ' ') {
        start++;
    }

    while (this->data[end] == ' ') {
        end--;
    }

    int length = end - start;
    char *content = malloc(length + 1); 
    strcpy(content, this->data);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;
}


// StringBuilder:


void ___StringBuilder_init___(struct java_lang_StringBuilder *this)
{
    char *content = malloc(1);
    *content = '\0';
    int length = 0;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}

void ___StringBuilder_init_I___(struct java_lang_StringBuilder *this, int capacity)
{
    // capacity arg is not used
    char *content = malloc(1);
    *content = '\0';
    int length = 0;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}

void ___StringBuilder_init_String___(struct java_lang_StringBuilder *this, struct java_lang_String *str)
{

    char *content = malloc(str->length + 1);
    strcpy(content, str->data);
    int length = str->length;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}


void ___StringBuilder_init_CharSequence___(struct java_lang_StringBuilder *this, struct java_lang_CharSequence *seq)
{
    char *content = malloc(seq->length + 1);
    strcpy(content, seq->data);
    int length = seq->length;
    *(this) = (struct java_lang_StringBuilder) { (struct java_lang_AbstractStringBuilder) { "java::java.lang.StringBuilder" }, length, content };
}


struct java_lang_StringBuilder *append_StringBuilder_C_StringBuilder(struct java_lang_StringBuilder * this, char ch)
{
    int new_length = this->length + 1;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    new_str[this->length] = ch;
    new_str[this->length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuilder *append_StringBuilder_String_StringBuilder(struct java_lang_StringBuilder *this, struct java_lang_String *str)
{
    int new_length = this->length + str->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, str->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuilder *append_StringBuilder_CharSequence_StringBuilder(struct java_lang_StringBuilder *this, struct java_lang_CharSequence *seq)
{
    int new_length = this->length + seq->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, seq->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuilder *append_StringBuilder_StringBuffer_StringBuilder(struct java_lang_StringBuilder *this, struct java_lang_StringBuffer *buf)
{
    int new_length = this->length + buf->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, buf->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuilder *appendCodePoint_StringBuilder_I_StringBuilder(struct java_lang_StringBuilder * this, int code_point)
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
    return this;
}


char charAt_StringBuilder_I_C(struct java_lang_StringBuilder *this, int index)
{
    if (index < 0 || index > this->length) {
        return '\0';
    }

    return this->data[index];
}


char codePointAt_StringBuilder_I_I(struct java_lang_StringBuilder *this, int index)
{
    if (index < 0 || index > this->length) {
        return '\0';
    }

    return this->data[index];
}


char codePointBefore_StringBuilder_I_I(struct java_lang_StringBuilder *this, int index)
{
    if (index - 1 < 0 || index - 1 > this->length) {
        return '\0';
    }

    return this->data[index - 1];
}


int codePointCount_StringBuilder_II_I(struct java_lang_StringBuilder *this, int begin, int end)
{
    if (begin < 0 || end > this->length || begin > end) {
        return '\0';
    }

    return end - begin;
}


int length_StringBuilder__I(struct java_lang_StringBuilder *this)
{
    return this->length;
}


struct java_lang_String *substring_StringBuilder_I_String(struct java_lang_StringBuilder *this, int begin)
{
    if (begin < 0 || begin > this->length) {
        return NULL;
    }

    int length = this->length - begin;
    char *content = malloc(length + 1);
    strcpy(content, this->data + begin);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;
}


struct java_lang_String *substring_StringBuilder_II_String(struct java_lang_StringBuilder *this, int begin, int end)
{
    if (begin < 0 || begin > this->length || end < 0 || end > this->length || begin > end) {
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
    return malloc_site;
}


struct java_lang_String *toString_StringBuilder__String(struct java_lang_StringBuilder *this)
{
    char *content = this->data;
    int length = this->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;
    
}


// StringBuffer:


void ___StringBuffer_init___(struct java_lang_StringBuffer *this)
{
    char *content = malloc(1);
    *content = '\0';
    int length = 0;
    *(this) = (struct java_lang_StringBuffer) { (struct java_lang_Object) { "java::java.lang.StringBuffer" }, length, content };
}

void ___StringBuffer_init_String___(struct java_lang_StringBuffer *this, struct java_lang_String *str)
{

    char *content = malloc(str->length + 1);
    strcpy(content, str->data);
    int length = str->length;
    *(this) = (struct java_lang_StringBuffer) { (struct java_lang_Object) { "java::java.lang.StringBuffer" }, length, content };
}


struct java_lang_StringBuffer *append_StringBuffer_C_StringBuffer(struct java_lang_StringBuffer * this, char ch)
{
    int new_length = this->length + 1;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    new_str[this->length] = ch;
    new_str[this->length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuffer *append_StringBuffer_String_StringBuffer(struct java_lang_StringBuffer *this, struct java_lang_String *str)
{
    int new_length = this->length + str->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, str->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuffer *append_StringBuffer_StringBuffer_StringBuffer(struct java_lang_StringBuffer *this, struct java_lang_StringBuffer *buf)
{
    int new_length = this->length + buf->length;

    char *new_str = malloc(new_length + 1);
    strcpy(new_str, this->data);
    strcat(new_str + this->length, buf->data);
    new_str[new_length + 1] = '\0';

    free(this->data);
    this->data = new_str;
    this->length = new_length;
    return this;
}


struct java_lang_StringBuffer *appendCodePoint_StringBuffer_I_StringBuffer(struct java_lang_StringBuffer * this, int code_point)
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
    return this;
}


char codePointAt_StringBuffer_I_I(struct java_lang_StringBuffer *this, int index)
{
    if (index < 0 || index > this->length) {
        return '\0';
    }

    return this->data[index];
}


char codePointBefore_StringBuffer_I_I(struct java_lang_StringBuffer *this, int index)
{
    if (index - 1 < 0 || index - 1 > this->length) {
        return '\0';
    }

    return this->data[index - 1];
}


int codePointCount_StringBuffer_II_I(struct java_lang_StringBuffer *this, int begin, int end)
{
    if (begin < 0 || end > this->length || begin > end) {
        return '\0';
    }

    return end - begin;
}


int length_StringBuffer__I(struct java_lang_StringBuffer *this)
{
    return this->length;
}


struct java_lang_String *substring_StringBuffer_I_String(struct java_lang_StringBuffer *this, int begin)
{
    if (begin < 0 || begin > this->length) {
        return NULL;
    }

    int length = this->length - begin;
    char *content = malloc(length + 1);
    strcpy(content, this->data + begin);

    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;
}


struct java_lang_String *toString_StringBuffer__String(struct java_lang_StringBuffer *this)
{
    char *content = this->data;
    int length = this->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;   
}


// CharSequence:


char charAt_CharSequence_I_C(struct java_lang_CharSequence *this, int index)
{
    if (index < 0 || index > this->length) {
        return '\0';
    }

    return this->data[index];
}


int length_CharSequence__I(struct java_lang_CharSequence *this)
{
    return this->length;
}


struct java_lang_String *toString_CharSequence__String(struct java_lang_CharSequence *this)
{
    char *content = this->data;
    int length = this->length;
    struct java_lang_String * malloc_site;
    malloc_site = malloc(16);
    *malloc_site = (struct java_lang_String) { (struct java_lang_Object) { "java::java.lang.String" }, length, content };
    return malloc_site;   
}


/*
// java::java.lang.String.<init>:()V
// java::java.lang.String.compareTo:(Ljava/lang/String;)I
// java::java.lang.String.concat:(Ljava/lang/String;)Ljava/lang/String;
// java::java.lang.String.contains:(Ljava/lang/CharSequence;)Z
// java::java.lang.String.endsWith:(Ljava/lang/String;)Z
// java::java.lang.String.equalsIgnoreCase:(Ljava/lang/String;)Z
// java::java.lang.String.indexOf:(I)I
// java::java.lang.String.indexOf:(II)I
// java::java.lang.String.indexOf:(Ljava/lang/String;)I
// java::java.lang.String.indexOf:(Ljava/lang/String;I)I
// java::java.lang.String.isEmpty:()Z
// java::java.lang.String.lastIndexOf:(I)I
// java::java.lang.String.lastIndexOf:(II)I
// java::java.lang.String.lastIndexOf:(Ljava/lang/String;)I
// java::java.lang.String.lastIndexOf:(Ljava/lang/String;I)I
// java::java.lang.String.length:()I
// java::java.lang.String.replace:(CC)Ljava/lang/String;
// java::java.lang.String.replace:(Ljava/lang/CharSequence;Ljava/lang/CharSequence;)Ljava/lang/String;
// java::java.lang.String.startsWith:(Ljava/lang/String;)Z
// java::java.lang.String.startsWith:(Ljava/lang/String;I)Z
// java::java.lang.String.toLowerCase:()Ljava/lang/String;
// java::java.lang.String.toString:()Ljava/lang/String;
// java::java.lang.String.toUpperCase:()Ljava/lang/String;
// java::java.lang.String.trim:()Ljava/lang/String;
// java::java.lang.StringBuilder.<init>:(Ljava/lang/String;)V
// java::java.lang.StringBuilder.<init>:(Ljava/lang/CharSequence;)V
// java::java.lang.StringBuilder.<init>:()V
// java::java.lang.StringBuilder.<init>:(I)V
// java::java.lang.StringBuilder.append:(C)Ljava/lang/StringBuilder;
// java::java.lang.StringBuilder.append:(Ljava/lang/CharSequence;)Ljava/lang/StringBuilder;
// java::java.lang.StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
// java::java.lang.StringBuilder.append:(Ljava/lang/StringBuffer;)Ljava/lang/StringBuilder;
// java::java.lang.StringBuilder.appendCodePoint:(I)Ljava/lang/StringBuilder;
// java::java.lang.StringBuilder.charAt:(I)C
// java::java.lang.StringBuilder.codePointAt:(I)I
// java::java.lang.StringBuilder.codePointBefore:(I)I
// java::java.lang.StringBuilder.codePointCount:(II)I
// java::java.lang.StringBuilder.length:()I
// java::java.lang.StringBuilder.substring:(II)Ljava/lang/String;
// java::java.lang.StringBuilder.substring:(I)Ljava/lang/String;
// java::java.lang.StringBuilder.toString:()Ljava/lang/String;
// java::java.lang.StringBuffer.<init>:(Ljava/lang/String;)V
// java::java.lang.StringBuffer.<init>:()V
// java::java.lang.StringBuffer.append:(C)Ljava/lang/StringBuffer;
// java::java.lang.StringBuffer.append:(Ljava/lang/String;)Ljava/lang/StringBuffer;
// java::java.lang.StringBuffer.append:(Ljava/lang/StringBuffer;)Ljava/lang/StringBuffer;
// java::java.lang.StringBuffer.appendCodePoint:(I)Ljava/lang/StringBuffer;
// java::java.lang.StringBuffer.codePointAt:(I)I
// java::java.lang.StringBuffer.codePointBefore:(I)I
// java::java.lang.StringBuffer.codePointCount:(II)I
// java::java.lang.StringBuffer.length:()I
// java::java.lang.StringBuffer.substring:(I)Ljava/lang/String;
// java::java.lang.StringBuffer.toString:()Ljava/lang/String;
// java::java.lang.CharSequence.charAt:(I)C
// java::java.lang.CharSequence.toString:()Ljava/lang/String;
// java::java.lang.CharSequence.length:()I
*/