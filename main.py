from data_load_clean import load_session, preprocess_race_laps
from plotting import (
    plot_position_changes,
    plot_delta_to_leader,
    plot_pit_strategy,
    plot_driver_fuel_adjusted_pace,
    plot_driver_lap_boxplot
)


def main():
    session, laps_df, results_df = load_session(2025, 'Qatar')
    df_enriched, clean_laps, SC_VSC_laps = preprocess_race_laps(laps_df)

    plot_position_changes(df_enriched, SC_VSC_laps, session, 'ALL')
    plot_delta_to_leader(df_enriched, SC_VSC_laps, session, 'ALL', 'VER')
    plot_pit_strategy(df_enriched, SC_VSC_laps, session, ['VER', 'NOR', 'PIA'], True)
    plot_driver_fuel_adjusted_pace(clean_laps, df_enriched, SC_VSC_laps, 'VER', session)
    plot_driver_fuel_adjusted_pace(clean_laps, df_enriched, SC_VSC_laps, 'ANT', session)
    plot_driver_fuel_adjusted_pace(clean_laps, df_enriched, SC_VSC_laps, 'PIA', session)
    plot_driver_lap_boxplot(clean_laps, ['VER', 'SAI', 'ANT', 'NOR', 'PIA'], (10, 25), session)


if __name__ == '__main__':
    main()
