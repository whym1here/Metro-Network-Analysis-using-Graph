# Metro Network Analysis and Proposal

## Overview/Abstract

This project analyzes existing metro networks and proposes new metro line layouts for cities based on population distribution and geographical data. It utilizes web scraping for data collection, geospatial analysis for station mapping, clustering algorithms to identify potential station locations, and Minimum Spanning Trees (MST) to generate efficient network designs. The primary goal is to provide a data-driven approach for urban transit planning.

## Project Objectives

*   **Data Collection:** Scrape metro station names from online sources (e.g., Wikipedia) and gather their geographical coordinates using OpenStreetMap.
*   **Existing Network Analysis:** Generate and visualize MSTs for existing metro networks to understand their current structure.
*   **New Network Proposal:** Propose new metro network designs for cities by:
    *   Clustering geographical areas based on population density or other relevant metrics.
    *   Calculating MSTs based on these cluster centers to form potential metro lines.
*   **Algorithm Comparison:** Implement and compare different clustering algorithms (K-Means, Bisecting K-Means, Minibatch K-Means) for their effectiveness in network proposal.
*   **Visualization:** Create interactive maps and plots to visualize metro networks, station locations, and analysis results.

## Project Structure

The project is organized into several key directories and files:

*   `Raw-Data/`: Stores the initial lists of station names scraped from websites.
*   `web-scraping/`: Contains Python scripts (e.g., `delhi-metro-station-names.py`) that use `Requests` and `BeautifulSoup` to scrape station names from Wikipedia pages.
*   `dataset/`: Contains processed data, primarily CSV files (e.g., `delhi-metro-station-details.csv`) with station names and their corresponding latitude and longitude coordinates obtained from OpenStreetMap.
*   `plotter-finder/`: Includes scripts and notebooks for finding latitude/longitude coordinates for a list of station names and some initial plotting experiments.
    *   `latitude-longitude-finder.py`: Takes an `input.txt` file (with one station name per line) and uses the OpenStreetMap Nominatim API to find coordinates, saving them to a CSV in the `dataset/` directory.
    *   `input.txt`: A sample input file for `latitude-longitude-finder.py`.
*   `mst/`: Contains Python scripts (e.g., `delhi-mst.py`) to generate and visualize MSTs for existing metro networks using station data from the `dataset/` directory. Output maps are typically saved in this directory or `final-output/`.
*   `final-output/`: Stores the results of analyses, including generated HTML maps of proposed networks and CSV files containing cluster information.
*   `Raipur.csv`: An example input CSV file for `final.py` and the `final-*.ipynb` notebooks. It demonstrates the required format for proposing new networks:
    *   `Name`: Name of the location/area.
    *   `Latitude`: Latitude of the location.
    *   `Longitude`: Longitude of the location.
    *   `Population`: Population of the area.
    *   `Area (km)`: Area in square kilometers.
