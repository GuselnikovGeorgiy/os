#include <stdio.h>

#include <pthread.h>

#include <unistd.h>



#define THREAD_COUNT 10

#define MAX_ACTIVE_THREADS 3



int variable = 0;



void* thread_function(void* thread_id) {

    int id = *((int*)thread_id);

    printf("Поток %d начал работу\n", id);



    sleep(3);

    variable += 1;

    

    printf("Поток %d завершил работу, var=%d\n", id, variable);

    pthread_exit(NULL);

}



int main() {

    pthread_t threads[THREAD_COUNT];

    int thread_ids[THREAD_COUNT];



    

    for (int i = 0; i < THREAD_COUNT; i++) {

        thread_ids[i] = i + 1;

        if (pthread_create(&threads[i], NULL, thread_function, &thread_ids[i]) != 0) {

            printf("Ошибка создания потока %d\n", i+1);

            return -1;

        }

    }

    

    for (int i = 0; i < THREAD_COUNT; i++) {

        pthread_join(threads[i], NULL);

    }

    

    return 0;

}