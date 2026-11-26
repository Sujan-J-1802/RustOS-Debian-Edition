#include <stdio.h>
#include <stdlib.h>
int main(int argc,char *argv[])
{
	FILE *src, *dest;
	int ch;
	if (argc != 3){
		printf("Usage: %s source destination\n", argv[0]);
		return  1;
	}
	src=fopen(argv[1], "r");
	if (src == NULL){
		perror("Source file");
		return 1;
	}
	dest=fopen(argv[2],"w");
	if (dest == NULL){
		perror("Destination file");
		fclose(src);
		return 1;
	}
	while ((ch = fgetc(src)) != EOF)
		fputc(ch,dest);
		return 1;
	fclose(src);
	fclose(dest);
	printf("File copied successfully.\n");
}
