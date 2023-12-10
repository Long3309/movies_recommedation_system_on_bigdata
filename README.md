# myrecommender
## Kiến trúc xây dựng
![Toàn bộ kiến trúc](imgs/full-diagram.png)

## Raw data
- Dữ liệu raw của tập dữ liệu MovieLens được lưu trong [folder](data). Tập dữ liệu sử dụng để thực nghiệm là `movielens_1M`
- Dữ liệu được crawler, dùng python để download trong thư mực [crawler](crawler).

## Enrich data
### Dữ liệu được tiền xử lý theo luồng sau:
- Chuyển dữ liệu về dạng `.csv` và lưu vào folder [enrich](enrich)
- Thêm tên các cột cho data: userID, itemID, rating, timestamp, ... (chạy file [changetocsv](notebooks\changetocsv.ipynb) để thực thi)


### Làm giàu dữ liệu
- Tạo dữ liệu giả lập streaming bằng file [createStreamingdata](notebooks/createStreamingdata.ipynb) -> dữ liệu được tạo ra sẽ lưu trong folder raw chờ để đưa lên Azure Blob Storage


## Process
- Sau khi chạy file [unionData](unionData.ipynb) sẽ lưu các ratings mới bằng cách lấy rating của ngày trước đó + ratings mới được tạo ra bước làm giàu dữ liệu. Ta thu dược folder mới chứa dữ liệu `ratings.csv` mới. Phục vụ cho mục đích huấn luyện


## Deep Learning & Recommendation Systems
### KNN
Sử dụng KNN để thực hiện xây dựng hệ khuyến nghị

### Deep Learning
Dùng model LightGCN để xây dựng hệ khuyến nghị
GCNs có thể được sử dụng để mã hóa tín hiệu tương tác trong các embeddings. Các mục đã tương tác có thể được coi là đặc điểm của người dùng, vì chúng cung cấp bằng chứng trực tiếp về sở thích của người dùng. Tương tự, người dùng tiêu thụ một mục có thể được xem xét như là đặc điểm của mục và được sử dụng để đo lường sự tương đồng hợp tác giữa hai mục. Một cách tự nhiên để tích hợp tín hiệu tương tác vào nhúng là bằng cách khai thác kết nối cấp cao từ tương tác người dùng-mục.
<img src="https://recodatasets.z20.web.core.windows.net/images/High_order_connectivity.png" width=500 style="display:block; margin-left:auto; margin-right:auto;">
Để làm rõ hơn về phương pháp LigtGCN, ta cần quan tâm đến hai thiết kế chính: tổng hợp vùng lân cận trong lớp và kết hợp giữa các lớp.
-	Trong mỗi lớp, đối với mỗi người trong đồ thị, tính toán việc cập nhật embeddings của nó dưới dạng tổng trọng số của các embeddings từ tất cả các mục lân cận của nó (phim) và ngược lại
$$
\begin{array}{l}
\mathbf{e}_{u}^{(k+1)}=\sum_{i \in \mathcal{N}_{u}} \frac{1}{\sqrt{\left|\mathcal{N}_{u}\right|} \sqrt{\left|\mathcal{N}_{i}\right|}} \mathbf{e}_{i}^{(k)} \\
\mathbf{e}_{i}^{(k+1)}=\sum_{u \in \mathcal{N}_{i}} \frac{1}{\sqrt{\left|\mathcal{N}_{i}\right|} \sqrt{\left|\mathcal{N}_{u}\right|}} \mathbf{e}_{u}^{(k)}
\end{array}
$$
-	Khi kết hợp lớp, thay vì lấy embeddings của lớp K cuối cùng, LightGCN tính tổng có trọng số của các phần nhúng ở các lớp khác nhau 
$$
\mathbf{e}_{u}=\sum_{k=0}^{K} \alpha_{k} \mathbf{e}_{u}^{(k)} ; \quad \mathbf{e}_{i}=\sum_{k=0}^{K} \alpha_{k} \mathbf{e}_{i}^{(k)}
$$
<img src="https://recodatasets.z20.web.core.windows.net/images/lightGCN-model.jpg" width=600 style="display:block; margin-left:auto; margin-right:auto;">

Mô hình dự đoán được định nghĩa là đo lường sự tương đồng giữa người dùng và phim, do đó cho phép dự đoán khả năng người dùng thích bộ phim đó.

$$
\hat{y}_{u i}=\mathbf{e}_{u}^{T} \mathbf{e}_{i}
$$
Để đào tạo mô hình, sử dụng hàm độ lỗi  Bayesian Personalized Ranking (BPR) khuyến khích dự đoán về một mục nhập gần kề cao hơn so với các mục không gần kề của nó:
$$
L_{B P R}=-\sum_{u=1}^{M} \sum_{i \in \mathcal{N}_{u}} \sum_{j \notin \mathcal{N}_{u}} \ln \sigma\left(\hat{y}_{u i}-\hat{y}_{u j}\right)+\lambda\left\|\mathbf{E}^{(0)}\right\|^{2}
$$

## Curated
- Để tổng hợp dữ liệu, chạy file [toCurated](toCurated.ipynb) để lưu dữ liệu bằng cách merge dữ liệu user, dữ liệu movies và dữ liệu ratings lại với nhau.

## Visualize
### Dashboard ngày 8-12-2023
![Alt text](imgs\08-12-2023.png)
### Dashboard ngày 9-12-2023
![Alt text](imgs\09-12-2023.png)
### Dashboard ngày 10-12-2023
![Alt text](imgs\10-12-2023.png)


# Tổng kết luồng xử lý
- Mỗi ngày, dữ liệu trên hệ thóng sẽ cập nhật mới về bằng Synapse Analytics
- Chạy file `uninonData.ipynb` để gộp dữ liệu
- Chạy file `lightgcn.ipynb` để thực hiện thuật toán lấy kết quả khuyến nghị
- Chạy file `toCurated.ipynb` để lấy kết quả dữ liệu cuối cùng
- Dùng Synapse Analytics để tiếp tục vận hành hệ thống đã xây dựng
- Dùng PowerBI để truy cập dữ liệu mới để trực quan, tạo bảng Dashboard mới
- Dùng CosMosDB để lưu trữ kết quả và xây dựng Web
