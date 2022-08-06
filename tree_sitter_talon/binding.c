#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "tree_sitter/parser.h"

extern const TSLanguage *tree_sitter_talon(void);

static PyObject *tree_sitter_talon_id(PyObject *self, PyObject *args)
{
  return PyLong_FromVoidPtr((void *)tree_sitter_talon());
}

static PyMethodDef module_methods[] = {
    {
        .ml_name = "_tree_sitter_talon_id",
        .ml_meth = (PyCFunction)tree_sitter_talon_id,
        .ml_flags = METH_NOARGS,
        .ml_doc = "_tree_sitter_talon_id()\n--\n\n\
               Create an instance of tree_sitter_talon.",
    },
    {NULL},
};

static void module_free(void *self)
{
}

static struct PyModuleDef module_definition = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "binding",
    .m_doc = NULL,
    .m_size = 0,
    .m_free = module_free,
    .m_methods = module_methods,
};

PyMODINIT_FUNC PyInit_binding(void)
{
  PyObject *module = PyModule_Create(&module_definition);
  if (module == NULL)
    return NULL;
  return module;
}
