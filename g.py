#coding:utf-8
import matplotlib.pyplot as plt

price = [100, 250, 380, 500, 700]
number = [1, 2, 3, 4, 5]

# �O���t������
plt.plot(price, number)

# �O���t�̃^�C�g��
plt.title("price / number")

# x���̃��x��
plt.xlabel("price")

# y���̃��x��
plt.ylabel("number")

# �\������
plt.show()