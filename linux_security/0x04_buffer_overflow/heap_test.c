#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*
 * Build: gcc -o heap_test heap_test.c
 * Run:   ./heap_test
 * Then in another terminal:
 *   ./read_write_heap.py $(pidof heap_test) SEEKME123 YOURTEXT
 */

int main(void)
{
	const char *initial = "SEEKME123";
	size_t len = strlen(initial) + 1;
	char *heap_buf = malloc(len);

	if (!heap_buf) {
		perror("malloc");
		return 1;
	}
	memcpy(heap_buf, initial, len);

	printf("heap string address: %p\n", (void *)heap_buf);
	printf("heap string value:   %s\n", heap_buf);
	fflush(stdout);

	while (1) {
		sleep(1);
		printf("heap string value:   %s\n", heap_buf);
		fflush(stdout);
	}

	return 0;
}
