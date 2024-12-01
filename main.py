import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Constants
DATA_FILE_PATH = './dataset/salaries_by_college_major.csv'

# Load the dataset
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data.dropna()

# Visualizations
def plot_boxplot(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=data, x='Group', y='Mid-Career Median Salary', palette='Set2', ax=ax)
    ax.set_title('Mid-Career Median Salary by Group', fontsize=14)
    ax.set_xlabel('Group', fontsize=12)
    ax.set_ylabel('Mid-Career Median Salary (USD)', fontsize=12)
    st.pyplot(fig)

def plot_top_majors(data):
    top_majors = data.nlargest(5, 'Mid-Career Median Salary')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_majors, y='Undergraduate Major', x='Mid-Career Median Salary', palette='Blues_r', ax=ax)
    ax.set_title('Top 5 Majors by Mid-Career Median Salary', fontsize=14)
    ax.set_xlabel('Mid-Career Median Salary (USD)', fontsize=12)
    ax.set_ylabel('Undergraduate Major', fontsize=12)
    st.pyplot(fig)

def plot_growth_salary(data):
    growth_salary = data.copy()
    growth_salary['Growth'] = data['Mid-Career Median Salary'] - data['Starting Median Salary']
    top_growth = growth_salary.nlargest(5, 'Growth')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_growth, y='Undergraduate Major', x='Growth', palette='Greens_r', ax=ax)
    ax.set_title('Top 5 Majors by Growth Salary', fontsize=14)
    ax.set_xlabel('Growth Salary (USD)', fontsize=12)
    ax.set_ylabel('Undergraduate Major', fontsize=12)
    st.pyplot(fig)

# Analysis
def display_analysis(data):
    highest_paying_major = data.loc[data['Mid-Career Median Salary'].idxmax()]
    lowest_paying_major = data.loc[data['Mid-Career Median Salary'].idxmin()]

    st.subheader("Highest-Paying Major")
    st.write(f"**Major**: {highest_paying_major['Undergraduate Major']}")
    st.write(f"**Starting Median Salary**: ${highest_paying_major['Starting Median Salary']:,.2f}")
    st.write(f"**Mid-Career Median Salary**: ${highest_paying_major['Mid-Career Median Salary']:,.2f}")
    st.write(f"**Mid-Career Salary Range**: ${highest_paying_major['Mid-Career 10th Percentile Salary']:,.2f} - ${highest_paying_major['Mid-Career 90th Percentile Salary']:,.2f}")
    st.write(f"**Group**: {highest_paying_major['Group']}")

    st.subheader("Lowest-Paying Major")
    st.write(f"**Major**: {lowest_paying_major['Undergraduate Major']}")
    st.write(f"**Starting Median Salary**: ${lowest_paying_major['Starting Median Salary']:,.2f}")
    st.write(f"**Mid-Career Median Salary**: ${lowest_paying_major['Mid-Career Median Salary']:,.2f}")
    st.write(f"**Mid-Career Salary Range**: ${lowest_paying_major['Mid-Career 10th Percentile Salary']:,.2f} - ${lowest_paying_major['Mid-Career 90th Percentile Salary']:,.2f}")
    st.write(f"**Group**: {lowest_paying_major['Group']}")

# Main function
def main():
    data = load_data(DATA_FILE_PATH)

    st.title("College Salaries Explorer")
    st.write(data)

    with st.expander("Visualizations"):
        st.header("Visualizations")
        st.subheader("Mid-Career Median Salary by Group")
        plot_boxplot(data)
        st.subheader("Top 5 Majors by Mid-Career Median Salary")
        plot_top_majors(data)
        st.subheader("Top 5 Majors by Growth Salary")
        plot_growth_salary(data)

    with st.expander("Analysis"):
        st.header("Analysis")
        display_analysis(data)

if __name__ == "__main__":
    main()
