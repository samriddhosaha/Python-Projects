import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()
import os
import calendar

# Load data
file_path = os.path.join(os.path.dirname(__file__), 'fcc-forum-pageviews.csv')
df = pd.read_csv(file_path, index_col='date', parse_dates=True)

# Clean data
df = df.dropna()
# clean outliers
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.barplot(x='year', y='value', hue='month', data=df_bar, palette='bright', ax=ax)
    labels = list(calendar.month_name[1:])  # ['January', ..., 'December']
    for t, l in zip(ax.legend(loc='upper left', title='Months').texts, labels): t.set_text(l)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.tight_layout()

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month'] = pd.Categorical(df_box['month'], 
                                     categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
                                     ordered=True)

    # Draw box plots
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1])
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    plt.tight_layout()

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
