# BlightFight
Repo for Capstone Project of Data Science at Scale course offered by University of Washington on Coursera.

[Final Report](https://github.com/dnc1994/BlightFight/blob/master/src/Final-Report.ipynb)

[Average Blight Risk Visualization](https://dnc1994.com/BlightFight/src/dmap.html)

## Task

Work with real data collected in Detroit to help urban planners predict **blight** (the deterioration and decay of buildings and older areas of large cities, due to neglect, crime, or lack of economic support).

## Approach

### Step 1: Establish a list of all the buildings with their space extents.

#### Done

0. Filter NAs and invalid coordinates (outside the bounds of Detroit)
1. Extract latitutude/longitude pair and address (in raw text) from 4 files
2. Concatenate them into one data frame
3. Clean up the address field (extract numbers, drop symbols, normalize spelling, expand abbreviations, etc)
4. Cluster geolocations by fuzzy matching on address field and incident proximities (`eps = 0.000075`).
5. Represent each building with a rectangle centered at average coordinates.

#### Tried

- DBSCAN based on coordinates, no good.
- DBSCAN based on a combination of coordinates and address fields, impossible to do without rewriting algorithm because of the way that feature distances are computed.

### Step 2: Generate a balanced data set for training and testing

#### Done

0. Map demolition permits to buildings, derive positive labels.
1. Random sample a same amount of buildings with negative labels.
2. Concatenate them into a "training" set.

#### Note

This "training" set will later be divided into a (real) training set and a validation set. In this task it does not make much sense to use the remaining data as a "testing" set (at least no in a traditional sense) because we only got buildings that are not on the demolition list. And there's no way to figure out their true labels. So this part is a little bit like **semi-supervised learning**: I'll just evaluate the model on the validation set and use the remaining data for visualization and drawing conclusions. Anyway this is also what the task requires us to do.

### Step 3: Develop a naive model and evalute its performance.

I believe it's OK to jump right to Step 4.

### Step 4: Feature engineering.

#### Done

0. Derive features from `violations.csv`, `calls.csv` and `crimes.csv`. Bascially counts of one-hot-encoded categorical variables.
1. Examine feature importance using random forest. Got a ~0.83 AUC score on OOB data.

#### Note

Counts of violations and crimes are the simplist yet most important features. I even hadn't include a decaying propagation effect of bad incidents.

### Step 5: Develop a more advanced model.

0. Trained a Xgboost model, got a ~0.85 AUC score on OOB data
1. Simplify the model and still got a~0.849 AUC score.

### Step 6: Evaluation and drawing conclusions.

Present a summary with some visualizations.

0. Explain the model.
1. Make a Choropleth map of blight risks on out-of-sample data.

## Author
[Linghao Zhang](https://github.com/dnc1994)

## License
[MIT license](https://github.com/dnc1994/BlightFight/blob/master/LICENSE)
