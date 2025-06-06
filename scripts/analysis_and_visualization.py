import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Optional

def visualize_rating_distribution_side_by_side(
    data: pd.DataFrame,
    column: str,
    top_n: Optional[int] = 10,
    figsize: tuple = (16, 6),
    palette: str = 'viridis',
    rotation: int = 45,
    title: Optional[str] = None
) -> pd.DataFrame:
    """
    Create side-by-side visualizations of review count and average rating distribution.
    
    Args:
        data: Input DataFrame containing review data
        column: Column name to group by (e.g., 'app_name')
        top_n: Number of top categories to display (None for all)
        figsize: Figure dimensions (width, height)
        palette: Color palette name
        rotation: X-axis label rotation
        title: Custom title for the plot
    
    Returns:
        pd.DataFrame: Aggregated statistics with count and mean rating
    
    Example:
        df = pd.read_csv('reviews.csv')
        stats = visualize_rating_distribution_side_by_side(df, 'app_name')
    """
    # Input validation
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas DataFrame")
    if column not in data.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    if 'rating' not in data.columns:
        raise ValueError("DataFrame must contain a 'rating' column")

    # Prepare data
    if top_n:
        top_categories = data[column].value_counts().nlargest(top_n).index
        data = data[data[column].isin(top_categories)]
    
    # Calculate statistics
    stats = (
        data.groupby(column)['rating']
        .agg(['count', 'mean'])
        .sort_values('count', ascending=False)
        .reset_index()
    )
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Plot 1: Review Count
    sns.barplot(
        data=stats,
        x=column,
        y='count',
        ax=ax1,
        palette=palette,
        order=stats[column]
    )
    ax1.set_title(f'Review Count by {column}', pad=20)
    ax1.set_xlabel('')
    ax1.set_ylabel('Number of Reviews')
    ax1.tick_params(axis='x', rotation=rotation)
    
    # Plot 2: Average Rating
    sns.barplot(
        data=stats,
        x=column,
        y='mean',
        ax=ax2,
        palette=palette,
        order=stats[column]
    )
    ax2.set_title(f'Average Rating by {column}', pad=20)
    ax2.set_xlabel('')
    ax2.set_ylabel('Average Rating (1-5)')
    ax2.tick_params(axis='x', rotation=rotation)
    ax2.set_ylim(0, 5)
    
    # Add overall title if specified
    if title:
        fig.suptitle(title, y=1.05, fontsize=14)
    
    plt.tight_layout()
    plt.show()
    
    return stats