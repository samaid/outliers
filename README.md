# Automated detection of outliers from performance measurements

`pip install outlier_utils` - this is a required package
`pip install pandas` or `conda install pandas` - this is a required package
`python outlier_detector.py` - to run this example

The example contains an example dataset of historic data for some artificial workload that runs on a regular basis for performance regression monitoring. In this dataset there are 3 fields `Date`, the date when the measurement was performed, `Performance`, floating point number representing performance. It can be in any units. Current implementation assumes higher numbers mean slower. If your measurment units mean higher is better then you need to change lines 47 and 52. Replace `sgt.min_test_indices` with `sgt.max_test_indices`, and vice versa. The third column `Verdict` meaning verdict about each measurement. Possible values
* `""` - new data point, no verdict yet
* `"manual-inspection"` - not enough historic data to make an automated decision about regression; it requires manual human inspection.
* `"no-regression"` - measurement compared against historic data and does not seem a regression
* `"potential-regression"` - measurement compared against historic data and does seem a regression. Requires human confirmation to set verdict `"regression"`
* `"regression"` - human inspected `"potential-regression"` and found that this is actual regression
* `"potential-improvement"` - measurement compared against historic data and does look like an improvement. Requires human confirmation to set verdict `"improvement"`
* `"improvement"` - human inspected `"potential-improvement"` and found that this is actual improvement
* `"false-positive"` - human inspected `"potential-improvement"` or `"potential-regression"` and found that this is a false positive

In the example there are 3 new data points simulating
* New improvement
* New regression
* No regression cases

Comment-uncomment lines 72-74 to observe effects.

Have a wonderful journey!
