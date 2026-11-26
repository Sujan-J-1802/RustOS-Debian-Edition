#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
int main(void)
{
	pid_t pid=fork();
	if (pid==-1)
	{
		perror("fork");
		exit(1);
	}
	if(pid==0)
	{
		printf("The child process ID is %d\n", getpid());
		exit(0);
	}
	else
	{
		printf("The parent process ID is %d\n", getpid());
		wait(NULL);
	}
	return 0;
}
