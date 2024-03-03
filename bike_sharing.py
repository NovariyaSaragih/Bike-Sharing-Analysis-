import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
hour_data = pd.read_csv('D:\SEMESTER 6\proyek_analisis_data_dicoding\dashboard\hour.csv')
day_data = pd.read_csv('D:\SEMESTER 6\proyek_analisis_data_dicoding\dashboard\day.csv')

# Pertanyaan 1
def pertanyaan_1():
    avg_rentals_workingday = day_data[day_data['workingday'] == 1]['cnt'].mean()
    avg_rentals_holiday = day_data[day_data['workingday'] == 0]['cnt'].mean()

    fig, ax = plt.subplots()
    ax.bar(['Hari Kerja', 'Hari Libur'], [avg_rentals_workingday, avg_rentals_holiday])
    ax.set_title('Rata-rata Jumlah Peminjaman Sepeda\nAntara Hari Kerja dan Hari Libur\n')
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')

    st.pyplot(fig)

# Pertanyaan 2
def pertanyaan_2():
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    sns.lineplot(ax=axes[0], x='hour', y='cnt', data=hour_data, color='blue')
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

    st.pyplot(fig)

# Pertanyaan 3
def pertanyaan_3():
    hourly_usage_weekday = hour_data[hour_data['workingday'] == 1].groupby('hour')['cnt'].mean()
    hourly_usage_weekend = hour_data[hour_data['workingday'] == 0].groupby('hour')['cnt'].mean()

    fig, ax = plt.subplots()
    ax.plot(hourly_usage_weekday.index, hourly_usage_weekday.values, label='Hari Kerja')
    ax.plot(hourly_usage_weekend.index, hourly_usage_weekend.values, label='Akhir Pekan')
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Rata-rata Jumlah Sepeda yang Dipinjam')
    ax.set_title('Perbedaan Penggunaan Sepeda antara di Jam Hari Kerja dan Akhir Pekan\n')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# Main program
def main():
    st.title('Dashboard Analisis Data Sepeda')

    menu = ['Pertanyaan 1', 'Pertanyaan 2', 'Pertanyaan 3']
    choice = st.sidebar.selectbox('Pilih Pertanyaan', menu)

    if choice == 'Pertanyaan 1':
        pertanyaan_1()
    elif choice == 'Pertanyaan 2':
        pertanyaan_2()
    elif choice == 'Pertanyaan 3':
        pertanyaan_3()

if __name__ == '__main__':
    main()
