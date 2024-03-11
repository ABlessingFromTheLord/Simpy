import matplotlib.pyplot as plt
from datetime import date

plt.style.use("ggplot")

fig = plt.figure(figsize=12,8)

plt.barh(y=df["Task"])