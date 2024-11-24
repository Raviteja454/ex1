# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kE2mFF_0l9OrZv0DeppOwKQE_biALDQd
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

data = pd.ExcelFile('Bookshop.xlsx')
sheets = data.sheet_names
sheets

book_df = pd.read_excel('Bookshop.xlsx', sheet_name='Book')
book_df.head()

author_df = pd.read_excel('Bookshop.xlsx', sheet_name='Author')
author_df.head()

author_df.insert(1,'Author',author_df['First Name']+' '+author_df['Last Name'])
author_df.drop(['First Name','Last Name','Birthday','Country of Residence','Hrs Writing per Day'],axis=1, inplace=True)
author_df.head()

info_df = pd.read_excel('Bookshop.xlsx', sheet_name='Info')
info_df.head()

info_df.insert(0,'BookID',info_df['BookID1']+info_df['BookID2'].astype(str))
info_df.drop(['BookID1','BookID2','SeriesID','Volume Number','Staff Comment'],axis=1, inplace=True)
info_df.head()

award_df = pd.read_excel('Bookshop.xlsx',sheet_name='Award')
award_df.head()

checkout_df = pd.read_excel('Bookshop.xlsx', sheet_name='Checkouts')
checkout_df.head()

edition_df = pd.read_excel('Bookshop.xlsx', sheet_name='Edition')
edition_df.head()

publish_df = pd.read_excel('Bookshop.xlsx',sheet_name='Publisher')
publish_df.head()

rating_df = pd.read_excel('Bookshop.xlsx', sheet_name='Ratings')
rating_df.head()

rating_df.rename(columns={'ReviewerID':'UserID'},inplace=True)
rating_df.drop('ReviewID',axis=1,inplace=True)

sales_q1_df = pd.read_excel('Bookshop.xlsx', sheet_name='Sales Q1')
sales_q2_df = pd.read_excel('Bookshop.xlsx', sheet_name='Sales Q2')
sales_q3_df = pd.read_excel('Bookshop.xlsx', sheet_name='Sales Q3')
sales_q4_df = pd.read_excel('Bookshop.xlsx', sheet_name='Sales Q4')

sales_data = pd.concat([sales_q1_df, sales_q2_df, sales_q3_df, sales_q4_df],ignore_index=True)
sales_data.head()

sales_data.drop('Discount',axis=1,inplace=True)

books_with_authors = pd.merge(book_df, author_df, left_on='AuthID', right_on='AuthID', how='inner')
books_with_authors.head()

books_with_authors.drop('AuthID',axis=1,inplace=True)

books_with_info = pd.merge(books_with_authors,info_df,left_on='BookID', right_on='BookID', how='inner')
books_with_info.head()

books_with_checkouts = pd.merge(books_with_info, checkout_df, left_on='BookID', right_on='BookID', how='left')
books_with_checkouts.head()

books_with_checkouts.info()

books_with_checkouts['CheckoutMonth'].fillna(books_with_checkouts['CheckoutMonth'].mode()[0],inplace=True)
books_with_checkouts['Number of Checkouts'].fillna(books_with_checkouts['Number of Checkouts'].median(),inplace=True)

books_with_editions = pd.merge(books_with_checkouts, edition_df, left_on='BookID', right_on='BookID', how='inner')
books_with_editions.head()

final_df = pd.merge(books_with_editions, rating_df, left_on='BookID', right_on='BookID', how='left')
final_df.head()

final_df.info()

final_df.dropna(inplace=True)

final_df.info()

final_df.columns

final_df.describe()

final_df.Title.nunique()

final_df.Title.unique()

plt.figure(figsize=(10,10))
final_df.value_counts('Title').plot(kind='bar')
plt.title('Count of Books')
plt.show()

avg_rating_per_book = final_df.groupby('Title')['Rating'].mean()

plt.figure(figsize=(12, 6))
avg_rating_per_book.plot(kind='bar', color='salmon')
plt.title("Average Rating per Book")
plt.xlabel("Title")
plt.ylabel("Average Rating")
plt.show()

