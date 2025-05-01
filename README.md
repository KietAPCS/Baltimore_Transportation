# Baltimore Transportation Analysis

## Project Overview
This project presents a comprehensive analysis of Baltimore's transportation infrastructure, focusing on road networks, public transit systems, and traffic patterns. Using network analysis, geospatial data processing, and machine learning techniques, we identify critical bottlenecks, optimize bus routes, and predict traffic flows across the city.

## Key Features
- Graph-based representation of Baltimore's road network
- Analysis of Average Annual Daily Traffic (AADT) patterns
- Public transportation optimization via bus stop importance metrics
- Geospatial visualization of transportation data
- Machine learning models for traffic prediction

## Repository Structure

### Data Files
- **2025_Problem_D_Data/**: Primary datasets for analysis
  - `Bus_Routes.csv`: Public transit route information
  - `Bus_Stops.csv`: Bus stop locations and ridership data
  - `Edge_Names_With_Nodes.csv`: Road segment identifiers
  - `edges_drive.csv`: Road network connection data
  - `MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv`: Traffic volume data
  - `nodes_all.csv` & `nodes_drive.csv`: Intersection nodes data

### Geospatial Data
- `graph.geojson`: Complete network visualization
- `nodes.geojson`: Network intersection points
- `path.geojson`: Specific route visualizations

### Analysis Scripts
- `graph.py`: Core network construction and analysis
  - Creates directed graph representation
  - Calculates network metrics
  - Generates geospatial visualizations
- `bus.py`: Public transit analysis
  - Evaluates bus stop importance
  - Analyzes route efficiency
  - Identifies key transit hubs
- `analysis.py`/`analysis.ipynb`: Main analysis workflows
- `train.ipynb`: Model training for traffic prediction
- `prediction.ipynb`: Traffic flow forecasting

### Outputs
- **figures/**: Visualization outputs
  - Network topology visualizations
  - Traffic heatmaps
  - Distribution analyses
  - Bottleneck identification
- **models/**: Trained machine learning models
  - Traffic prediction models
  - Network flow optimizers

## Getting Started

### Requirements
- Python 3.8+
- NetworkX
- Pandas
- GeoPandas
- Matplotlib
- TensorFlow/Keras
- NumPy
- tqdm

### Installation
1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
To generate network visualizations and basic metrics:
```bash
python graph.py
```

To analyze bus transportation system:
```bash
python bus.py
```

For comprehensive analysis, open and run the Jupyter notebooks:
- `analysis.ipynb`: Overall network analysis
- `train.ipynb`: Model training
- `prediction.ipynb`: Traffic prediction

## Key Findings
- Identified the top 20 traffic bottlenecks in Baltimore's road network
- Analyzed traffic patterns across urban and rural areas
- Quantified the impact of major tunnels (Fort McHenry, Harbor) on traffic flow
- Created predictive models for future traffic volume

## Future Work
- Real-time traffic optimization algorithms
- Integration with weather data for condition-based predictions
- Multi-modal transportation planning

## Contributing
This project was developed for the 2025 Mathematical Contest in Modeling (MCM) / Interdisciplinary Contest in Modeling (ICM).

## Team
ICM Team - Baltimore Transportation Analysis

## License
MIT License

Copyright (c) 2025 ICM Team - Baltimore Transportation Analysis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Note: The data used in this project is sourced from public transportation agencies
and may be subject to different licenses. Please refer to the original data
providers for terms of use for the datasets.
