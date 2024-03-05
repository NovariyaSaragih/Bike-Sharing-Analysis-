import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
hour_data = pd.read_csv('hour.csv')
day_data = pd.read_csv('day.csv')

# Fungsi untuk perhitungan interval kepercayaan
def calculate_confidence_interval(data):
    mean = np.mean(data)
    std_dev = np.std(data)
    n = len(data)
    z = 1.96  # Nilai z untuk interval kepercayaan 95%
    margin_of_error = z * (std_dev / np.sqrt(n))
    lower_bound = mean - margin_of_error
    upper_bound = mean + margin_of_error
    return lower_bound, upper_bound
    
# Set title
st.title('Dashboard Bike Sharing Dataset')

# Visualisasi untuk pertanyaan 1: Rata-rata Jumlah Peminjaman Sepeda Antara Hari Kerja dan Hari Libur
avg_rentals_workingday = day_data[day_data['workingday'] == 1]['cnt'].mean()
avg_rentals_holiday = day_data[day_data['workingday'] == 0]['cnt'].mean()

# Menampilkan plot menggunakan Streamlit
st.bar_chart({'Hari Kerja': avg_rentals_workingday, 'Hari Libur': avg_rentals_holiday})

# Visualisasi untuk pertanyaan 2: Pola Ketersediaan Sepeda Berdasarkan Jam, Hari, dan Musim
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

sns.lineplot(ax=axes[0], x='hr', y='cnt', data=hour_data, color='blue')
axes[0].set_title('Pola Ketersediaan Sepeda Berdasarkan Jam\n')
axes[0].set_xlabel('Jam (0-23)')
axes[0].set_ylabel('Jumlah Peminjaman')

sns.lineplot(ax=axes[1], x='weekday', y='cnt', data=hour_data, color='green')
axes[1].set_title('Pola Ketersediaan Sepeda Berdasarkan Hari\n')
axes[1].set_xlabel('Hari (0: Senin - 6: Minggu)')
axes[1].set_ylabel('Jumlah Peminjaman')

sns.lineplot(ax=axes[2], x='season', y='cnt', data=hour_data, color='red')
axes[2].set_title('Pola Ketersediaan Sepeda Berdasarkan Musim\n')
axes[2].set_xlabel('Musim')
axes[2].set_ylabel('Jumlah Peminjaman')
axes[2].set_xticks(hour_data['season'].unique())
axes[2].set_xticklabels(['Musim 1 (Spring)', 'Musim 2 (Summer)', 'Musim 3 (Fall)', 'Musim 4 (Winter)'])

# Menampilkan plot menggunakan st.pyplot
st.pyplot(fig)

# Visualisasi untuk pertanyaan 3: Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan Akhir Pekan dengan Interval Kepercayaan
hourly_usage_weekday = hour_data[hour_data['workingday'] == 1].groupby('hr')['cnt'].mean()
hourly_usage_weekend = hour_data[hour_data['workingday'] == 0].groupby('hr')['cnt'].mean()

lower_bound_weekday, upper_bound_weekday = calculate_confidence_interval(hourly_usage_weekday)
lower_bound_weekend, upper_bound_weekend = calculate_confidence_interval(hourly_usage_weekend)

plt.plot(hourly_usage_weekday.index, hourly_usage_weekday.values, label='Hari Kerja')
plt.fill_between(hourly_usage_weekday.index, lower_bound_weekday, upper_bound_weekday, alpha=0.2)
plt.plot(hourly_usage_weekend.index, hourly_usage_weekend.values, label='Akhir Pekan')
plt.fill_between(hourly_usage_weekend.index, lower_bound_weekend, upper_bound_weekend, alpha=0.2)
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Rata-rata Jumlah Sepeda yang Dipinjam')
plt.title('Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan Akhir Pekan\n')
plt.legend()
plt.xticks(range(0, 24))
plt.grid(True)

# Menampilkan plot menggunakan st.pyplot
st.pyplot()
