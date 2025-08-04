#ifndef DISPLAY_H_
#define DISPLAY_H_

#include <stdint.h>

/* Initialize the TM1637 pins and clear the display */
int display_init(void);

/* Write exactly 4 segment bytes (bit7 = dot) */
int display_write(const uint8_t segs[4]);

/* Provided by tm1637.c */
extern const uint8_t tm1637_segment_map[16];

#endif /* DISPLAY_H_ */
