#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 1024
int main(int argc, char *argv[])
{
	FILE *fp;
	char line[MAX];
	int count=0;
	if (argc!=3){
		printf("Usage: %s filename word\n", argv[0]);
		return 1;
	}
	fp=fopen(argv[1],"r");
	if (fp==NULL){
		perror("fopen");
		return 1;
	}
	while (fgets(line, sizeof(line), fp)!=NULL){
		count++;
		if (strstr(line, argv[2])!=NULL)
			printf("%s: %d: %s", argv[1], count,line);
	}
	fclose(fp);
	return 0;
}
