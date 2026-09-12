import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('dark_background')


def plot_position_changes(df_enriched, sc_vsc_laps, session, drivers_to_plot='ALL'):
    fastf1.plotting.setup_mpl()
    fig, ax = plt.subplots(figsize=(14, 7))

    if isinstance(drivers_to_plot, str) and drivers_to_plot.upper() == 'ALL':
        drivers = df_enriched['Driver'].unique()
    elif isinstance(drivers_to_plot, list):
        drivers = drivers_to_plot
    else:
        max_lap = df_enriched['LapNumber'].max()
        final_laps = df_enriched[df_enriched['LapNumber'] == max_lap]
        drivers = final_laps.sort_values('Position')['Driver'].head(5).tolist()

    used_colors = {}

    for driver in drivers:
        driver_data = df_enriched[df_enriched['Driver'] == driver].sort_values('LapNumber')

        if driver_data.empty:
            continue

        try:
            color = f"{fastf1.plotting.get_driver_color(driver, session=session)}"
        except Exception:
            color = '#808080'

        linestyle = '-'
        if color in used_colors:
            linestyle = '--'
        else:
            used_colors[color] = True

        ax.plot(
            driver_data['LapNumber'],
            driver_data['Position'],
            label=driver,
            color=color,
            linestyle=linestyle,
            linewidth=2
        )

    for sc_lap in sc_vsc_laps.get('SC', []):
        ax.axvspan(sc_lap - 0.5, sc_lap + 0.5, color='yellow', alpha=0.2, zorder=0)

    for vsc_lap in sc_vsc_laps.get('VSC', []):
        ax.axvspan(vsc_lap - 0.5, vsc_lap + 0.5, color='orange', alpha=0.15, zorder=0)

    ax.invert_yaxis()
    max_pos = int(df_enriched['Position'].max())
    ax.set_yticks(range(1, max_pos + 1))
    ax.grid(True, linestyle='--', alpha=0.3)

    ncol = 2 if len(drivers) > 10 else 1
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', ncol=ncol)

    plt.tight_layout()
    plt.show()


def plot_delta_to_leader(df_enriched, sc_vsc_laps, session=None, drivers_to_plot='ALL', reference_driver=None):
    fig, ax = plt.subplots(figsize=(14, 7))

    if isinstance(drivers_to_plot, str) and drivers_to_plot.upper() == 'ALL':
        drivers = df_enriched['Driver'].unique().tolist()
    elif isinstance(drivers_to_plot, list):
        drivers = [d.upper() for d in drivers_to_plot]
    else:
        max_lap = df_enriched['LapNumber'].max()
        final_laps = df_enriched[df_enriched['LapNumber'] == max_lap]
        drivers = final_laps.sort_values('Position')['Driver'].head(5).tolist()

    df_plot = df_enriched.copy()

    if reference_driver:
        ref_code = reference_driver.upper()

        if ref_code not in drivers:
            drivers.append(ref_code)

        ref_data = df_plot[df_plot['Driver'] == ref_code][['LapNumber', 'DeltaToLeader']].rename(
            columns={'DeltaToLeader': 'RefDeltaToLeader'}
        )

        df_plot = df_plot.merge(ref_data, on='LapNumber', how='left')
        df_plot['PlotDelta'] = df_plot['DeltaToLeader'] - df_plot['RefDeltaToLeader']
    else:
        df_plot['PlotDelta'] = df_plot['DeltaToLeader']

    used_colors = {}

    for driver in drivers:
        driver_data = df_plot[df_plot['Driver'] == driver].sort_values('LapNumber')

        if driver_data.empty:
            continue

        try:
            color = fastf1.plotting.get_driver_color(driver, session=session)
        except Exception:
            color = '#808080'

        linestyle = '-'
        if color in used_colors:
            linestyle = '--'
        else:
            used_colors[color] = True

        linewidth = 3 if reference_driver and driver == reference_driver.upper() else 2

        ax.plot(
            driver_data['LapNumber'],
            driver_data['PlotDelta'],
            label=driver,
            color=color,
            linestyle=linestyle,
            linewidth=linewidth
        )

    for sc_lap in sc_vsc_laps.get('SC', []):
        ax.axvspan(sc_lap - 0.5, sc_lap + 0.5, color='yellow', alpha=0.2, zorder=0)

    for vsc_lap in sc_vsc_laps.get('VSC', []):
        ax.axvspan(vsc_lap - 0.5, vsc_lap + 0.5, color='orange', alpha=0.15, zorder=0)

    ax.invert_yaxis()
    ax.axhline(0, color='white', linestyle=':', linewidth=1.5, alpha=0.8)
    ax.grid(True, linestyle='--', alpha=0.3)

    ncol = 2 if len(drivers) > 10 else 1
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', ncol=ncol)

    plt.tight_layout()
    plt.show()


