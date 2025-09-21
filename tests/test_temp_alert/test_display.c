#include <zephyr/ztest.h>
#include "display.h"

ZTEST(display_tests, test_display_init_success)
{
    int ret = display_init();
    zassert_equal(ret, 0, "display_init() should return 0 on success, got %d", ret);
}

/**
 * @tests SRS-02
 */
ZTEST(display_tests, test_display_write_zeroes)
{
    uint8_t zeroes[4] = {0, 0, 0, 0};
    int ret = display_write(zeroes);
    zassert_equal(ret, 0, "display_write() failed with zeroes, got %d", ret);
}

/**
 * @tests SRS-02
 */
ZTEST(display_tests, test_display_write_valid_digits)
{
    extern const uint8_t tm1637_segment_map[16];
    uint8_t digits[4] = {
        tm1637_segment_map[1], /* digit '1' */
        tm1637_segment_map[2], /* digit '2' */
        tm1637_segment_map[3], /* digit '3' */
        tm1637_segment_map[4]  /* digit '4' */
    };
    int ret = display_write(digits);
    zassert_equal(ret, 0, "display_write() failed with valid digits, got %d", ret);
}

// Register suite and generate test_main automatically
ZTEST_SUITE(display_tests, NULL, NULL, NULL, NULL, NULL);
