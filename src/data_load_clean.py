import fastf1
import pandas as pd


def load_session(year: int, grand_prix: str):
    session = fastf1.get_session(year, grand_prix, 'R')
    session.load(telemetry=False, weather=False)
    laps_df = session.laps.copy()
    results_df = session.results.copy()
    return session, laps_df, results_df


def preprocess_race_laps(laps_df: pd.DataFrame):
    df = laps_df.copy()

    df['LapTimeSeconds'] = df['LapTime'].dt.total_seconds()

    race_start_time = df['LapStartTime'].min()
    df['RaceTimeSeconds'] = (df['Time'] - race_start_time).dt.total_seconds()

    leader_laps = df[df['Position'] == 1.0][['LapNumber', 'Time']].copy()
    leader_laps.rename(columns={'Time': 'LeaderTime'}, inplace=True)

    df = df.merge(leader_laps, on='LapNumber', how='left')
    df['DeltaToLeader'] = (df['Time'] - df['LeaderTime']).dt.total_seconds()

    leader_laps = df[df['Position'] == 1.0].sort_values('LapNumber')
    safety_car_laps = []
    vsc_laps = []

    for _, row in leader_laps.iterrows():
        status = str(row['TrackStatus'])
        lap_num = int(row['LapNumber'])

        if '4' in status:
            safety_car_laps.append(lap_num)
        elif '6' in status:
            vsc_laps.append(lap_num)

    SC_VSC_laps = {
        'SC': safety_car_laps,
        'VSC': vsc_laps
    }

    is_pit_lap = df['PitInTime'].notna() | df['PitOutTime'].notna()
    is_neutralised = df['TrackStatus'] != '1'

    df['IsCleanLap'] = (~is_pit_lap) & (~is_neutralised) & (df['IsAccurate'] == True)
    clean_laps_df = df[df['IsCleanLap']].copy()

    return df, clean_laps_df, SC_VSC_laps
