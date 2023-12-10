import streamlit as st 
import requests
import pandas as pd
import pymongo
st.set_page_config(page_title="Movie Web", layout="wide")
st.header("Sản phẩm demo Web Application")
poster_data = pd.read_csv("movie_poster.csv", names=["itemID", "url"])

# Hàm liên kết với mongodb

def get_collection(connection_str):
    myclient = pymongo.MongoClient(connection_str)
    mydb = myclient["result"]
    mycol = mydb["06-12-2023"]
    return mycol
# Hàm lấy hình ảnh - bổ sung thêm title các thứ
@st.cache_data()
def fetch_poster(movie_id):
    url = str(poster_data[poster_data["itemID"] == movie_id]["url"].values[0])
    return url
        
# Nhập userID
userID = st.number_input("Nhập vào id người dùng: ", min_value=1, max_value=6040, step=1)
connection_str = "mongodb://longnguyenuit:ZkhrACfJflUhurRi1xUBFVLXMxNQrn2czSp5yHvomR4pvzmRPJX4niIdQT0FxdJCRVUtTx0eUkv4ACDbiTmXsQ%3D%3D@longnguyenuit.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@longnguyenuit@"
res_collection = get_collection(connection_str)
# Duyệt qua từng dòng trên collection dựa trên userID, duyệt qua các movieID trong list 10 movieID
@st.cache_data()
def get_movies(user):
    data = res_collection.find({"userID": user})
    for row in data:
        return row["itemIDs"]

            
# show_res(userID)
button = st.button("Apply")
if button:
    for movieID in get_movies(userID):
        try:
            st.image(fetch_poster(movieID), 200)
        except:
            continue