# Distribution of Price
plt.figure(figsize=(10, 6))
sns.histplot(final_df['Price'], bins=30, kde=True)
plt.title('Distribution of Book Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Distribution of Rating
plt.figure(figsize=(10, 6))
sns.histplot(final_df['Rating'], bins=30, kde=True)
plt.title('Distribution of Book Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

# Distribution of Number of Checkouts
plt.figure(figsize=(10, 6))
sns.histplot(x=final_df['Number of Checkouts'], bins=30, kde=True)
plt.title('Distribution of Number of Checkouts')
plt.xlabel('Number of Checkouts')
plt.ylabel('Frequency')
plt.show()

# Count plot for Genre
plt.figure(figsize=(12, 8))
sns.countplot(y='Genre', data=final_df, order=final_df['Genre'].value_counts().index)
plt.title('Count of Books by Genre')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.show()

genre_counts = final_df['Genre'].value_counts() #counting each genre
plt.figure(figsize=(8, 8))
plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Genre Popularity")
plt.show()

# Count plot for Format
plt.figure(figsize=(12, 8))
sns.countplot(y='Format', data=final_df, order=final_df['Format'].value_counts().index)
plt.title('Count of Books by Format')
plt.xlabel('Count')
plt.ylabel('Format')
plt.show()

books_per_author = final_df['Author'].value_counts()

plt.figure(figsize=(10, 6))
books_per_author.plot(kind='bar', color='skyblue')
plt.title("Number of Books per Author")
plt.xlabel("Author")
plt.ylabel("Number of Books")
plt.show()

book_count = final_df.groupby('Author')['Title'].count().reset_index().sort_values('Title', ascending=False).head(20).set_index('Author')

plt.figure(figsize=(15, 10))
sns.barplot(x=book_count['Title'], y=book_count.index, palette='inferno')
plt.title("Top 20 Authors with the Most Number of Books")
plt.xlabel("Total Number of Books")
plt.ylabel("Author")
plt.show()

top_authors_sales = final_df.groupby('Author')['Number of Checkouts'].sum().reset_index()
top_authors_sales = top_authors_sales.sort_values(by='Number of Checkouts', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_authors_sales, x='Author', y='Number of Checkouts', palette="Blues_d")
plt.title('Top Authors by Number of Checkouts')
plt.xlabel('Author')
plt.ylabel('Total Checkouts')
plt.xticks(rotation=45)
plt.show()

# Scatter plot for Price vs. Number of Checkouts
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Price', y='Number of Checkouts', data=final_df)
plt.title('Price vs. Number of Checkouts')
plt.xlabel('Price')
plt.ylabel('Number of Checkouts')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=final_df, x='Rating', y='Number of Checkouts', hue='Genre')
plt.title('Relationship Between Ratings and Number of Checkouts')
plt.xlabel('Rating')
plt.ylabel('Number of Checkouts')
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Box plot for Rating by Genre
plt.figure(figsize=(12, 8))
sns.boxplot(x='Genre', y='Rating', data=final_df)
plt.xticks(rotation=45)
plt.title('Box Plot of Ratings by Genre')
plt.xlabel('Genre')
plt.ylabel('Rating')
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x='Format', y='Rating', data=final_df, palette='pastel')
plt.title('Boxplot of Ratings by Format')
plt.xlabel('Format')
plt.ylabel('Rating')
plt.xticks(rotation=45)
plt.show()

# Grouping by CheckoutMonth to find total checkouts per month
monthly_checkouts = final_df.groupby('CheckoutMonth')['Number of Checkouts'].sum().reset_index()

# Time series plot for monthly checkouts
plt.figure(figsize=(10, 6))
sns.lineplot(x='CheckoutMonth', y='Number of Checkouts', data=monthly_checkouts)
plt.title('Total Number of Checkouts by Month')
plt.xlabel('Checkout Month')
plt.ylabel('Total Number of Checkouts')
plt.xticks(range(1, 13))  # Assuming months are from 1 to 12
plt.show()

plt.figure(figsize=(12, 6))
sales_data['ISBN'].value_counts().hist(bins=30)
plt.title('Distribution of Sales by ISBN')
plt.xlabel('Number of Sales')
plt.ylabel('Frequency')
plt.show()

sales_over_time = sales_data.groupby('Sale Date').size()

plt.figure(figsize=(12, 6))
sales_over_time.plot()
plt.title('Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Sales')
plt.show()

df = final_df.copy()

df.head()

df = df[['BookID', 'Title', 'Author', 'Genre', 'CheckoutMonth','Number of Checkouts', 'ISBN', 'Format','Pages','Price', 'Rating', 'UserID']]
df.head()h

def recommend_popular_by_checkouts(top_n=10):
    popular_books = df.groupby('Title')['Number of Checkouts'].sum().sort_values(ascending=False).head(top_n)
    return popular_books.reset_index()

print("Popular Books by Checkouts:")
print(recommend_popular_by_checkouts())

def recommend_popular_by_ratings(top_n=10):
    popular_books = df.groupby('Title')['Rating'].mean().sort_values(ascending=False).head(top_n)
    return popular_books.reset_index()

print("Popular Books by Ratings:")
print(recommend_popular_by_ratings())

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

scaler = StandardScaler()
le = LabelEncoder()

df.columns

