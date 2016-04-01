#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>
#include <string.h>

char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%%^&*()_-+={}:;\"\'\\/?|<>";

void change(char* a, char* b)
{
	char c = *b;
	*b = *a;
	*a = c;
}

char get_next_password_symbol(void)
{
	return alphabet[rand() % strlen(alphabet)];
}

char* gen(int length, int seed)
{
	char* result = calloc(length + 1, sizeof(char));
	int lng = 0, i;
	srand((unsigned int) time(NULL) + length * seed);
	while(lng < length)
	{
		result[lng++] = get_next_password_symbol();
	}
	for(i = 0; result[i] != '\0'; i++)
	{
		change(result + i, result + rand() % length);
		result[i] = get_next_password_symbol();
	}
	result[length] = '\0';
	return result;
}
