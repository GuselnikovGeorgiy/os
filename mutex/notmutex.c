#include <stdio.h>

#include <unistd.h>

#include <pthread.h>



void print_rectangle(char ch) {

    for (int i = 0; i < 5; ++i) {

        for (int j = 0; j < 10; j++) {

            printf("%c", ch);

            sleep(0.02);

        }

        printf("\n");

    }

    printf("\n");

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

    pthread_t child1, child2;

    int child_id1 = 1;

    int child_id2 = 2;



    pthread_create(&child1, NULL, thread_func1, &child_id1);

    pthread_create(&child2, NULL, thread_func2, &child_id2);



    pthread_join(child1, NULL); 

    pthread_join(child2, NULL);



    return 0;

}