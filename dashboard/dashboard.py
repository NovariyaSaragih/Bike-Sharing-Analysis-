import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
hour = pd.read_csv('D:/SEMESTER 6/proyek_analisis_data_dicoding/dashboard/hour.csv')
day = pd.read_csv('D:/SEMESTER 6/proyek_analisis_data_dicoding/dashboard/day.csv')

# Merge Data
combined_data = pd.concat([hour, day], axis=0)

# Set title
st.title('Dashboard Bike Sharing Dataset')

# Sidebar
st.sidebar.title('Pertanyaan')
selected_question = st.sidebar.radio('Pilih Pertanyaan:', ('Perbedaan Jumlah Peminjaman Sepeda Antara Hari Kerja dan Hari Libur', 'Pola Ketersediaan Sepeda Berdasarkan Jam, Hari, dan Musim', 'Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan Akhir Pekan'))

# Answer Question 1
if selected_question == 'Perbedaan Jumlah Peminjaman Sepeda Antara Hari Kerja dan Hari Libur':
    avg_rentals_workingday = day[day['workingday'] == 1]['cnt'].mean()
    avg_rentals_holiday = day[day['workingday'] == 0]['cnt'].mean()
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

# Answer Question 2
elif selected_question == 'Pola Ketersediaan Sepeda Berdasarkan Jam, Hari, dan Musim':
    st.write('### Pola Ketersediaan Sepeda Berdasarkan Jam, Hari, dan Musim')
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Plotting ketersediaan sepeda berdasarkan jam
    sns.lineplot(ax=axes[0], x='hr', y='cnt', data=hour, color='blue')
    axes[0].set_title('Pola Ketersediaan Sepeda Berdasarkan Jam')
    axes[0].set_xlabel('Jam (0-23)')
    axes[0].set_ylabel('Jumlah Peminjaman')

    # Plotting ketersediaan sepeda berdasarkan hari
    sns.lineplot(ax=axes[1], x='weekday', y='cnt', data=hour, color='green')
    axes[1].set_title('Pola Ketersediaan Sepeda Berdasarkan Hari')
    axes[1].set_xlabel('Hari (0: Senin - 6: Minggu)')
    axes[1].set_ylabel('Jumlah Peminjaman')

    # Plotting ketersediaan sepeda berdasarkan musim
    sns.lineplot(ax=axes[2], x='season', y='cnt', data=hour, color='red')
    axes[2].set_title('Pola Ketersediaan Sepeda Berdasarkan Musim')
    axes[2].set_xlabel('Musim')
    axes[2].set_ylabel('Jumlah Peminjaman')
    axes[2].set_xticks(hour['season'].unique().tolist())  # Mengatur label musim sesuai data
    axes[2].set_xticklabels(['Musim 1 (Spring)', 'Musim 2 (Summer)', 'Musim 3 (Fall)', 'Musim 4 (Winter)'])  # Mengganti label musim

    st.pyplot(fig)

# Answer Question 3
else:
    st.write('### Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan Akhir Pekan')
    hourly_usage_weekday = hour[hour['workingday'] == 1].groupby('hr')['cnt'].mean()
    hourly_usage_weekend = hour[hour['workingday'] == 0].groupby('hr')['cnt'].mean()

    fig, ax = plt.subplots()
    ax.plot(hourly_usage_weekday.index, hourly_usage_weekday.values, label='Hari Kerja')
    ax.plot(hourly_usage_weekend.index, hourly_usage_weekend.values, label='Akhir Pekan')
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Sepeda yang Dipinjam')
    ax.set_title('Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan Akhir Pekan')
    ax.legend()
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)
