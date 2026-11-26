cat << 'EOF' > list_dir.c
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
int main(int argc,char *argv[])
{
	char buff[100];
	DIR *dirp;
	strict dirent *dptr;
	printf("Enter Directory Name: ");
	if (scanf("%99s",buff)!=1)
	{
		fprintf(stderr,"Failed to read input\n");
		return 1;
	}
	if ((dirp=opendir(buff))==NULL)
	{
		perror("Error opening directory");
		exit(EXIT_FAILURE);
	}
	while ((DPtr=readdir(dirp))!=NULL)
	{
		printf("%s\n",dptr->d_name);
	}
	closedir(dirp);
	return 0;
}
EOF
