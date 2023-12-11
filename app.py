import streamlit as st 
import requests
import pandas as pd
import pymongo
import numpy as np
from datetime import datetime, timedelta

import streamlit.components.v1 as components

st.set_page_config(page_title="Movie Web", layout="wide")
st.header("Sản phẩm demo Web Application")
poster_data = pd.read_csv("./crawler/movie_poster.csv", names=["itemID", "url"])

# Hàm liên kết với mongodb
def get_collection(connection_str):
    myclient = pymongo.MongoClient(connection_str)
    mydb = myclient["result"]
    mycol = mydb["10-12-2023"]
    return mycol
# Lấy ra top15 movies được xem nhiều nhất
def get_topmovies():
    # date = datetime.now().strftime("%d-%m-%Y")
    ratings = pd.read_csv(f"./enrich/10-12-2023/ratings.csv")
    today = datetime(2023, 12, 10)
    ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
    start_date = today - timedelta(days=30)
    filtered_df = ratings[(ratings['timestamp'] >= start_date) & (ratings['timestamp'] <= today)]
    item_counts  = filtered_df.groupby(by = "itemID").size()
    top_items = item_counts.nlargest(15)
    top_items = top_items.index.to_list()
    return top_items
movies = pd.read_csv("./enrich/movies.csv")
# Hàm lấy hình ảnh - bổ sung thêm title các thứ
@st.cache_data()
def fetch_poster(movie_ids):
    # title = movies.iloc[movie_id].title
    list_url = list()
    for movieid in movie_ids:
        try:
            url = str(poster_data[poster_data["itemID"] == movieid]["url"].values[0])
            list_url.append(url)
        except:
            continue
    return list_url


@st.cache_data()
def get_resources():
    # Load ma trận tương đồng (similarity matrix)
    similarity = np.load("similarity_matrix.npy")
    return similarity

# Duyệt qua từng dòng trên collection dựa trên userID, duyệt qua các movieID trong list 10 movieID
@st.cache_data()
def get_movies(user):
    data = res_collection.find({"userID": user})
    for row in data:
        return row["itemIDs"]

st.subheader("Top movies có nhiều lượt xem nhất trong 30 ngày gần đây")
top_items = get_topmovies()
imageCarouselComponent1 = components.declare_component("image-carousel-component", path="frontend/public")
imageCarouselComponent1(imageUrls=fetch_poster(top_items), height=200)

# Nhập userID
st.subheader("Phim phù hợp với người dùng")

connection_str = "mongodb://longnguyenuit:ZkhrACfJflUhurRi1xUBFVLXMxNQrn2czSp5yHvomR4pvzmRPJX4niIdQT0FxdJCRVUtTx0eUkv4ACDbiTmXsQ%3D%3D@longnguyenuit.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@longnguyenuit@"
res_collection = get_collection(connection_str)

similarity = get_resources()
userID = st.number_input("Nhập vào id người dùng: ", min_value=1, max_value=6040, step=1)
imageCarouselComponent1 = components.declare_component("image-carousel-component", path="frontend/public")
imageCarouselComponent1(imageUrls=fetch_poster(get_movies(userID)), height=200)

st.subheader("Phim tương tự nội dung bạn muốn xem")
movie_title = st.selectbox("Chọn phim bạn muốn xem", options=movies["title"].tolist())

columns =st.columns(10)
def fetch_poster_2(movie_id):
    title = movies.iloc[movie_id].title
    try:
        url = str(poster_data[poster_data["itemID"] == movie_id]["url"].values[0])
        return url, title
    except:
        return title
def show_result(title):
    i = 0
    for movieID in content_based_recommendation(title):
        try:
            url , title = fetch_poster_2(movieID)
            with columns[i]:
                st.write(title)
                st.image(url)
        except:
            title = fetch_poster_2(movieID)
            with columns[i]:
                st.write(title)
        i = i + 1
def content_based_recommendation(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda vector:vector[1])
    list_movieID = list()
    for i in distance[1:11]:
        # print(movies.iloc[i[0]].title)
        list_movieID.append(i[0])
    return list_movieID
                
show_result(movie_title)


