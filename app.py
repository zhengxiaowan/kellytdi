from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import numpy as np
from bokeh.models import PrintfTickFormatter, LinearAxis, Range1d
from bokeh.plotting import figure, output_file, show
from bokeh import embed

app = Flask(__name__)

# Load the dataset
df_info=pd.read_csv('df_info.csv')
us_state_abbrev = {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGINIA': 'VA',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY',
    'DISTRICT OF COLUMBIA': 'DC',
    'PUERTO RICO': 'PR'
}


@app.route('/',methods=['GET','POST'])
def index():
#  return render_template('index.html')

    if request.method == 'GET':
        return render_template('index.html')
    else:
        statein=request.form['state']
        stateout=str(statein).upper()
        
        if stateout not in us_state_abbrev.values():
            return 'Wrong input, please check!'
        else:
            df=df_info[df_info['state']==stateout].set_index('year')
            years = ['2011','2012','2013','2014','2015','2016','2017']
            q1 = df['q25']
            q2 = df['median']
            q3 = df['q75']
            iqr = q3 - q1
            upper= q3 + 1.5*iqr
            lower = q1 - 1.5*iqr
            upper = df['q0']
            lower = df['q100']
            count=df['count'].values
            ylim=max(count)*1.05

            p = figure(tools="save", background_fill_color="#EFE8E2", title="Box plot of Wage in "+str(stateout), x_range=years, x_axis_label='Year', y_axis_label='Wage in $')

            # stems
            p.segment(years, upper, years, q3, line_color="black")
            p.segment(years, lower, years, q1, line_color="black")

            # boxes
            p.vbar(years, 0.7, q2, q3, fill_color="#E08E79", line_color="black")
            p.vbar(years, 0.7, q1, q2, fill_color="#3B8686", line_color="black")

            # whiskers (almost-0 height rects simpler than segments)
            p.rect(years, lower, 0.2, 0.01, line_color="black")
            p.rect(years, upper, 0.2, 0.01, line_color="black")

            p.xgrid.grid_line_color = None
            p.ygrid.grid_line_color = "white"
            p.grid.grid_line_width = 2
            p.xaxis.major_label_text_font_size="12pt"
            p.left[0].formatter.use_scientific = False
            p.y_range = Range1d(0, max(upper)*1.05)

            p.extra_y_ranges = {"foo": Range1d(start=0, end=ylim)}
            p.add_layout(LinearAxis(y_range_name="foo", axis_label="Petition Number"), 'right')
            p.line(['2011','2012','2013','2014','2015','2016','2017'], count, line_width=2, color="blue", y_range_name="foo",legend="petition number")    
            # Embed plot into HTML via Flask Render
            script, div = embed.components(p)
            #show(p)
            return render_template('graph.html', script=script, div=div)
    

if __name__ == '__main__':
  app.run(port=33507)
