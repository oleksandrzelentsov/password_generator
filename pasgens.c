#include <Python.h>
#include "password_lib.h"

static PyObject* generate_password(PyObject* self, PyObject* args)
{
	int n = 8;
	int seed = rand() % 100;
	char* s;
	PyArg_ParseTuple(args, "|ii", &n, &seed);
	s = gen(n, seed);
	PyObject* result = Py_BuildValue("s", s);
	free(s);
	return result;
}

PyMethodDef myMethods[] = {
	{"generate_password",	generate_password,		METH_VARARGS,	"Generates a password from length if given."},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initpasgens(void)
{
	(void) Py_InitModule("pasgens", myMethods);
}
 
