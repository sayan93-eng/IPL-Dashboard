# 🏏 IPL Dashboard

A comprehensive analytics dashboard for Indian Premier League (IPL) cricket statistics from 2008-2024, built with Python, Flask, and Dash.

## ✨ Features

### 🏟️ Match Analysis
- **Detailed Scorecards**: Complete batting and bowling statistics
- **Partnership Analysis**: Visual breakdown of batting partnerships
- **Fall of Wickets**: Interactive wicket progression tracking
- **Innings Progression**: Bar plots and line charts showing run flow
- **Runs Distribution**: Pie charts analyzing scoring patterns

### 📊 Season Statistics  
- **Team Performance**: Win/loss records, form analysis
- **Player Rankings**: Top batters and bowlers for each season
- **Match Timeline**: Chronological view of all matches
- **Interactive Navigation**: Easy season and team selection

### 🏆 All-time Records
- **Career Statistics**: Complete player career analysis
- **Head-to-Head**: Batter vs bowler matchup analysis
- **Performance Metrics**: Advanced statistical comparisons
- **Historical Trends**: Multi-season performance tracking

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Pandas
- **Frontend**: Dash, Plotly, HTML/CSS
- **Styling**: Bootstrap, Custom CSS
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly graphs and charts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sayan93-eng/IPL-Dashboard.git
   cd IPL-Dashboard
   ```

2. **Run setup script**
   ```bash
   python setup.py
   ```

3. **Manual setup (alternative)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Download IPL Dataset**
   - Download from [Kaggle IPL Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
   - Extract to `data/ipl_complete_dataset_2008-2024/`
   - Ensure you have `matches.csv` and `deliveries.csv`

5. **Run the application**
   ```bash
   python dashboard.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
IPL-Dashboard/
├── src/
│   ├── alltime/          # All-time statistics module
│   ├── match/            # Match analysis module  
│   ├── season/           # Season statistics module
│   ├── home/             # Homepage module
│   ├── components/       # Shared UI components
│   ├── utils/            # Utility functions
│   └── assets/           # CSS and static files
├── data/                 # IPL dataset files
├── dashboard.py          # Main Flask application
├── requirements.txt      # Python dependencies
└── README.md
```

## 🎯 Usage Guide

### Navigation
- **Home**: Overview and project introduction
- **Match**: Detailed analysis of individual matches
- **Season**: Season-wise team and player statistics  
- **All-time**: Career records and head-to-head analysis

### Match Analysis
1. Select IPL season from dropdown
2. Choose specific match
3. Explore different tabs:
   - **Scorecard**: Batting/bowling figures
   - **Bar Plot**: Over-by-over progression
   - **Line Plot**: Cumulative run progression
   - **Pie Chart**: Runs distribution analysis

### Season Statistics
1. Select season
2. Navigate between:
   - **Matches**: Chronological match timeline
   - **Teams**: Team performance metrics
   - **Players**: Top performers rankings

### All-time Records
1. **Records**: Search any player for career stats
2. **Head-to-Head**: Compare batter vs bowler matchups

## 🔧 Configuration

### Data Location
Ensure your data files are in:
```
data/ipl_complete_dataset_2008-2024/
├── matches.csv
└── deliveries.csv
```

### Port Configuration
Default port is 5000. To change:
```python
# In dashboard.py
app.run(debug=True, port=YOUR_PORT)
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Source**: [Kaggle IPL Complete Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
- **Framework**: Built with Dash and Plotly
- **Inspiration**: Cricket analytics community

## 📞 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/sayan93-eng/IPL-Dashboard/issues) page
2. Create a new issue with detailed description
3. Provide error logs and environment details

---

**Made with ❤️ for cricket analytics enthusiasts**