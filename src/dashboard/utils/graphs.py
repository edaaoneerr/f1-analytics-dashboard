import statsmodels.formula.api as smf
import statsmodels.api as sm
import numpy as np
import pandas as pd

# Load data
f1_data = pd.read_csv("f1_single_analytical_dataset.csv")

# Recreate logged variables
f1_data['log_temprature'] = np.log(f1_data['temperature'])
f1_data['log_windspeed'] = np.log(f1_data['windspeed'])
f1_data['log_pit_duration'] = np.log(f1_data['min_pit_duration'])
f1_data['log_fastest_lap_time'] = np.log(f1_data['fastest_lap_time'])

formula = 'is_crash ~ is_street_circuit + qualifying_position + pit_stop_count + log_pit_duration + log_fastest_lap_time + log_temprature + log_windspeed + precipitation'

log_model = smf.glm(
    formula=formula,
    data=f1_data,
    family=sm.families.Binomial()
).fit()

params = log_model.params

means = f1_data.mean(numeric_only=True)

def predict_probability(street_value):

    logit = (
        params["Intercept"]
        + params["is_street_circuit"] * street_value
        + params["qualifying_position"] * means["qualifying_position"]
        + params["pit_stop_count"] * means["pit_stop_count"]
        + params["log_pit_duration"] * means["log_pit_duration"]
        + params["log_fastest_lap_time"] * means["log_fastest_lap_time"]
        + params["log_temprature"] * means["log_temprature"]
        + params["log_windspeed"] * means["log_windspeed"]
        + params["precipitation"] * means["precipitation"]
    )

    return 1 / (1 + np.exp(-logit))


p_non_street = predict_probability(0)
p_street = predict_probability(1)

difference = (p_street - p_non_street) * 100