*   `final.py`: The main Streamlit web application. It allows users to upload a CSV (like `Raipur.csv`), choose a clustering algorithm, set parameters (like K for K-Means), and visualize the proposed metro network.
*   `final-kmc.ipynb`, `final-bkmc.ipynb`, `final-mbkmc.ipynb`: Jupyter notebooks that provide a more detailed, step-by-step analysis for proposing new metro networks using K-Means, Bisecting K-Means, and Minibatch K-Means clustering algorithms, respectively. They read data (e.g., from `Raipur.csv`), perform clustering, generate MSTs, and save output maps/CSVs to `final-output/`.
*   `mst_utils.py`: A utility script containing functions related to MST generation (e.g., Kruskal's algorithm, Haversine distance calculation).
*   `ml_utils.py`: A utility script containing functions related to machine learning tasks, primarily clustering.
*   `g_util.py`: A general utility script likely containing helper functions used across different parts of the project.
*   `assets/`: Contains static assets, like images, used by the Streamlit application (e.g., `logo.png`).
*   `dump/`: Appears to be a directory for storing miscellaneous or temporary files (e.g., `all-delhi-metro-station-details.csv`).
*   `comparison-all-kmc.ipynb`: A Jupyter notebook likely used for comparing the results of different K-Means clustering runs or configurations.
*   `requirements.txt`, `dependencies.txt`: Files listing project dependencies.

## Data Flow

1.  **Scrape Station Names:**
    *   Scripts in `web-scraping/` (e.g., `delhi-metro-station-names.py`) are run to scrape station names from Wikipedia.
    *   Output: Text files with station names are saved in `Raw-Data/`.

2.  **Prepare Input for Geocoding (Manual Step):**
    *   Station names from files in `Raw-Data/` are manually copied or processed into `plotter-finder/input.txt`. Each station name should be on a new line.

3.  **Find Coordinates (Geocoding):**
    *   The `city` variable within `plotter-finder/latitude-longitude-finder.py` is set to the target city (e.g., "Delhi").
    *   `plotter-finder/latitude-longitude-finder.py` is executed. It reads station names from `plotter-finder/input.txt` and uses the OpenStreetMap Nominatim API to fetch their latitude and longitude.
    *   Output: A CSV file (e.g., `delhi-metro-station-details.csv`) containing station names and coordinates is saved in the `dataset/` directory.

4.  **Existing Network Analysis (MST):**
    *   Scripts in `mst/` (e.g., `delhi-mst.py`) use the corresponding CSV files from `dataset/` (e.g., `dataset/delhi-metro-station-details.csv`).
    *   These scripts generate an MST based on the actual station locations.
    *   Output: Interactive HTML maps visualizing the MST of the existing network are saved, typically in the `mst/` directory or `final-output/`.

5.  **New Network Proposal (Clustering and MST):**
    *   Input: A user-provided CSV file (e.g., `Raipur.csv`) with columns: `Name` (of areas/localities), `Latitude`, `Longitude`, `Population`, and `Area (km)`.
    *   This CSV is used by either:
        *   `final.py` (Streamlit application)
        *   `final-kmc.ipynb`, `final-bkmc.ipynb`, `final-mbkmc.ipynb` (Jupyter notebooks)
    *   Process:
        *   The locations are clustered using a chosen algorithm (K-Means, Bisecting K-Means, Minibatch K-Means). Population can be used as weights in some clustering approaches.
        *   An MST is then generated using the centroids of these clusters as nodes.
    *   Output:
        *   Interactive HTML maps of the proposed metro network.
        *   CSV files containing cluster assignments and centroid data.
        *   These outputs are typically saved in the `final-output/` directory.

## Core Algorithms and Techniques Used

*   **Web Scraping:** `Requests` (for HTTP requests) and `BeautifulSoup` (for HTML parsing) to collect station data from Wikipedia.
*   **Geocoding:** `geopy` library with OpenStreetMap Nominatim API to convert station names/addresses into latitude and longitude coordinates.
*   **Data Handling and Manipulation:** `Pandas` for managing and processing datasets (station lists, coordinate data, population data).
*   **Clustering Algorithms:**
    *   `Scikit-learn` library for:
        *   K-Means
        *   Bisecting K-Means
        *   Minibatch K-Means
*   **Minimum Spanning Trees (MST):**
    *   Custom implementation of Kruskal's algorithm (likely in `mst_utils.py`).
    *   Haversine formula for calculating great-circle distances between geographical coordinates.
*   **Data Visualization:**
    *   `Folium`: For creating interactive maps (HTML output).
    *   `Matplotlib` and `Seaborn`: For static plots and charts in Jupyter notebooks.
*   **Web Application Framework:** `Streamlit` for creating the interactive user interface (`final.py`).

## How to Run the Project

### 1. Setup Environment and Dependencies

*   It's recommended to use a Python virtual environment.
    ```bash
    pip install virtualenv
    virtualenv venv
    # On Windows PowerShell
    .\venv\Scripts\activate.ps1
    # On macOS/Linux
    source venv/bin/activate
    ```
*   Install dependencies using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    (Note: `dependencies.txt` also exists; `requirements.txt` is generally the standard.)

### 2. Data Preparation

*   **A. To Scrape New/Updated City Station Names:**
    1.  Navigate to the `web-scraping/` directory.
    2.  Modify an existing script (e.g., `delhi-metro-station-names.py`) or create a new one for the target city and Wikipedia page.
    3.  Run the script (e.g., `python web-scraping/delhi-metro-station-names.py`).
    4.  The scraped station names will be saved in a file in the `Raw-Data/` directory.

*   **B. To Get Coordinates for Station Names:**
    1.  Prepare a file named `input.txt` in the `plotter-finder/` directory. List one station name per line. You can populate this from files in `Raw-Data/`.
    2.  Open `plotter-finder/latitude-longitude-finder.py`.
    3.  Modify the `city` variable in the script to your target city (e.g., `city = "Mumbai"`). This helps the geocoder disambiguate locations.
    4.  Run the script: `python plotter-finder/latitude-longitude-finder.py`.
    5.  The output CSV file (e.g., `<city>-metro-station-details.csv`) with names and coordinates will be saved in the `dataset/` directory.

### 3. Analyzing Existing Metro Networks

1.  Navigate to the `mst/` directory.
2.  Ensure the relevant station details CSV (from step 2B) is present in the `dataset/` directory.
3.  Modify the script (e.g., `delhi-mst.py`) to load the correct CSV file if needed.
4.  Run the script (e.g., `python mst/delhi-mst.py`).
5.  An HTML map visualizing the MST of the existing network will be generated in the `mst/` directory or `final-output/`.

### 4. Proposing New Networks (Streamlit Application)

1.  **Prepare Input Data:**
    *   Create a CSV file (similar to `Raipur.csv`) with the following columns for your target city/area:
        *   `Name`: Name of the locality or potential station area.
        *   `Latitude`: Latitude of the center of the area.
        *   `Longitude`: Longitude of the center of the area.
        *   `Population`: Estimated population of the area.
        *   `Area (km)`: Area in square kilometers.
2.  **Run the Streamlit App:**
    *   Ensure your input CSV is accessible.
    *   Navigate to the project's root directory.
    *   Run the command:
        ```bash
        streamlit run final.py
        ```
3.  **Use the App:**
    *   The application will open in your web browser.
    *   Upload your prepared CSV file.
    *   Enter the city name.
    *   Choose a clustering method (K-Means, Bisecting K-Means, Minibatch K-Means).
    *   Set the number of clusters (K).
    *   The results (map, cluster details) will be displayed.
    *   Generated files (maps, data) from analyses performed via the app or notebooks are typically found in `final-output/`.

### 5. Proposing New Networks (Jupyter Notebooks)

1.  **Prepare Input Data:**
    *   As in step 4.1, prepare your input CSV (e.g., `Raipur.csv`).
2.  **Run Notebooks:**
    *   Open a Jupyter Notebook server (`jupyter notebook` or `jupyter lab`).
    *   Navigate to and open one of the analysis notebooks (e.g., `final-kmc.ipynb`, `final-bkmc.ipynb`).
    *   In the notebook, ensure the `dataset_path` variable (or similar) correctly points to your input CSV file.
    *   Run the cells in the notebook sequentially.
3.  **View Outputs:**
    *   The notebook will display maps and data.
    *   Output HTML maps and CSV files (cluster data) will be saved in the `final-output/` directory.

## Project Status

This is a data analysis project aimed at demonstrating a methodology for metro network planning using publicly available data and common data science techniques.

## TODO / Future Work

*   Automate the creation of `plotter-finder/input.txt` from the scraped data in `Raw-Data/`.
*   Integrate more diverse datasets for new network proposals (e.g., points of interest, employment hubs, traffic flow data).
*   Develop more sophisticated weighting for clustering (e.g., combining population, area, and other socio-economic factors).
*   Explore other graph algorithms beyond MST for network design (e.g., Steiner trees, network flow algorithms).
*   Enhance the Streamlit application with more customization options and comparative analysis features.
*   Add comprehensive unit tests for utility functions and core logic.
*   Expand the analysis to include more cities and compare results.
*   Improve error handling and user feedback in scripts and the Streamlit app.
