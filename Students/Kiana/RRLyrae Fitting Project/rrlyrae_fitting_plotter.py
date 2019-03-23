
import matplotlib as mpl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.stats import LombScargle as ls
from gatspy.periodic import RRLyraeTemplateModeler, LombScargle
from gatspy import datasets, periodic
import ipywidgets as widgets


def variable_star_eval(dataset, time_col, mag_col):
    '''
    This function creates 3 plots:
        1. The raw dataset in time vs magnitude.
        2. The Lomb Scargle Periodogram, to determine the most likely period of the star.
        3. One period of the light curve fit, which was generated using the RRLyraeTemplateModeler
           function from the gatspy library.  This fit is overlaid with the original data, which
           has been transformed to be displayed in one period.
    The function output includes the time, magnitude and phase information to recreate the fit shown
    in graph 3.
    '''

    mpl.style.use('ggplot')

    data = pd.read_csv(dataset)
    t, mag = data[time_col], data[mag_col]

    # plots the raw data
    fig, ax = plt.subplots()
    ax.scatter(t, mag)
    ax.set_title("Raw Brightness Data")
    ax.set(xlabel='Time', ylabel='Magnitude')
    plt.gca().invert_yaxis()
    plt.show()

    # plots a frequency-power plot of the data to find the most likely frequency for the variable star
    fig, ax = plt.subplots()
    model = LombScargle().fit(t, mag)
    periods, power = model.periodogram_auto(nyquist_factor=100)
    ax.plot(periods, power)
    ax.set_title('Lomb Scargle Periodogram')
    ax.set(xlim=(0.0, 1.4),
       xlabel='period (days)',
       ylabel='Lomb-Scargle Power');
    plt.show()

    #pulls the highest-power frequency from plot n.2 and uses this as the basis for model
    period = periods[np.argmax(power)]
    per_str = str(period)
    print("Most likely period is " + per_str + " days.")

    #  uses RRLyrae fitting program from Gatspy
    model = periodic.RRLyraeTemplateModeler()
    model.fit(t, mag)
    t_fit = np.linspace(0, period, 1000)
    mag_fit = model.predict(t_fit, period=period)
    phase = (t / period) % 1
    phasefit = t_fit / period

    # creates a dictionary containing all the fitting information.
    fit_info = pd.DataFrame({'t_fit': t_fit,
                            'mag_fit': mag_fit,
                            'phase_fit': phasefit,
                            'period (days)': period})
    fit_info_file = pd.DataFrame.to_csv(fit_info)

    # plot the fit
    fig, ax = plt.subplots()
    ax.errorbar(phase, mag, fmt='o')
    ax.plot(phasefit, mag_fit, '-', color='gray')
    ax.set(xlabel='phase', ylabel='magnitude')
    ax.invert_yaxis()
    ax.set_title('Light Curve Best Fit')
    plt.show()

    return(fit_info)


def user_interface(list_of_files, time_col, mag_col, output_filepath):
    '''
    This function inputs a list of files, which columns to use in files (must be the same
    columns for all files) and the location of the saved output.  It uses the variable_star_eval
    function to plot 3 graphs of the data, and asks the user to determine whether the fit is
    good.  If the fit is good, the user should enter "1", and if the fit is bad, they should enter "0".
    No other inputs are allowed. The function then creates a file with the time, magnitude, and phase
    fit curve data, as well as a column with the binary indicator of goodness of fit, and column listing
    the original source of the data.

    A user could use these two columns to subset the data to only good or bad fits, and further filter to
    a specific dataset.
    '''

    instructions = '''
    Guidelines for good or bad fits:

    If using sparse data, it may be difficult to find a high-power fit.
    When judging a fit, if there is an obvious mismatch between the light curve fit and
    the data points, this is an indicator it is not a good fit. Examples include:
        If most data points falls roughly along the modeled light curve, but there are one or
        more points which clearly do not align with the curve.

        Most data points do not align with the modeled light curve at all.

        There is significant scatter even though the points generally align with the modeled
        light curve.

    If any of these are the case for a dataset and fit, it should be marked "0" to indicate
    a poor fit.
    You may want to examine the Lomb Scargle Periodogram of poorly fitted datasets to see
    if there are other highly likely periods.
    '''
    print(instructions)
    #initiates an output file
    output_file_good = pd.DataFrame()
    output_file_bad = pd.DataFrame()


    # Loops through all datasets in the list_of_files, generates the graphs, and
    # requires the user to decide if the fit is good or not.

    for file in list_of_files:
        fit_info = variable_star_eval(file, time_col, mag_col)

        # interactive part where user evaluates whether it's a good fit
        while True:
            try:
                fit_qual = int(input("Is this curve a good fit? 1 = good fit, 0 = not good fit. "), 2)
                break
            except ValueError:
                print("Error: Must enter either 1 or 0.")

        # Creates files based on user's input, 1 is good fit, 0 is bad fit.
        if fit_qual == 1:
            output_file_good = output_file_good.append(fit_info)
        elif fit_qual == 0:
            output_file_bad = output_file_bad.append(fit_info)


        # Creates column with name of file data is from
        fit_info['original_datafile_name'] = file

    print("Great job! You're done evaluating fits! Fit data can be found at the filepath you provided; " + output_filepath)
    save_out_good = output_file_good.to_csv(output_filepath + "_goodfits" + ".csv")
    save_out_bad = output_file_bad.to_csv(output_filepath + "_badfits" + ".csv")
