import pandas as pd
import numpy as np
from mySSA import mySSA
from sklearn.metrics import mean_squared_error, mean_absolute_error

def run_ssa_and_get_forecast():
    """Helper function to run the SSA process and return the forecast."""
    ts = pd.read_csv('AirPassengers.csv', parse_dates=True, index_col='Month')
    ts_ = ts.copy()
    ts_.iloc[67:79] = np.nan
    ts_.loc['1961-12-01', '#Passengers'] = np.nan
    ts_ = ts_.asfreq('MS')
    ssa = mySSA(ts_)
    ssa.embed(embedding_dimension=36, suspected_frequency=12)
    ssa.decompose()
    return ssa.forecast_recurrent(steps_ahead=48, return_df=True)

def calculate_error_metrics(original, forecast):
    """Adaptor function to calculate MSE and MAE."""
    # Ensure the forecast and original data are aligned
    common_index = original.index.intersection(forecast.index)
    original_aligned = original.loc[common_index]
    forecast_aligned = forecast.loc[common_index]

    mse = mean_squared_error(original_aligned, forecast_aligned)
    mae = mean_absolute_error(original_aligned, forecast_aligned)

    return {'MSE': mse, 'MAE': mae}

def test_forecast_consistency():
    """Tests if the forecast is consistent with a baseline."""
    # Run the SSA process to get the current forecast
    current_forecast = run_ssa_and_get_forecast()

    # Load the baseline forecast
    baseline_forecast = pd.read_csv('baseline_forecast.csv', parse_dates=True, index_col=0)
    baseline_forecast.index.freq = 'MS'

    # Check if the forecasts are close enough (allowing for small floating point differences)
    pd.testing.assert_frame_equal(current_forecast, baseline_forecast, check_exact=False, rtol=0.05)

def test_error_metrics():
    """Tests if the MSE and MAE are within a negligible threshold."""
    # Run the SSA process to get the forecast
    forecast_df = run_ssa_and_get_forecast()

    # Load original data
    original_ts = pd.read_csv('AirPassengers.csv', parse_dates=True, index_col='Month')
    original_ts.rename(columns={'#Passengers': 'Original'}, inplace=True)

    # Calculate error metrics
    error_metrics = calculate_error_metrics(original_ts['Original'], forecast_df['Forecast'])

    # Assert that the errors are negligible
    assert error_metrics['MSE'] < 100
    assert error_metrics['MAE'] < 10
