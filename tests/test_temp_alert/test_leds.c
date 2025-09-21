#include <zephyr/ztest.h>
#include "leds.h"

ZTEST(leds_tests, test_leds_init_success)
{
    int ret = leds_init();
    zassert_equal(ret, 0, "leds_init() should return 0 on success, got %d", ret);
}

ZTEST_SUITE(leds_tests, NULL, NULL, NULL, NULL, NULL);
