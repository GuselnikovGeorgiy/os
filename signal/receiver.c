#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

#include <signal.h>





// Обработчик сигнала

void signal_handler(int signo) {

    printf("Процесс-получатель получил сигнал kill\n");

    exit(0);

}



int main() {

    

    pid_t pid = getpid();



    FILE *file = fopen("receiver.txt", "w");

    if (file == NULL) {

        exit(1);

    }

    fprintf(file, "%d", (int)pid);

    fclose(file);



    signal(SIGUSR1, signal_handler);



    printf("Процесс-получатель ждет сигнала kill...\n");



    while(1) {

        printf("Ожидаю сигнала...\n");

        sleep(2);

    }



    return 0;

} 