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


### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system


## Author

* [**Kiana Henny**](https://github.com/hennykf)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Jake VanderPlas, who created the gatspy library.
* Fitting methods closely follow those found here: https://jakevdp.github.io/blog/2015/06/13/lomb-scargle-in-python/
