from data_load_clean import load_session, preprocess_race_laps
from plotting import (
    plot_position_changes,
    plot_delta_to_leader,
    plot_pit_strategy,
    plot_driver_fuel_adjusted_pace,
    plot_driver_lap_boxplot
)


def main():
    year_input = input("Enter Year (e.g., 2023): ").strip()
    year = int(year_input)

    grand_prix = input("Enter Grand Prix name or country (e.g., Qatar, Monza, SilverStone): ").strip()

    drivers_input = input("Enter driver codes separated by commas (e.g., VER, NOR, PIA) or press Enter for ALL: ").strip()
    if drivers_input:
        drivers = [d.strip().upper() for d in drivers_input.split(',')]
    else:
        drivers = 'ALL'

    ref_driver_input = input("Enter reference driver code for Delta plot (e.g., VER) or press Enter for default leader: ").strip()
    reference_driver = ref_driver_input.upper() if ref_driver_input else None

    session, laps_df, results_df = load_session(year, grand_prix)
    df_enriched, clean_laps, SC_VSC_laps = preprocess_race_laps(laps_df)

    plot_position_changes(df_enriched, SC_VSC_laps, session, drivers)
    plot_delta_to_leader(df_enriched, SC_VSC_laps, session, drivers, reference_driver)
    plot_pit_strategy(df_enriched, SC_VSC_laps, session, drivers, show_stint_length=True)
    
    if isinstance(drivers, list):
        for driver in drivers:
            plot_driver_fuel_adjusted_pace(clean_laps, df_enriched, SC_VSC_laps, driver, session)

        plot_driver_lap_boxplot(clean_laps, drivers, session=session)


if __name__ == '__main__':
    main()
