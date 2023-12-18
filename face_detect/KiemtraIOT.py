import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Tạo một tập dữ liệu mẫu
np.random.seed(0)
data = np.random.randn(100)  # Chuỗi ngẫu nhiên 100 điểm dữ liệu
# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(data, columns=['Value'])
df.to_csv('data.csv', index=False)
# Xác định giá trị tốt nhất cho p, d, và q (ví dụ sử dụng giá trị đơn giản)
p = 1
d = 1
q = 1
# Xây dựng mô hình ARIMA
model = sm.tsa.ARIMA(df['Value'], order=(p, d, q))
result = model.fit()
# In thông tin về mô hình
print(result.summary())
# Dự báo giá trị tương lai (ví dụ: dự báo 10 bước tiếp theo)
forecast = result.forecast(steps=10)
print(forecast)
# Vẽ biểu đồ chuỗi gốc và dự báo
plt.figure(figsize=(12, 6))
plt.plot(df['Value'], label='Chuỗi gốc')
plt.plot(range(len(df), len(df) + 10), forecast, label='Dự báo')
plt.legend()
plt.title('Dự báo chuỗi thời gian bằng ARIMA')
plt.show()