df[['Number of Checkouts','Pages','Price']] = scaler.fit_transform(df[['Number of Checkouts','Pages','Price']])

df['Genre'] = le.fit_transform(df['Genre'])

df['Format'] = le.fit_transform(df['Format'])

df.head()

features = df[['Genre','Number of Checkouts','Format','Pages','Price','Rating']]

pca = PCA()
pca.fit(features)

pca.explained_variance_ratio_

sns.set_style('whitegrid')
plt.figure(figsize=(12,9))
plt.plot(range(1,len(pca.explained_variance_ratio_)+1), pca.explained_variance_ratio_.cumsum(),marker='o', linestyle='--')
plt.title("Explained Variance by Components")
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.show()

pca = PCA(n_components=4)
pca_result=pca.fit_transform(features)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(pca_result)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,8))
plt.plot(range(1,11), wcss, marker='o', linestyle='--')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.show()

kmeans = KMeans(n_clusters=4)
df['Cluster'] = kmeans.fit_predict(pca_result)

df.head()

def recommend_books(book_title, top_n=10):
    if book_title not in df['Title'].values:
        return "Book not found."

    cluster_label = df.loc[df['Title'] == book_title]['Cluster'].values[0]
    recommended_books = df[(df['Cluster'] == cluster_label) & (df['Title'] != book_title)]

    if recommended_books.empty:
        return "No similar books found in this cluster."

    recommended_titles = recommended_books[['Title','Author']].drop_duplicates().reset_index(drop=True)

    # for title in recommended_titles:
    #     print(title)

    return recommended_titles[:top_n]

print("Recommendations for 'Nothing But Capers':")
recommend_books('Nothing But Capers')

from sklearn.metrics.pairwise import cosine_similarity

user_item_matrix = df.pivot_table(index='UserID', columns='Title', values='Rating').fillna(0)

# Compute cosine similarity between users
user_similarity_matrix = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)

def recommend_books_collaborative_on_user(user_id, top_n=10):
    if user_id not in user_similarity_df.index:
        return ["User not found."]

    similar_users = user_similarity_df[user_id].sort_values(ascending=False).iloc[1:top_n + 1]
    recommended_books_indices = user_item_matrix.loc[similar_users.index].mean(axis=0).sort_values(ascending=False).index.tolist()

    return recommended_books_indices[:top_n]

recommend_books_collaborative_on_user(53365.)

# Create a pivot table with 'Title' as the index and 'UserID' as the columns
book_user_matrix = df.pivot_table(index='Title', columns='UserID', values='Rating').fillna(0)

# Compute cosine similarity between books
book_similarity_matrix = cosine_similarity(book_user_matrix)
book_similarity_df = pd.DataFrame(book_similarity_matrix, index=book_user_matrix.index, columns=book_user_matrix.index)

def recommend_books_collaborative_on_books(book_title, top_n=10):
    if book_title not in book_similarity_df.index:
        return ["Book not found."]

    # Find the most similar books
    similar_books = book_similarity_df[book_title].sort_values(ascending=False).iloc[1:top_n + 1]
    return similar_books.index.tolist()

recommend_books_collaborative_on_books('Post Alley')

import streamlit as st # Streamlit UI
st.title("Book Recommendation System")

# Option for Popular Books
st.header("Popular Books by Checkout")
if st.button('Show Popular Checkouts'):
    st.write(recommend_popular_by_checkouts())

st.header("Popular Books by Ratings")
if st.button('Show Popular Books by Ratings'):
    st.write(recommend_popular_by_ratings())


# Option for Book-based Recommendation using Clustering
st.header("Recommend Books Based on a Title")
book_title = st.text_input("Enter the title of a book:")

if st.button('Recommend Similar Books by Title'):
    if book_title:
        recommended = recommend_books(book_title)
        st.write(recommended)


st.header("Recommend Books Based on User Similarity")
UserId = st.text_input("Enter the title of a book:")

if st.button('Recommend Books for User'):
    if UserId:
        recommended = recommend_books_collaborative_on_user(UserId)
        st.write(recommended)
    else:
        st.write("Please enter a book title.")



# Option for Association-Based Recommendation
st.header("Recommend Books Based on Association Rules")
book_title_association = st.text_input("Enter book title for association-based recommendation:")
#top_n_association = st.slider('Select number of recommended books', 1, 10, 5, key="top_n_association")
if st.button('Recommend Books by Association Rules recommend_books_collaborative_on_books'):
    if book_title_association:
        recommended_books_association = recommend_books_collaborative_on_books(book_title_association)
        st.write(recommended_books_association)
    else:
        st.write("Please enter a book title.")

streamlit run app.ipynb

!pip3 install streamlit

!streamlit run app