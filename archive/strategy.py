import pandas as pd


def find_rise_correction(
    df,
    min_up_moves=3,
    max_lookback=100
):
    """
    Find the latest pattern:

    1. At least 3 consecutive increases in closing price.
    2. Then a correction starts.
    3. Correction must not reach 50% of the previous rise.

    Definition of an up move:
        close[i] > close[i-1]
    """

    df = df.sort_values("date").reset_index(drop=True).copy()

    if len(df) < min_up_moves + 2:
        return None

    # فقط بخش اخیر بازار
    start_index = max(1, len(df) - max_lookback)

    # از آخر به اول دنبال اصلاح اخیر می‌گردیم
    for correction_end in range(len(df) - 1, start_index, -1):

        # --------------------------------------------------
        # مرحله 1:
        # آخرین کندل باید بخشی از اصلاح باشد.
        # یعنی قیمت فعلی کمتر از سقف اخیر باشد.
        # --------------------------------------------------

        correction_low = df.loc[
            correction_end, "close"
        ]

        # از این نقطه به عقب می‌رویم و موج صعود را پیدا می‌کنیم
        for rise_high_idx in range(
            correction_end - 1,
            start_index - 1,
            -1
        ):

            rise_high = df.loc[
                rise_high_idx, "close"
            ]

            # سقف باید بالاتر از قیمت اصلاح باشد
            if correction_low >= rise_high:
                continue

            # --------------------------------------------------
            # پیدا کردن شروع موج صعود
            # --------------------------------------------------

            rise_start_idx = rise_high_idx

            consecutive_up_moves = 0

            while rise_start_idx > start_index:

                current_close = df.loc[
                    rise_start_idx, "close"
                ]

                previous_close = df.loc[
                    rise_start_idx - 1, "close"
                ]

                if current_close > previous_close:

                    consecutive_up_moves += 1
                    rise_start_idx -= 1

                else:
                    break

            # حداقل 3 افزایش متوالی
            if consecutive_up_moves < min_up_moves:
                continue

            rise_low_idx = rise_start_idx

            rise_low = df.loc[
                rise_low_idx, "close"
            ]

            # --------------------------------------------------
            # 50% Fibonacci retracement
            # --------------------------------------------------

            rise_range = rise_high - rise_low

            if rise_range <= 0:
                continue

            fifty_percent = (
                rise_low +
                0.5 * rise_range
            )

            # اصلاح نباید به 50% برسد
            if correction_low <= fifty_percent:
                continue

            # --------------------------------------------------
            # Pattern found
            # --------------------------------------------------

            return {
                "rise_start_idx": rise_low_idx,
                "rise_high_idx": rise_high_idx,
                "correction_end_idx": correction_end,

                "rise_low": rise_low,
                "rise_high": rise_high,
                "correction_low": correction_low,

                "fifty_percent": fifty_percent,

                "up_moves": consecutive_up_moves,

                "rise_percent": (
                    (rise_high - rise_low)
                    / rise_low
                    * 100
                ),

                "correction_percent": (
                    (rise_high - correction_low)
                    / (rise_high - rise_low)
                    * 100
                )
            }

    return None