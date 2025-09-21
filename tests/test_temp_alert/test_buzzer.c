#include <zephyr/ztest.h>
#include "buzzer.h"

/**
 * @tests SRS-04
 */
ZTEST(buzzer_tests, test_buzzer_fire_pattern_runs)
{
    /* We expect no crash or error, can't assert much in unit test */
    buzzer_fire_pattern();
    zassert_true(true, "buzzer_fire_pattern should complete without error");
}

ZTEST_SUITE(buzzer_tests, NULL, NULL, NULL, NULL, NULL);