def plot_pit_strategy(df_enriched, sc_vsc_laps, session=None, drivers_to_plot='ALL', show_stint_length=False):
    fig, ax = plt.subplots(figsize=(14, 8))

    max_lap = df_enriched['LapNumber'].max()
    final_laps = df_enriched[df_enriched['LapNumber'] == max_lap].sort_values('Position')

    if isinstance(drivers_to_plot, str) and drivers_to_plot.upper() == 'ALL':
        selected_set = set(df_enriched['Driver'].unique())
    elif isinstance(drivers_to_plot, list):
        selected_set = set(d.upper() for d in drivers_to_plot)
    else:
        selected_set = set(final_laps['Driver'].head(5).tolist())

    ordered_drivers = final_laps[final_laps['Driver'].isin(selected_set)]['Driver'].tolist()
    dnf_drivers = [d for d in selected_set if d not in ordered_drivers]
    ordered_drivers.extend(dnf_drivers)

    fallback_colors = {
        'SOFT': '#FF3333',
        'MEDIUM': '#FFF200',
        'HARD': '#EBEBEB',
        'INTERMEDIATE': '#39B54A',
        'WET': '#00AEEF'
    }

    unique_compounds = df_enriched['Compound'].dropna().str.upper().unique()
    compound_colors = {}

    for compound in unique_compounds:
        try:
            color = fastf1.plotting.get_compound_color(compound, session=session)
            compound_colors[compound] = color
        except Exception:
            compound_colors[compound] = fallback_colors.get(compound, '#808080')

    y_positions = range(len(ordered_drivers) - 1, -1, -1)

    for y_idx, driver in zip(y_positions, ordered_drivers):
        driver_laps = df_enriched[df_enriched['Driver'] == driver].sort_values('LapNumber')

        if driver_laps.empty:
            continue

        for stint_num, stint_data in driver_laps.groupby('Stint'):
            start_lap = stint_data['LapNumber'].min()
            end_lap = stint_data['LapNumber'].max()
            compound = str(stint_data['Compound'].iloc[0]).upper()
            color = compound_colors.get(compound, '#808080')

            stint_length = (end_lap - start_lap) + 1
            ax.barh(
                y=y_idx,
                width=stint_length,
                left=start_lap - 0.5,
                height=0.6,
                color=color,
                edgecolor='black',
                linewidth=0.8
            )

            if show_stint_length:
                x_center = (start_lap - 0.5) + (stint_length / 2.0)
                integer_stint = int(stint_length)
                ax.text(
                    x=x_center,
                    y=y_idx,
                    s=f"{integer_stint}",
                    ha='center',
                    va='center',
                    color='black',
                    fontsize=13,
                    fontweight='bold'
                )

    for sc_lap in sc_vsc_laps.get('SC', []):
        ax.axvspan(sc_lap - 0.5, sc_lap + 0.5, color='yellow', alpha=0.15, zorder=0)

    for vsc_lap in sc_vsc_laps.get('VSC', []):
        ax.axvspan(vsc_lap - 0.5, vsc_lap + 0.15, color='orange', alpha=0.1, zorder=0)

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(ordered_drivers, fontsize=11, fontweight='bold')

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=color, label=comp)
        for comp, color in compound_colors.items()
    ]

    ax.legend(handles=legend_handles, bbox_to_anchor=(1.02, 1), loc='upper left')
    ax.set_xlim(0, df_enriched['LapNumber'].max() + 1)
    ax.grid(True, axis='x', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_driver_fuel_adjusted_pace(clean_laps_df, df_enriched, sc_vsc_laps, driver_code, session=None, starting_fuel_kg=110.0, time_penalty_per_kg=0.03, sc_ratio=0.5):
    driver_laps = clean_laps_df[clean_laps_df['Driver'] == driver_code.upper()].copy()

    if driver_laps.empty:
        return

    driver_laps.sort_values('LapNumber', inplace=True)

    total_race_laps = int(df_enriched['LapNumber'].max())
    sc_vsc_set = set(sc_vsc_laps.get('SC', []) + sc_vsc_laps.get('VSC', []))
    num_sc_laps = len(sc_vsc_set)
    num_racing_laps = total_race_laps - num_sc_laps

    fuel_burn_per_race_lap = starting_fuel_kg / (num_racing_laps + (num_sc_laps * sc_ratio))
    fuel_burn_per_saftey_lap = fuel_burn_per_race_lap * sc_ratio

    lap_fuel_dict = {}
    current_fuel = starting_fuel_kg

    for lap in range(1, total_race_laps + 1):
        burn = fuel_burn_per_saftey_lap if lap in sc_vsc_set else fuel_burn_per_race_lap
        current_fuel -= burn
        lap_fuel_dict[lap] = max(0.0, current_fuel)

    driver_laps['RemainingFuel'] = [lap_fuel_dict[lap] for lap in driver_laps['LapNumber']]
    driver_laps['FuelAdjustmentSeconds'] = driver_laps['RemainingFuel'] * time_penalty_per_kg
    driver_laps['FuelAdjustedLapTime'] = driver_laps['LapTimeSeconds'] - driver_laps['FuelAdjustmentSeconds']

    try:
        driver_color = fastf1.plotting.get_driver_color(driver_code, session=session)
    except Exception:
        driver_color = '#00D2BE'

    fig, ax = plt.subplots(figsize=(12, 6))

    full_driver_data = df_enriched[df_enriched['Driver'] == driver_code.upper()]
    pit_laps = full_driver_data[full_driver_data['PitInTime'].notna()]['LapNumber']

    for i, pit_lap in enumerate(pit_laps):
        ax.axvline(x=pit_lap, color='white', linestyle=':', linewidth=1.2, alpha=0.7)

    ax.scatter(
        driver_laps['LapNumber'],
        driver_laps['LapTimeSeconds'],
        color=driver_color,
        alpha=0.3,
        s=50,
        edgecolors='none'
    )

    ax.scatter(
        driver_laps['LapNumber'],
        driver_laps['FuelAdjustedLapTime'],
        color=driver_color,
        alpha=1.0,
        s=60,
        edgecolors='white',
        linewidth=0.8
    )

    for stint_id, stint_data in driver_laps.groupby('Stint'):
        if len(stint_data) > 1:
            z = np.polyfit(stint_data['LapNumber'], stint_data['FuelAdjustedLapTime'], 1)
            p = np.poly1d(z)
            ax.plot(
                stint_data['LapNumber'],
                p(stint_data['LapNumber']),
                color='white',
                linestyle='--',
                alpha=0.8,
                linewidth=1.5
            )

    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(loc='upper right', frameon=True)

    plt.tight_layout()
    plt.show()


def plot_driver_lap_boxplot(df_laps, drivers, duration=None, session=None):
    if not isinstance(drivers, list) or len(drivers) == 0:
        return

    drivers = [d.upper() for d in drivers]

    data_to_plot = []
    plot_labels = []
    box_colors = []

    if duration is None:
        for driver in drivers:
            d_laps = df_laps[df_laps['Driver'] == driver]['LapTimeSeconds'].dropna()
            if not d_laps.empty:
                data_to_plot.append(d_laps.values)
                plot_labels.append(driver)

                try:
                    color = fastf1.plotting.get_driver_color(driver, session=session)
                except Exception:
                    color = '#00D2BE'
                box_colors.append(color)

    elif isinstance(duration, tuple) and len(duration) == 2:
        start_lap, end_lap = duration
        for driver in drivers:
            d_laps = df_laps[
                (df_laps['Driver'] == driver) &
                (df_laps['LapNumber'] >= start_lap) &
                (df_laps['LapNumber'] <= end_lap)
            ]['LapTimeSeconds'].dropna()

            if not d_laps.empty:
                data_to_plot.append(d_laps.values)
                plot_labels.append(f"{driver}\n({start_lap}-{end_lap})")

                try:
                    color = fastf1.plotting.get_driver_color(driver, session=session)
                except Exception:
                    color = '#00D2BE'
                box_colors.append(color)

    elif isinstance(duration, list):
        for idx, driver in enumerate(drivers):
            stint_num = duration[idx] if idx < len(duration) else 1
            d_laps = df_laps[
                (df_laps['Driver'] == driver) &
                (df_laps['Stint'] == stint_num)
            ]['LapTimeSeconds'].dropna()

            if not d_laps.empty:
                data_to_plot.append(d_laps.values)
                plot_labels.append(f"{driver}\n(S{stint_num})")

                try:
                    color = fastf1.plotting.get_driver_color(driver, session=session)
                except Exception:
                    color = '#00D2BE'
                box_colors.append(color)

    if not data_to_plot:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    flierprops = dict(marker='x', color='white', markeredgecolor='white', markersize=7)

    bplot = ax.boxplot(
        data_to_plot,
        patch_artist=True,
        label=plot_labels,
        flierprops=flierprops,
        medianprops=dict(color='white', linewidth=2),
        boxprops=dict(linewidth=1.2),
        whiskerprops=dict(color='white', linewidth=1.2),
        capprops=dict(color='white', linewidth=1.2)
    )

    ax.set_xticklabels(plot_labels, fontsize=11, fontweight='bold')

    for patch, color in zip(bplot['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.grid(True, axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()
