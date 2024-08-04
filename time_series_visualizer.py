import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from calendar import month_name
from calendar import month_abbr
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df = pd.DataFrame(df)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    global df
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by = 'date')
    dates = df['date']
    values = df['value']

    fig = plt.figure(figsize=(10, 5))
    plt.plot(dates, values, color='red')

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    global df
    # Copy and modify data for monthly bar plot
    df['date'] = pd.to_datetime(df['date'])
    months = list(month_name[1:])
    df['months'] = pd.Categorical(df['date'].dt.strftime('%B'), categories=months, ordered=True)
    
    # Draw bar plot
    df_bar = pd.pivot_table(data=df, index=df['date'].dt.year, columns='months', values='value', observed=True)
    ax = df_bar.plot(kind='bar', figsize=(12, 4), ylabel='Mean Page Views', xlabel='Year', rot=0)
    ax.legend(bbox_to_anchor=(0.95, 0.95), loc='upper left')

    fig = plt

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    months_order = list(month_abbr[1:13])
    df_box['month'] = pd.Categorical(df_box['month'], categories=months_order, ordered=True)

    fig, axs = plt.subplots(1, 2, figsize=(10,5))
    sns.boxplot(x='year', y='value',hue='year', data=df_box, ax=axs[0], palette='Set2', legend=False)
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value',hue='month', data=df_box, ax=axs[1], palette='husl', legend=False)
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    plt.tight_layout()
    fig = plt

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_line_plot()
draw_bar_plot()
draw_box_plot()