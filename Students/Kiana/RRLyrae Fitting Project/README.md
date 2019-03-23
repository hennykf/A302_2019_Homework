# Variable Star Light Curve Fitting Functions

An interactive module that fits light curves to variable star data, and allows a user to
visually sort these fits into good and bad fits.  Information about these fits is then stored in a .csv,
along with the input of the user on the goodness of the fit.

## Getting Started

First, you're going to want to create a list of all the datasets to be fitted, to pass to the fitting tool.  The names of the columns you will be using should be the same for all datasets.

### Prerequisites

You'll need to install the gatspy package;

```
$ pip install gatspy
```

## Functions

```
variable_star_eval(dataset, time_col, mag_col)
```
```
user_interface(list_of_files, time_col, mag_col, output_filepath)
```


### Using variable_star_eval
```
variable_star_eval(dataset, time_col, mag_col)
```

`dataset`: the .csv file with the time and magnitude data in it.  You could probably also use
flux instead of magnitude.

`time_col`: column with time data

`mag_col`: column with magnitude data

Returns: `fit_info`: Contains t, phase, and magnitude fit data, and the period used to
generate that fit.

This function creates 3 plots:
      1. The raw dataset in time vs magnitude. This can sometimes be helpful just to see where
      you're starting from and help give you a little intuition with the data.
      2. The Lomb Scargle Periodogram, which is used to determine the most likely period of the star.
      It finds the highest-power period, and uses that period to perform the light curve fit for the
      third graph.  If the light curve doesn't seem to fit very well, look to see if there are other
      high-power possible periods using this graph.
      3. One period of the light curve fit, which was generated using the RRLyraeTemplateModeler
         function from the gatspy library.  This fit is overlaid with the original data, which
         has been transformed to be displayed in one period.
  The function output includes the time, magnitude and phase information to recreate the fit shown
  in graph 3.


*Example:*
```
fit_info = variable_star_eval('ZTF18abosdvm.csv', 'jd', 'mag')
```

### Using user_interface

```
user_interface(list_of_files, time_col, mag_col, output_filepath)
```

`list_of_files`: A list, (), of all the datasets you want to evaluate for goodness of fit.

`time_col`: column with time data

`mag_col`: column with magnitude data

`output_filepath`: name of output file with fit data.  `user_interface` will automatically
create a .csv file, so do not include a file extension.

`user_interface` uses the variable_star_eval function to plot 3 graphs of the data, and asks the user to determine whether the fit is good.  If the fit is good, the user should enter "1", and if the fit is bad, they should enter "0". No other inputs are allowed. The function then creates two files, with the time, magnitude, and phase light curve data, and a column listing the original source of the data. All fits that
are given a 1 value are compiled into a file whose name is by `output_filepath`, and whether it is the good or bad fit file. For example, in the example below, the two files created will be `example_file_goodfits.csv` and `example_file_badfits.csv`, in the current working directory.


```
user_interface(('ZTF17aacnrhp.csv', 'ZTF18aavskho.csv', 'ZTF18abosdvm.csv'),
               'jd', 'mag', 'example_file')
```



## Author

* [**Kiana Henny**](https://github.com/hennykf)

## Acknowledgments

* Thanks to Jake VanderPlas, who created the gatspy library.
* Fitting methods closely follow those found here: https://jakevdp.github.io/blog/2015/06/13/lomb-scargle-in-python/
