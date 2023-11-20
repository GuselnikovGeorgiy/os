#include <stdio.h>

#include <pthread.h>

#include <unistd.h>



pthread_mutex_t mutex;



void print_rectangle(char ch) {

    pthread_mutex_lock(&mutex);

    for (int i = 0; i < 5; ++i) {

        for (int j = 0; j < 10; j++) {

            printf("%c", ch);

            sleep(0.02);

        }

        printf("\n");

    }

    printf("\n");

    pthread_mutex_unlock(&mutex);

}



void *thread_func1(void *arg) { // функция которая будет выполнена в потоке

    print_rectangle('*');

    return NULL; 

} 



void *thread_func2(void *arg) { // функция которая будет выполнена в потоке

    print_rectangle('#');

    return NULL; 

} 



int main() {



    pthread_mutex_init(&mutex, NULL);



    pthread_t child1, child2;

    int child_id1 = 1;

    int child_id2 = 2;



    pthread_create(&child1, NULL, thread_func1, &child_id1);

    pthread_create(&child2, NULL, thread_func2, &child_id2);



    pthread_join(child1, NULL); 

    pthread_join(child2, NULL);



    pthread_mutex_destroy(&mutex);



    return 0;

}