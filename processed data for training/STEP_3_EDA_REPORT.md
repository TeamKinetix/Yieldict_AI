# CropYield — Step 3: Data Preprocessing & EDA

## Dataset used
The 10-column dataset from `crop_yield.csv.zip` was selected because it includes annual rainfall in addition to agricultural variables.

## Preprocessing decisions
- Standardized column names.
- Renamed `Crop_Year` to `year`.
- Removed leading/trailing whitespace from `crop`, `season`, and `state`.
- Converted numerical fields to numeric types.
- Removed exact duplicate rows.
- Kept zero-yield records because they correspond to zero-production observations and may be meaningful.
- **Removed `production` from the modeling dataset** because `yield` is essentially derived from production and area, creating target leakage.
- Extreme yield values were not deleted automatically because yield varies greatly by crop; we will compare robust model performance and may use a log-transformed target.

## Dataset summary
- rows: 19689
- columns: 9
- missing_values_total: 0
- duplicate_rows: 0
- crops: 55
- states: 30
- seasons: 6
- years: 24
- zero_yield_rows: 112

## Yield statistics

|       |         yield |
|:------|--------------:|
| count | 19689         |
| mean  |    79.954     |
| std   |   878.306     |
| min   |     0         |
| 1%    |     0.0812412 |
| 5%    |     0.249518  |
| 25%   |     0.6       |
| 50%   |     1.03      |
| 75%   |     2.38889   |
| 90%   |     9.532     |
| 95%   |    21.9149    |
| 99%   |   104.273     |
| max   | 21105         |

## Numeric correlations with yield

|                 |   correlation_with_yield |
|:----------------|-------------------------:|
| yield           |               1          |
| annual_rainfall |               0.020761   |
| fertilizer      |               0.00286186 |
| year            |               0.00253912 |
| area            |               0.00185848 |
| pesticide       |               0.00178163 |

## Main EDA findings
- The target is extremely right-skewed: median yield is about 1.03 while the maximum is 21,105.
- Crop type is expected to be a major predictor because different crops have very different yield scales.
- Simple Pearson correlations of individual numeric variables with yield are weak, so a nonlinear model and categorical features are important.
- The log-transformed target is much easier to model visually because it reduces the influence of extreme yield values.
- No missing values or duplicate rows remain after preprocessing.
