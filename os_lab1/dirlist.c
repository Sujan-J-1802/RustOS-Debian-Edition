
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>

int main() {
    char dirname[100];
    struct dirent *entry;
    struct stat info;
    DIR *dir;

    printf("Enter directory name to search: ");
    scanf("%99s", dirname);

    dir = opendir(".");

    if (dir == NULL) {
        perror("Cannot open directory");
        return 1;
    }

    int found = 0;

    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, dirname) == 0) {
            if (stat(entry->d_name, &info) == 0 &&
                S_ISDIR(info.st_mode)) {
                printf("Directory found: %s\n", entry->d_name);
                found = 1;
                break;
            }
        }
    }

    if (!found) {
        printf("Directory not found.\n");
    }

    closedir(dir);
    return 0;
}
