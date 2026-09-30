import pandas as pd
import matplotlib.pyplot as plt


#this dict was in a github repo
STATE_CODES = {
"AK": "Alaska",
"AL": "Alabama",
"AR": "Arkansas",
"AZ": "Arizona",
"CA": "California",
"CO": "Colorado",
"CT": "Connecticut",
"DE": "Delaware",
"FL": "Florida",
"GA": "Georgia",
"HI": "Hawaii",
"IA": "Iowa",
"ID": "Idaho",
"IL": "Illinois",
"IN": "Indiana",
"KS": "Kansas",
"KY": "Kentucky",
"LA": "Louisiana",
"MA": "Massachusetts",
"MD": "Maryland",
"ME": "Maine",
"MI": "Michigan",
"MN": "Minnesota",
"MO": "Missouri",
"MS": "Mississippi",
"MT": "Montana",
"NC": "North Carolina",
"ND": "North Dakota",
"NE": "Nebraska",
"NH": "New Hampshire",
"NJ": "New Jersey",
"NM": "New Mexico",
"NV": "Nevada",
"NY": "New York",
"OH": "Ohio",
"OK": "Oklahoma",
"OR": "Oregon",
"PA": "Pennsylvania",
"RI": "Rhode Island",
"SC": "South Carolina",
"SD": "South Dakota",
"TN": "Tennessee",
"TX": "Texas",
"UT": "Utah",
"VA": "Virginia",
"VT": "Vermont",
"WA": "Washington",
"WI": "Wisconsin",
"WV": "West Virginia",
"WY": "Wyoming",
"DC": "District of Columbia",
"AS": "American Samoa",
"GU": "Guam GU",
"MP": "Northern Mariana Islands",
"PR": "Puerto Rico PR",
"VI": "U.S. Virgin Islands",
}


def plot_aqi(aqi_series, state_name, county_name, destination, filename=None):
    avg_aqi = round(aqi_series.mean())
    #set teh plot color
    plot_color = 'red' if avg_aqi > 50 else 'green'

    plt.plot(aqi_series.values, color=plot_color)
    
    plt.title(f"{county_name} County, {state_name}\nAverage AQI: {avg_aqi}")

    #show or save the plot
    if destination == '1':
        plt.show()
    elif destination == '2':
        if filename:
            plt.savefig(filename)
        plt.close()

def main():
    headers = ["State Code","County Code","Site Num","Parameter Code",
        "POC","Latitude","Longitude","Datum","Parameter Name","Sample Duration",
        "Pollutant Standard","Date Local","Units of Measure","Event Type",
        "Observation Count","Observation Percent","Arithmetic Mean","1st Max Value",
        "1st Max Hour","AQI","Method Code","Method Name","Local Site Name","Address",
        "State Name","County Name","City Name","CBSA Name","Date of Last Change"]
    
    df = pd.read_csv("daily_44201_2021.csv", names=headers, header=0, low_memory=False)
    #Infinite loop for state selection
    while True:
        state_code = input("please enter a 2 letter state code (Q to quit): ").strip().upper()
        if state_code == "Q": break
        if state_code not in STATE_CODES:
            print("Invalid state code, please try again.")
            continue
        state_name = STATE_CODES[state_code]

        #split the df into just state data
        df_state = df[df["State Name"] == state_name]

        #Inifinite loop for county selection
        while True:
            counties = sorted(list(set(df_state['County Name'])))

            #print all the counties with an index
            print()
            for idx, county in enumerate(counties):
                print(f"{idx}: {county}")

            county_num = input("Please enter a number for a county: ").strip()
            try:
                county_name = counties[int(county_num)]
            except IndexError, ValueError:
                print("Invalid county selection")
                continue
            output_choice = input("\n1: Screen\n2: File\nSelect an output for the plot: ").strip()
            file_name = None
            if output_choice == "2":
                file_name = input("Enter a file name for the ouput (incluude file extention): ")
            #seperate to just county data without losing state data
            df_county = df_state[df_state['County Name'] == county_name]
            #get that countys aqi
            aqi_data = df_county['AQI'].dropna()

            plot_aqi(aqi_data, state_name, county_name, output_choice, file_name)

            again = input("Would you like to do annother county? (y/n) ")
            if again.lower() != 'y':
                break



if __name__ == "__main__":
    main()
