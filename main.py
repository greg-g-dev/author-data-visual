# Tiny WebDev
# Python data visualization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def scale_by_million(x):
  return x/1000000

def scale_by_thousand(x):
  return x/1000

with open("books.csv","r") as datafile:
    data = pd.read_csv(datafile,delimiter=",")

# Questions to answer
# 1. Authors with most titles
# 2. Authors with most ratings
# 3. Authors with highest ratings
# 4. Title with most ratings
# 5. Title with highest ratings
# 6. Is there a relationship for authors between their rating and number of volumes?
# 7. Does top titled author get consistent rating across their titles

# Set Author as Index
author_data = data.set_index("authors", drop = False)

# Stephen King titles
king_data = author_data.loc["Stephen King",["title","average_rating","ratings_count"]]
print(f"Stephen Books\n{king_data}")

# Get the Stephen King titles with the top 10 ratings count
king_rating_count_top10 = king_data.nlargest(10,'ratings_count',keep='all')

# Initialize subplot to hold all the Stephen King charts
figure, king_chart = plt.subplots(3,1,figsize=(15,10))

# Bar chart for the  average rating of Top 10 Stephen King titles
king_chart[0].barh(king_rating_count_top10['title'],king_rating_count_top10['average_rating'], .5, color="red")

king_chart[0].set_xlabel('Rating')
king_chart[0].set_ylabel('Title')
king_chart[0].title.set_text('Stephen King Average Rating for Titles with Most Ratings')


# Save plot that was created
# Use bbox_inches setting to make sure nothing gets cropped out of figure
#plt.show()
#plt.savefig("fig-1-king-rating-bar.png", bbox_inches="tight")

# Bar chart for the rating count of Top 10 Stephen King titles
king_chart[1].barh(king_rating_count_top10['title'],king_rating_count_top10['ratings_count'],.5, color="red")

king_chart[1].set_xlabel('Rating Count')
king_chart[1].set_ylabel('Title')
king_chart[1].title.set_text('Stephen King Ratings Count for Titles with Most Ratings')

# Save plot that was created
# Use bbox_inches setting to make sure nothing gets cropped out of figure
#plt.savefig("fig-2-king-rating-count-bar.png", bbox_inches="tight")


# Stephen King title rating vs number of ratings
king_chart[2].scatter(king_data['ratings_count'],king_data['average_rating'], color="red")


king_chart[2].set_xlabel('Rating Count')
king_chart[2].set_ylabel('Rating')
king_chart[2].title.set_text('Stephen King Title Rating vs Number of Ratings')

# Save plot that was created
# Use bbox_inches setting to make sure nothing gets cropped out of figure
plt.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)
plt.savefig("fig-1-king.png", bbox_inches="tight")

# Group dataframe by author
data_by_author = data.groupby('authors')

# Average rating and title count per author 
author_avg_rating = data_by_author['average_rating'].agg([np.size,np.mean]).rename(columns={'size': 'title_count', 'mean': 'rating_mean'})


# Rating count
author_num_rating = data_by_author['ratings_count'].agg([np.sum]).rename(columns={'sum': 'total_rating_count'})

# Merge data sets together on author
author_avg_num_rating = author_avg_rating.merge(author_num_rating,left_on='authors', right_on='authors')


# Initialize subplot to hold all the Author charts
figure, author_chart = plt.subplots(2,1,figsize=(15,10))

# Get Authors with the 10 largest title counts
# Keep the ties
author_title_top10=author_avg_num_rating.nlargest(10,'title_count',keep='all')

print(f"Authors with the largest title count:\n {author_title_top10}")



# Author Bar chart Figure 1
#author_title_top10.plot.bar(y="title_count")
author_chart[0].barh(author_title_top10.index,author_title_top10['title_count'],.5)
#king_chart[1].barh(king_rating_count_top10['title'],king_rating_count_top10['ratings_count'],.5, color="red")

author_chart[0].set_xlabel('Title Count')
author_chart[0].set_ylabel('Author')
author_chart[0].title.set_text('Top 10 Author Title Counts')


#Scale down the number of ratings to millions
author_avg_num_rating['total_rating_count'] = author_avg_num_rating['total_rating_count'].transform(scale_by_million)

# Get authors with the top 10 largest total rating count
# Keep ties
author_rating_top10 = author_avg_num_rating.nlargest(10,'total_rating_count',keep='all')
print(f"Authors with the largest total rating count:\n {author_rating_top10}")

# Author Bar chart Figure 2
# Index is used for x-axis
author_chart[1].barh(author_rating_top10.index,author_rating_top10['total_rating_count'],.5)
author_chart[1].set_xlabel('Millions of Ratings')
author_chart[1].set_ylabel('Author')
author_chart[1].title.set_text('Top 10 Author Rating Counts')

plt.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)
# Save plot that was created from figures
# Use bbox_inches setting to make sure nothing gets cropped out of figure
plt.savefig("fig-2-author.png", bbox_inches="tight")

# Get authors with the top 100 largest total rating count
# Keep ties 
author_rating_top100 = author_avg_num_rating.nlargest(100,'total_rating_count',keep='all')

# Bubble scatter plot using Seaborn
# Size of bubble is title count
# Is there a relationship with title count?
auth_chart=sns.relplot(x="total_rating_count", y="rating_mean", size="title_count", sizes=(10,700), alpha=.5, palette="muted", data=author_rating_top100)
plt.xticks(rotation=90)
plt.xlabel('Millions of Ratings')
plt.ylabel('Mean Rating')
auth_chart.set(title='Relationship Between Title Count, Rating Count and Mean Rating')
#plt.title('Relationship Between Title Count, Rating Count and Mean Rating')
# Save plot that was created
# Use bbox_inches setting to make sure nothing gets cropped out of figure
plt.savefig("fig-3-author-rating-top100.png", bbox_inches="tight")
