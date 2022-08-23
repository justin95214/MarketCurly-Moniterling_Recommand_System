import numpy as np
import matplotlib.pyplot as plt

# -2 ~ 2 사이 균등분포 100개 추출
x1 = (np.random.random(100) - 0.5) * 4
y1 = (np.random.random(100) - 0.5) * 4

# 평균 0, 표준편차 1 정규분포 100개 추출
x2 = np.random.randn(100)
y2 = np.random.randn(100)

plt.scatter(x1, y1, color = 'purple', alpha = 0.6, label = 'uniform')
plt.scatter(x2, y2, color = 'orange', alpha = 0.7, label = 'normal')

plt.legend()
plt.show()