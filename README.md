# myrecommender
## Kiến trúc xây dựng
![Toàn bộ kiến trúc](imgs/full-diagram.png)

## Raw data
- Dữ liệu raw của tập dữ liệu MovieLens được lưu trong [folder](data). Tập dữ liệu sử dụng để thực nghiệm là `movielens_1M`
- Dữ liệu được crawler, dùng python để download trong thư mực [crawler](crawler).
- Chuyển dữ liệu về dạng `.csv` và lưu vào folder [enrich](enrich)
- Thêm tên các cột cho data: userID, itemID, rating, timestamp, ... (chạy file [changetocsv](notebooks\changetocsv.ipynb) để thực thi)
## Enrich data
### Dữ liệu được tiền xử lý theo luồng sau:
- Về phương pháp content_based similarity: Dữ liệu được thu thập thêm được lưu ở file [movies_tags](raw/ml-1m-movies_tags.txt) có thêm thông tin về các mục của movies. Dữ liệu này sau khi qua file /notebooks/content_base.ipynb sẽ chuyển dữ liệu về dạng vector similarity, các vector này giúp ta lấy được thông tin các movies nào là tương tự nhau, từ đó xếp hạng độ tương đồng giữa các movies và giúp người dùng tìm được một bộ phim tương tự với phim mà mình đã xem.

- Về phương pháp LightGCN: Sử dụng thuật toán đã build từ trước của microsoft, thuật toán này sẽ biến các node userID và movieID thành các vector embeddings, các vector này sẽ được cập nhập sau mỗi lần chạy bằng cách cộng tổng các vector emddings với các userID và movieID được kết nối với nó. Các vetor này được cập nhật ở mỗi lớp và sau đó cộng tổng có trọng số các lớp này lại với nhau. Sau đó dùng hàm độ lỗi để tối ưu thuật toán.

### Làm giàu dữ liệu
- Tạo dữ liệu giả lập streaming bằng file [createStreamingdata](notebooks/createStreamingdata.ipynb) -> dữ liệu được tạo ra sẽ lưu trong folder raw chờ để đưa lên Azure Blob Storage


## Process
- Sau khi chạy file [unionData](unionData.ipynb) sẽ lưu các ratings mới bằng cách lấy rating của ngày trước đó + ratings mới được tạo ra bước làm giàu dữ liệu. Ta thu dược folder mới chứa dữ liệu `ratings.csv` mới. Phục vụ cho mục đích huấn luyện

## Content-based Similarity 
Chạy file /notebooks/content_base.ipynb để lấy ra kết quả tính toán độ tương đồng giữa các movies, dựa trên tag movies mà nhóm thu thập được trên một dữ liệu khác. Link nguồn dữ liệu [source](https://github.com/xuChenSJTU/Movielens-1m-10m-20m-with-tags)

## Deep Learning & Recommendation Systems

### Deep Learning
Dùng model LightGCN để xây dựng hệ khuyến nghị
GCNs có thể được sử dụng để mã hóa tín hiệu tương tác trong các embeddings. Các mục đã tương tác có thể được coi là đặc điểm của người dùng, vì chúng cung cấp bằng chứng trực tiếp về sở thích của người dùng. Tương tự, người dùng tiêu thụ một mục có thể được xem xét như là đặc điểm của mục và được sử dụng để đo lường sự tương đồng hợp tác giữa hai mục. Một cách tự nhiên để tích hợp tín hiệu tương tác vào nhúng là bằng cách khai thác kết nối cấp cao từ tương tác người dùng-mục.

<img src="https://recodatasets.z20.web.core.windows.net/images/High_order_connectivity.png" width=500 style="display:block; margin-left:auto; margin-right:auto;">

Để làm rõ hơn về phương pháp LigtGCN, ta cần quan tâm đến hai thiết kế chính: tổng hợp vùng lân cận trong lớp và kết hợp giữa các lớp.
-	Trong mỗi lớp, đối với mỗi người trong đồ thị, tính toán việc cập nhật embeddings của nó dưới dạng tổng trọng số của các embeddings từ tất cả các mục lân cận của nó (phim) và ngược lại

-	Khi kết hợp lớp, thay vì lấy embeddings của lớp K cuối cùng, LightGCN tính tổng có trọng số của các phần nhúng ở các lớp khác nhau 


<img src="https://recodatasets.z20.web.core.windows.net/images/lightGCN-model.jpg" width=600 style="display:block; margin-left:auto; margin-right:auto;">

Mô hình dự đoán được định nghĩa là đo lường sự tương đồng giữa người dùng và phim, do đó cho phép dự đoán khả năng người dùng thích bộ phim đó.


Để đào tạo mô hình, sử dụng hàm độ lỗi  Bayesian Personalized Ranking (BPR) khuyến khích dự đoán về một mục nhập gần kề cao hơn so với các mục không gần kề của nó:


## Curated
- Để tổng hợp dữ liệu, chạy file [toCurated](toCurated.ipynb) để lưu dữ liệu bằng cách merge dữ liệu user, dữ liệu movies và dữ liệu ratings lại với nhau.

## Visualize
### Dashboard ngày 8-12-2023
![Alt text](imgs/08-12-2023.png)
### Dashboard ngày 9-12-2023
![Alt text](imgs/09-12-2023.png)
### Dashboard ngày 10-12-2023
![Alt text](imgs/10-12-2023.png)

## Website Demo
- Sản phẩm được xây dựng, deploy trên streamlit
- Link sản phẩm demo: [https://my-movies-recommendation-system.streamlit.app/](https://my-movies-recommendation-system.streamlit.app/)

# Tổng kết luồng xử lý
- Mỗi ngày, dữ liệu trên hệ thóng sẽ cập nhật mới về bằng Synapse Analytics
- Chạy file `uninonData.ipynb` để gộp dữ liệu
- Chạy file `lightgcn.ipynb` để thực hiện thuật toán lấy kết quả khuyến nghị
- Chạy file `toCurated.ipynb` để lấy kết quả dữ liệu cuối cùng
- Dùng Synapse Analytics để tiếp tục vận hành hệ thống đã xây dựng
- Dùng PowerBI để truy cập dữ liệu mới để trực quan, tạo bảng Dashboard mới
- Dùng CosMosDB để lưu trữ kết quả và xây dựng Web

