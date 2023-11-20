#include <stdio.h>

#include <stdlib.h>

#include <unistd.h>

#include <signal.h>



int main() {

    pid_t receiver_pid;

    // Получаем PID процесса-получателя

    FILE *file = fopen("receiver.txt", "r");

    if (file == NULL) {

        exit(1);

    }

    int pid;

    if (fscanf(file, "%d", &pid) == 1) {

        receiver_pid = pid;

    } else {

        exit(1);

    }

    fclose(file);

    

    // Отправляем сигнал SIGUSR1 процессу-получателю

    kill(receiver_pid, SIGUSR1);



    printf("Сигнал KILL отправлен процессу-получателю\n");



    return 0;

}