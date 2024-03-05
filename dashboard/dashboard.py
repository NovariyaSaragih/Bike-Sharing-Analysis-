import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set option to disable the warning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load data
hour_data = pd.read_csv('./dataset/hour.csv')
day_data = pd.read_csv('./dataset/day.csv')

# Informasi Biodata Pribadi
st.sidebar.title('Welcome To My Dashboard')
st.sidebar.title('Name: Novariya Br Saragih')
st.sidebar.title('LinkedIn: [Novariya Saragih](https://www.linkedin.com/in/novariyasaragih/)')
st.sidebar.title('GitHub: [Novariya Saragih](https://github.com/NovariyaSaragih/Bike-Sharing-Analysis-.git)')
st.sidebar.title('Email: novariya.saragih15@gmail.com')

# Function to visualize rentals difference
def visualize_rentals_difference():
    avg_rentals_workingday = day_data[day_data['workingday'] == 1]['cnt'].mean()
    avg_rentals_holiday = day_data[day_data['workingday'] == 0]['cnt'].mean()
    diff_rentals = avg_rentals_workingday - avg_rentals_holiday
    
    fig, ax = plt.subplots()
    ax.bar(['Hari Kerja', 'Hari Libur'], [avg_rentals_workingday, avg_rentals_holiday])
    ax.set_title('Rata-rata Jumlah Peminjaman Sepeda\nAntara Hari Kerja dan Hari Libur\n')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
        
    st.pyplot(fig)
    st.write('### Perbedaan Jumlah Peminjaman Sepeda Antara Hari Kerja dan Hari Libur')
    st.write(f'Rata-rata jumlah peminjaman sepeda pada hari kerja: {avg_rentals_workingday:,}')
    st.write(f'Rata-rata jumlah peminjaman sepeda pada hari libur: {avg_rentals_holiday:,}')
    st.write(f'Perbedaan jumlah peminjaman sepeda antara hari kerja dan hari libur: {diff_rentals:,}')


# Analisis tren harian
plt.figure(figsize=(12, 6))
plt.plot(day_data['dteday'], day_data['cnt'], marker='o', linestyle='-')
plt.title('Tren Jumlah Peminjaman Sepeda Harian')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah Peminjaman')
plt.xticks(day_data['dteday'][::30], rotation=45)
plt.tight_layout()
plt.show()


# Pertanyaan 2: Pola Ketersediaan Sepeda Berdasarkan Jam, Hari, dan Musim
def visualize_bike_availability_pattern():
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

    plt.tight_layout()
    st.pyplot()

# Pertanyaan 3: Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan di Jam Akhir Pekan
def visualize_usage_difference():
    def calculate_confidence_interval(data):
        mean = np.mean(data)
        std_dev = np.std(data)
        n = len(data)
        z = 1.96  # Nilai z untuk interval kepercayaan 95%
        margin_of_error = z * (std_dev / np.sqrt(n))
        lower_bound = mean - margin_of_error
        upper_bound = mean + margin_of_error
        return lower_bound, upper_bound

    hourly_usage_weekday = hour_data[hour_data['workingday'] == 1].groupby('hr')['cnt'].mean()
    hourly_usage_weekend = hour_data[hour_data['workingday'] == 0].groupby('hr')['cnt'].mean()

    lower_bound_weekday, upper_bound_weekday = calculate_confidence_interval(hourly_usage_weekday)
    lower_bound_weekend, upper_bound_weekend = calculate_confidence_interval(hourly_usage_weekend)

    fig, ax = plt.subplots()
    ax.plot(hourly_usage_weekday.index, hourly_usage_weekday.values, label='Hari Kerja')
    ax.fill_between(hourly_usage_weekday.index, lower_bound_weekday, upper_bound_weekday, alpha=0.2)
    ax.plot(hourly_usage_weekend.index, hourly_usage_weekend.values, label='Akhir Pekan')
    ax.fill_between(hourly_usage_weekend.index, lower_bound_weekend, upper_bound_weekend, alpha=0.2)
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Sepeda yang Dipinjam')
    ax.set_title('Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan di Jam Akhir Pekan')
    ax.legend()
    ax.set_xticks(range(0, 24))
    ax.grid(True)

    st.pyplot()

# Menampilkan dashboard
st.title('Bike Sharing Analysis')

st.header('Pertanyaan 1: Bagaimana Statistika dan Berapa Jumlah Sepeda yang dipinjam pada Hari Kerja dan Hari Libur')
visualize_rentals_difference()

st.header('Pertanyaan 2: Apakah Ada Pola Ketersediaan Sepeda Berdasarkan Jam, Hari, dan Musim')
visualize_bike_availability_pattern()

st.header('Pertanyaan 3: Bagaimana Perbedaan dalam Penggunaan Sepeda antara di Jam Hari Kerja dengan Jam di Akhir Pekan')
visualize_usage_difference()
