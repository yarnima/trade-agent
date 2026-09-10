from archive.chart import load_data, plot_pattern
from archive.strategy import find_rise_correction


SYMBOLS = [
    "femli",
    "shepna",
    "vakharazm"
]


for symbol in SYMBOLS:

    print()
    print("=" * 50)
    print(symbol)
    print("=" * 50)

    try:

        df = load_data(symbol)

        pattern = find_rise_correction(
            df,
            min_up_moves=3
        )

        if pattern is None:

            print("❌ Pattern not found")

            continue

        print("✅ Pattern found")

        print(
            f"Rise: "
            f"{pattern['rise_low']:.0f}"
            f" → "
            f"{pattern['rise_high']:.0f}"
        )

        print(
            f"Rise: "
            f"{pattern['rise_percent']:.2f}%"
        )

        print(
            f"Correction: "
            f"{pattern['correction_percent']:.2f}%"
        )

        print(
            f"50% level: "
            f"{pattern['fifty_percent']:.0f}"
        )

        print(
            f"Up moves: "
            f"{pattern['up_moves']}"
        )

        plot_pattern(
            symbol,
            pattern
        )

    except FileNotFoundError:

        print(
            f"⚠️ Data file not found: "
            f"data/{symbol}.parquet"
        )