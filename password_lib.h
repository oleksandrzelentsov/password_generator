#include "stdio.h"
#include "stdlib.h"
#include "ctype.h"
#include "time.h"

const int ispasschar(const char c)
{
	return ((c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == ' ');
}

int isnum(char* s)
{
	char *i = s;
	while (*(i++) != '\0')
	{
		if(!isdigit(*i))
			return 0;
	}
	return 1;
}

void change(char* a, char* b)
{
	char c = *b;
	*b = *a;
	*a = c;
}

char get_next_password_symbol(void)
{
	char c;
	while(!ispasschar(c = rand() % 256));
	return c;
}

int enc(char* s, int seed)
{
	int i;
	for(i = 0; s[i] != '\0'; i++) 
	{
		change(s + i,s + rand() % strlen(s));
		s[i] = get_next_password_symbol();
		change(s + i,s + rand() % strlen(s));
		s[i] = get_next_password_symbol();
		change(s + i,s + rand() % strlen(s));
		if(rand() % 2 - 1)
		{
			s[i] = rand()%10+'0';
		}
		if(rand()%4 == 3)
		{
			s[i] = get_next_password_symbol();
		}
	}
	return 0;
}

char* gen(int length, int seed)
{
	char* result = (char*) calloc(length, sizeof(char));
	int lng = 0;
	srand((unsigned int)time(NULL) + length * seed);
	while(lng < ((length == 0) ? 8 : length))
	{
		char c;
		if(ispasschar(c = rand() % 256))
			result[lng++] = c;
	}
	enc(result, seed);
	return result;
}
