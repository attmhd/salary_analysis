import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# Load dataset
def load_data():
    file_path = './dataset/'  # Pastikan file ini berada di lokasi yang sama dengan aplikasi Streamlit
    data = pd.read_csv(file_path)
    data['Salary Growth (%)'] = ((data['Mid-Career Median Salary'] - data['Starting Median Salary']) /
                                  data['Starting Median Salary']) * 100
    return data

data = load_data()

# Sidebar configuration
st.sidebar.title("Salary Analysis by College Major")
option = st.sidebar.selectbox("Select Analysis", ["Top Majors by Growth", "Clustering"])

if option == "Top Majors by Growth":
    st.title("Top Majors with Highest Salary Growth")
    top_majors = data[['Undergraduate Major', 'Salary Growth (%)']].sort_values(by='Salary Growth (%)', ascending=False)
    st.dataframe(top_majors.head(10))
    st.write("The table above shows the top 10 majors with the highest percentage growth in salary.")

elif option == "Clustering":
    st.title("Clustering Majors by Salary Metrics")

    # Clustering data
    clustering_data = data[['Starting Median Salary', 'Mid-Career Median Salary', 'Salary Growth (%)']].dropna()
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(clustering_data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(normalized_data)

    data['Cluster'] = -1  # Untuk menangani NaN
    data.loc[clustering_data.index, 'Cluster'] = clusters

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.scatter(normalized_data[:, 0], normalized_data[:, 1], c=clusters, cmap='viridis', alpha=0.7)
    plt.colorbar(label='Cluster')
    plt.xlabel('Starting Median Salary (Normalized)')
    plt.ylabel('Mid-Career Median Salary (Normalized)')
    plt.title('Clustering of College Majors by Salary Metrics')
    st.pyplot(plt)

    # Display clustered data
    st.write("Clustered data sample:")
    st.dataframe(data[['Undergraduate Major', 'Cluster', 'Starting Median Salary', 'Mid-Career Median Salary', 'Salary Growth (%)']].head(10))