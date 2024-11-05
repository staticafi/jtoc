#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

// ========== STATIC SECTION ==========
struct java_lang_Object * array__byte___clone_return_value = NULL;
struct java_lang_Object * array__char___clone_return_value = NULL;
struct java_lang_Object * array__int___clone_return_value = NULL;
struct java_lang_Object * array__long___clone_return_value = NULL;
struct java_lang_Object * array__float___clone_return_value = NULL;
struct java_lang_Object * array__double___clone_return_value = NULL;
struct java_lang_Object * array__boolean___clone_return_value = NULL;
struct java_lang_Object * array__reference___clone_return_value = NULL;
struct java_lang_Object * array__short___clone_return_value = NULL;
struct java_io_PrintStream * java_lang_System_out = NULL;

int ClassObject_secretNum = 0;
void * ___inflight_exception___ = NULL;
bool java_lang_System__clinit_already_run = false;
bool ClassObject__clinit_already_run = false;


// ========== STRUCTS SECTION ==========
struct java_lang_Object;
struct java_io_Serializable;
struct ClassObject;
struct array__boolean__;
struct array__double__;
struct array__char__;
struct array__int__;
struct array__short__;
struct java_lang_String;
struct array__long__;
struct java_io_PrintStream;
struct java_lang_CharSequence;
struct java_lang_System;
struct java_lang_Class;
struct array__byte__;
struct array__float__;
struct java_lang_Throwable;
struct java_lang_Comparable;
struct array__reference__;


struct java_lang_Object
{
    const char * ___class_identifier___;
};


struct java_io_Serializable
{
    const char * ___class_identifier___;
};


struct ClassObject
{
    struct java_lang_Object ___java_lang_Object___;
    double price;
};


struct array__boolean__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    bool * data;
};


struct array__double__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    double * data;
};


struct array__char__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    unsigned short int * data;
};


struct array__int__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    int * data;
};


struct array__short__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    short int * data;
};


struct java_lang_String
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    unsigned short int * data;
};


struct array__long__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    long long int * data;
};


struct java_io_PrintStream
{
    const char * ___class_identifier___;
};


struct java_lang_CharSequence
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    unsigned short int * data;
};


struct java_lang_System
{
    const char * ___class_identifier___;
};


struct java_lang_Class
{
    const char * ___class_identifier___;
};


struct array__byte__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    signed char * data;
};


struct array__float__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    float * data;
};


struct java_lang_Throwable
{
    const char * ___class_identifier___;
};


struct java_lang_Comparable
{
    const char * ___class_identifier___;
};


struct array__reference__
{
    struct java_lang_Object ___java_lang_Object___;
    int length;
    void * * data;
    const char * ___element_class_identifier___;
    int ___array_dimensions___;
};


// ========== FUNCTIONS SECTION ==========
void ___ClassObject_clinit___();
void ___ClassObject_clinit_wrapper___();
void ___ClassObject_init___(struct ClassObject * this);
void ___Object_init___(struct java_lang_Object * this);
void ___System_clinit___();
void ___System_clinit_wrapper___();


void ___ClassObject_clinit___()
{
    ___ClassObject_clinit_wrapper___();
    ClassObject_secretNum = (int) (10);
}


void ___ClassObject_clinit_wrapper___()
{
    if (! ((ClassObject__clinit_already_run) == (false)))
        goto label1;
    ClassObject__clinit_already_run = true;
    ___ClassObject_clinit___();
label1:
}


void ___ClassObject_init___(struct ClassObject * this)
{
    ___Object_init___(&((*(this)).___java_lang_Object___));
    *(unsigned long long int *)&this->price = 4622100592565682176ull;
}


int main(int agrc, char **argv)
{
    void * local_1a;
    struct ClassObject * new_tmp0;
    ___ClassObject_clinit_wrapper___();
    new_tmp0 = malloc(12);
    *new_tmp0 = (struct ClassObject) { { "java::ClassObject" }, 0 };
    ___ClassObject_init___(new_tmp0);
    local_1a = (void *) (new_tmp0);
    ___System_clinit_wrapper___();
    ___ClassObject_clinit_wrapper___();
    printf("%d\n", ClassObject_secretNum);
    ___System_clinit_wrapper___();
    printf("%f\n", (*((struct ClassObject *) (local_1a))).price);
    return 0;
}


void ___Object_init___(struct java_lang_Object * this)
{
    //to_construct = this;
}


void ___System_clinit___()
{
    struct java_io_PrintStream * malloc_site;
    malloc_site = malloc(4);
    java_lang_System_out = malloc_site;
    *malloc_site = (struct java_io_PrintStream) { "java::java.io.PrintStream" };
}


void ___System_clinit_wrapper___()
{
    if (! ((java_lang_System__clinit_already_run) == (false)))
        goto label1;
    java_lang_System__clinit_already_run = true;
    ___System_clinit___();
label1:
}


