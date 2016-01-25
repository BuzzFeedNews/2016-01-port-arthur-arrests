
import sys, os
import pandas as pd
import numpy as np
import zipfile

# reshape the data so that every offense is on a new row

def reshape_jail_data(df):
    df.drop(["Unnamed: 26"], axis=1, inplace=True)
    cols = df.columns.tolist()
    off_num_start = cols.index("#")
    n_offenses = len(df.columns[off_num_start:]) / 5
    # check that there are 10 offenses
    def get_offense_slice(offense_i):
        start_i = off_num_start + (5 * offense_i)
        end_i = off_num_start + (5 * (offense_i + 1))
        df_slice = df[df.columns[start_i:end_i]].copy()
        df_slice.columns = [ "#", "OFFENSE", "BOND", "WARRANT #", "FILED BY" ]
        df_slice["JAIL ID"] = df["ID#"]
        df_slice["ARREST DT"] = df["ARRESTED "]
        df_slice["RELEASE DT"] = df["RELEASE DT"]
        df_slice["RACE_SEX"] = df["RS"]        
        return df_slice
    offenses = pd.concat([ get_offense_slice(i) for i in range(int(n_offenses)) ])
    return offenses

def clean_up(df):
    _offenses = reshape_jail_data(df)\
        .sort_values([ "ARREST DT", "JAIL ID", "#" ])

    offenses = _offenses[
        _offenses["OFFENSE"].notnull() &
        # Nine release dates are listed as "0"
        (_offenses["RELEASE DT"] != 0)
    ].copy()

    offenses["ARREST DT"] = pd.to_datetime(offenses["ARREST DT"])

    offenses["RELEASE DT"] = pd.to_datetime(offenses["RELEASE DT"]\
        .astype(str).str.extract(r"([0-9]{4}-[0-9]{2}-[0-9]{2})"))

    time_served = offenses["RELEASE DT"] - offenses["ARREST DT"]
    offenses["days_served"] = time_served / np.timedelta64(1, "D")
    offenses["ARREST YEAR"] = offenses["ARREST DT"].dt.year
    offenses["RACE"] = offenses["RACE_SEX"].str[0]
    offenses["SEX"] = offenses["RACE_SEX"].str[1]
    return offenses


# Filter for just traffic related offenses and exclude other class Cs

# The data does not include a precise indication of whether an offense was traffic-related.
# Instead, BuzzFeed News manually identified offenses that appeared to be unambiguously
# traffic-related. For that reason, the analysis may underestimate the number of traffic-only arrests.

non_disqualifying_charges = [
    "FAILURE TO APPEAR", "", "CONTEMPT OF COURT", "CAPIAS PROFINE"
]

def is_traffic(charge):
    if  ("FAILURE TO MNTN FINAN RESP" in charge or
         "SPEED" in charge or
         "DRIVING" in charge or
         "TRAF OFF-NO CHILD RESTRAINT" in charge or
         "TRAF OFF-MOVING-NO SEATBELT" in charge or
         "NO LIABILITY INSURANCE" in charge or
         "STOP SIGN- RUNNING" in charge or
         "STOP LIGHT- RUNNING" in charge or
         "FAILURE TO SIGNAL" in charge or
         "TRAFFIC" in charge or
         "FAILURE CHANGE DL ADDRESS" in charge or
         "YIELD" in charge or
         "TRAFFIC OFFENSE-MOVING" in charge or
         "DRIVING-WHILE LIC EXPIRED" in charge or
         "FAILURE TO MNTN SINGLE LANE" in charge or
         "VEH-LICENSE PLATE OFFENSE" in charge or
         "WRONG WAY ON A ONE WAY" in charge or
         "DRIVING-NO MVI STICKER" in charge or
         "DEFECTIVE EQUIPMENT" in charge or
         "WRONG SIDE ROAD-NOT PASSING" in charge or 
         "DWI- UNDER 21/CLASS C" in charge or
         "FAILURE TO STOP RENDER AID" in charge or
         "FAILURE TO STOP RENDER INFO" in charge or
         "NEGLIGENT COLLISION" in charge):
        return True
    return False

def has_traffic_only(row):
    all_charges = row["charges"]
    has_class_c_only = False
    has_disqualifying_charges = False
    for c in all_charges: 
        if is_traffic(c):
            has_class_c_only = True
            continue
        if c not in non_disqualifying_charges:
            return False
    return has_class_c_only

def filter_traffic(df):
    grouped = df.groupby([ "JAIL ID", "ARREST DT" ])
    rapsheets = pd.DataFrame({
        "charges": grouped["OFFENSE"].apply(list),
        "warrants_filed_by": grouped["FILED BY"].apply(list)
        })
    rapheets_extra = grouped[[
        "RACE", "SEX", "RELEASE DT", "ARREST YEAR", "days_served"
    ]].first()
    rapsheets_final = rapsheets.join(rapheets_extra)
    traffic_only = rapsheets_final[
        rapsheets_final.apply(has_traffic_only, axis=1)
    ]
    return traffic_only

if __name__ == "__main__":
    HERE = os.path.dirname(os.path.realpath(__file__))
    RAW_DIR = os.path.join(HERE, "../data/raw/")

    path = os.path.join(RAW_DIR, "PAPD_ClassC_NoNames.csv")
    
    jail_data_raw = pd.read_csv(path)

    CLASS_C_OUT_FILENAME = "all_class_c_arrests.csv"
    CLASS_C_OUT_PATH = os.path.join(HERE, "../data/clean/", CLASS_C_OUT_FILENAME)
    cleaned_up_jail_data = clean_up(jail_data_raw)
    cleaned_up_jail_data.to_csv(CLASS_C_OUT_PATH, index=False, encoding="utf-8")

    TRAFFIC_OUT_FILENAME = "traffic_only.csv"
    TRAFFIC_OUT_PATH = os.path.join(HERE, "../data/clean/", TRAFFIC_OUT_FILENAME)
    traffic_only = filter_traffic(cleaned_up_jail_data)
    traffic_only.to_csv(TRAFFIC_OUT_PATH, encoding="utf-8")
