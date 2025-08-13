# Jupyter Notebook Instructions

This file provides instructions on how to use Jupyter Notebooks for data exploration in this project.

## Starting the Jupyter Notebook Server

To start the Jupyter Notebook server, run the following command in your terminal:

```bash
jupyter notebook
```

This will open a new tab in your web browser with the Jupyter interface.

## Creating a New Notebook

1.  From the Jupyter web interface, navigate to the `scripts/data_utils` directory.
2.  Click the "New" button and select "Python 3 (ipykernel)" to create a new notebook.
3.  Rename the new notebook file to something descriptive, like `data_exploration.ipynb`.

## Loading the Data

To load the processed data into a pandas DataFrame, you can use the following code in a cell in your notebook:

```python
import pandas as pd

# Path to the processed ratings data
ratings_file = '../../data/processed/amazon_all_beauty/ratings.csv'

# Load the data into a pandas DataFrame
df = pd.read_csv(ratings_file)

# Display the first few rows of the DataFrame
df.head()
```

## Data Exploration Commands

Here are some useful commands for exploring the data in your notebook. It's a good practice to run each of these in a new cell to see the output clearly.

### Check for Missing Values

This command will show you the number of missing values in each column.

```python
df.isnull().sum()
```

### Get Summary Statistics

This command will give you summary statistics (like mean, min, max, etc.) for the numeric columns. This is useful for spotting any unusual values.

```python
df.describe()
```

### Check Data Types

This command will show you the data type of each column.

```python
df.info()
```

### Visualize the Rating Distribution

This command will create a histogram to show you the distribution of ratings.

```python
import matplotlib.pyplot as plt

df['rating'].hist(bins=5)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()
```

### Analyze User and Item Activity

These commands will help you understand how many ratings each user and item has. This is important for understanding the sparsity of the data.

```python
# Get the number of ratings for each user
user_rating_counts = df['userId'].value_counts()
print(user_rating_counts.describe())

# Get the number of ratings for each item
item_rating_counts = df['itemId'].value_counts()
print(item_rating_counts.describe())
```

## Saving and Stopping

*   **Save your notebook:** Click the "Save" icon in the toolbar or press `Ctrl + S`.
*   **Stop the server:** Press `Ctrl + C` in the terminal where you started the server.
