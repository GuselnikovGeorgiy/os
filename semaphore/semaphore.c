#include <stdio.h>

#include <pthread.h>

#include <semaphore.h>

#include <unistd.h>



#define THREAD_COUNT 10

#define MAX_ACTIVE_THREADS 3



int variable = 0;



sem_t semaphore;



void* thread_function(void* thread_id) {

    int id = *((int*)thread_id);

    printf("Поток %d начал работу\n", id);



    sleep(3);

    variable += 1;



    printf("Поток %d завершил работу, var=%d\n", id, variable);

    sem_post(&semaphore); // Увеличиваем семафор после завершения работы потока

    pthread_exit(NULL);

}



int main() {

    pthread_t threads[THREAD_COUNT];

    int thread_ids[THREAD_COUNT];

    

    sem_init(&semaphore, 0, MAX_ACTIVE_THREADS); // Инициализация семафора

    sem_post(&semaphore);

    for (int i = 0; i < THREAD_COUNT; i++) {

        thread_ids[i] = i + 1;

        if (pthread_create(&threads[i], NULL, thread_function, &thread_ids[i]) != 0) {

            printf("Ошибка создания потока %d\n", i+1);

            return -1;

        }

        sem_wait(&semaphore); // Ожидаем доступные слоты семафора

    }

    

    for (int i = 0; i < THREAD_COUNT; i++) {

        pthread_join(threads[i], NULL);

    }

    

    sem_destroy(&semaphore); // Уничтожаем семафор

    

    return 0;

}