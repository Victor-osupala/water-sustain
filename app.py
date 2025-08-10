import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from io import StringIO
import time

# Page configuration
st.set_page_config(
    page_title="Sustainable Water Framework - Malete, Kwara State",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e1e5e9;
    }
    .status-good {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-danger {
        color: #dc3545;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'water_data' not in st.session_state:
    st.session_state.water_data = {
        'total_usage': 15420,
        'daily_limit': 20000,
        'efficiency': 77.1,
        'regions': [
            {'name': 'Central Malete', 'usage': 4200, 'capacity': 5000, 'users': 1250, 'coordinator': 'Dr. Adebayo Johnson', 'contact': '+234-803-123-4567'},
            {'name': 'North District', 'usage': 3800, 'capacity': 5000, 'users': 1100, 'coordinator': 'Engr. Fatima Usman', 'contact': '+234-805-234-5678'},
            {'name': 'South District', 'usage': 3920, 'capacity': 5000, 'users': 1180, 'coordinator': 'Prof. Kayode Alabi', 'contact': '+234-807-345-6789'},
            {'name': 'East Quarter', 'usage': 3500, 'capacity': 5000, 'users': 980, 'coordinator': 'Mrs. Halima Ibrahim', 'contact': '+234-809-456-7890'}
        ]
    }

if 'electrical_data' not in st.session_state:
    st.session_state.electrical_data = {
        'solar': {'current': 45, 'capacity': 60, 'status': 'optimal'},
        'generator': {'current': 20, 'capacity': 40, 'status': 'standby'},
        'grid': {'current': 35, 'capacity': 50, 'status': 'stable'}
    }

if 'user_metrics' not in st.session_state:
    st.session_state.user_metrics = {
        'total_users': 4510,
        'active_users': 3890,
        'avg_consumption': 3.42,
        'peak_hours': '10:00 - 14:00'
    }

# Load and process global water data
@st.cache_data
def load_global_water_data():
    """Load the global water consumption data for reference"""
    try:
        # Sample data from the CSV - in practice, you would load the actual file
        global_data = """Country,Year,Total Water Consumption (Billion Cubic Meters),Per Capita Water Use (Liters per Day),Agricultural Water Use (%),Industrial Water Use (%),Household Water Use (%),Rainfall Impact (Annual Precipitation in mm),Groundwater Depletion Rate (%),Water Scarcity Level
Nigeria,2024,487.5,245.8,52.3,28.7,19.0,1200.5,3.2,Moderate
Brazil,2024,417.2,310.0,55.5,18.4,23.9,1354.1,2.9,Low
India,2024,479.8,337.8,42.8,26.5,22.6,1391.9,2.2,Low
China,2024,507.3,253.1,50.9,25.6,26.8,1796.5,2.5,Moderate
USA,2024,249.5,186.4,51.4,24.8,27.7,1771.2,1.6,High"""
        
        df = pd.read_csv(StringIO(global_data))
        return df
    except:
        return pd.DataFrame()

# Helper functions
def get_status_class(usage, capacity):
    percentage = (usage / capacity) * 100
    if percentage < 60:
        return "status-good"
    elif percentage < 80:
        return "status-warning"
    else:
        return "status-danger"

def get_status_text(usage, capacity):
    percentage = (usage / capacity) * 100
    if percentage < 60:
        return "Normal"
    elif percentage < 80:
        return "High Usage"
    else:
        return "Critical"

# Main header
st.title("🌊 Sustainable Water Framework - Malete, Kwara State")
st.markdown("**AI-Powered Water Management System** | Real-time Monitoring Dashboard")

# Current time display
current_time = datetime.datetime.now()
st.markdown(f"**System Status:** 🟢 Online | **Last Updated:** {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Sidebar for navigation and controls
with st.sidebar:
    st.header("Navigation")
    tab_selection = st.selectbox(
        "Select Dashboard View:",
        ["📊 Dashboard", "👥 User Monitoring", "🗺️ Regional Distribution", "⚡ Power Management"]
    )
    
    st.header("System Controls")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.button("📥 Export Report"):
        st.success("Report exported successfully!")
    
    st.header("Quick Stats")
    st.metric("Total Users", f"{st.session_state.user_metrics['total_users']:,}")
    st.metric("Water Usage", f"{st.session_state.water_data['total_usage']:,}L")
    st.metric("Efficiency", f"{st.session_state.water_data['efficiency']}%")

# Main content area
if tab_selection == "📊 Dashboard":
    st.header("System Overview Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💧 Total Water Usage",
            f"{st.session_state.water_data['total_usage']:,}L",
            delta=f"{st.session_state.water_data['daily_limit'] - st.session_state.water_data['total_usage']:,}L remaining"
        )
    
    with col2:
        st.metric(
            "👥 Active Users",
            f"{st.session_state.user_metrics['active_users']:,}",
            delta=f"{st.session_state.user_metrics['total_users'] - st.session_state.user_metrics['active_users']} offline"
        )
    
    with col3:
        total_power = st.session_state.electrical_data['solar']['current'] + \
                     st.session_state.electrical_data['grid']['current'] + \
                     st.session_state.electrical_data['generator']['current']
        st.metric("⚡ Total Power", f"{total_power}kW", delta="Mixed sources")
    
    with col4:
        st.metric(
            "📈 Efficiency",
            f"{st.session_state.water_data['efficiency']}%",
            delta="2.3% from last week"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weekly Water Usage Trend")
        weekly_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Usage (L)': [14200, 15100, 14800, 15420, 16200, 13800, 12500],
            'Users': [4200, 4350, 4180, 4510, 4680, 3920, 3650]
        })
        
        fig = px.line(weekly_data, x='Day', y='Usage (L)', 
                     title="Daily Water Consumption", 
                     color_discrete_sequence=['#3b82f6'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Power Source Distribution")
        power_data = pd.DataFrame({
            'Source': ['Solar', 'Grid', 'Generator'],
            'Current (kW)': [
                st.session_state.electrical_data['solar']['current'],
                st.session_state.electrical_data['grid']['current'],
                st.session_state.electrical_data['generator']['current']
            ],
            'Colors': ['#f59e0b', '#10b981', '#ef4444']
        })
        
        fig = px.pie(power_data, values='Current (kW)', names='Source',
                    title="Current Power Distribution",
                    color_discrete_sequence=['#f59e0b', '#10b981', '#ef4444'])
        st.plotly_chart(fig, use_container_width=True)

elif tab_selection == "👥 User Monitoring":
    st.header("User Monitoring & Management")
    
    # User metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Registered Users", f"{st.session_state.user_metrics['total_users']:,}")
    with col2:
        st.metric("Currently Active", f"{st.session_state.user_metrics['active_users']:,}")
    with col3:
        st.metric("Avg. Consumption", f"{st.session_state.user_metrics['avg_consumption']}L/user")
    with col4:
        st.metric("Peak Hours", st.session_state.user_metrics['peak_hours'])
    
    st.divider()
    
    # Global comparison
    st.subheader("🌍 Global Water Usage Comparison")
    global_df = load_global_water_data()
    
    if not global_df.empty:
        # Calculate Nigeria's position
        nigeria_per_capita = 245.8  # From the data
        malete_per_capita = (st.session_state.water_data['total_usage'] / st.session_state.user_metrics['active_users']) * 1000
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Nigeria (National Average)",
                f"{nigeria_per_capita:.1f}L/day per capita",
                delta="Reference baseline"
            )
        
        with col2:
            st.metric(
                "Malete (Current)",
                f"{malete_per_capita:.1f}L/day per capita",
                delta=f"{malete_per_capita - nigeria_per_capita:+.1f}L vs national avg"
            )
        
        # Global comparison chart
        if len(global_df) > 0:
            fig = px.bar(global_df, x='Country', y='Per Capita Water Use (Liters per Day)',
                        title="Global Per Capita Water Usage Comparison (2024)",
                        color='Water Scarcity Level',
                        color_discrete_map={'Low': '#10b981', 'Moderate': '#f59e0b', 'High': '#ef4444'})
            
            # Add Malete data point
            fig.add_scatter(x=['Malete, Nigeria'], y=[malete_per_capita],
                           mode='markers', marker=dict(size=15, color='purple'),
                           name='Malete Current')
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # User management section
    st.subheader("📝 User Record Management")
    
    # Select region to manage
    selected_region = st.selectbox(
        "Select Region to Manage:",
        [region['name'] for region in st.session_state.water_data['regions']]
    )
    
    # Find selected region data
    region_data = next(r for r in st.session_state.water_data['regions'] if r['name'] == selected_region)
    region_index = st.session_state.water_data['regions'].index(region_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Current Data for {selected_region}:**")
        st.markdown(f"- **Users:** {region_data['users']:,}")
        st.markdown(f"- **Water Usage:** {region_data['usage']:,}L")
        st.markdown(f"- **Capacity:** {region_data['capacity']:,}L")
        st.markdown(f"- **Coordinator:** {region_data['coordinator']}")
        st.markdown(f"- **Contact:** {region_data['contact']}")
        
        utilization = (region_data['usage'] / region_data['capacity']) * 100
        st.progress(utilization / 100, text=f"Capacity Utilization: {utilization:.1f}%")
    
    with col2:
        st.markdown("**Update Record:**")
        
        with st.form(f"update_form_{selected_region}"):
            new_users = st.number_input("Number of Users", 
                                       min_value=0, 
                                       value=region_data['users'],
                                       step=1)
            
            new_usage = st.number_input("Current Water Usage (L)", 
                                       min_value=0, 
                                       value=region_data['usage'],
                                       step=10)
            
            new_capacity = st.number_input("Water Capacity (L)", 
                                          min_value=1, 
                                          value=region_data['capacity'],
                                          step=100)
            
            new_coordinator = st.text_input("Coordinator Name", 
                                           value=region_data['coordinator'])
            
            new_contact = st.text_input("Contact Information", 
                                       value=region_data['contact'])
            
            submitted = st.form_submit_button("🔄 Update Record")
            
            if submitted:
                # Update the region data
                st.session_state.water_data['regions'][region_index] = {
                    'name': selected_region,
                    'usage': new_usage,
                    'capacity': new_capacity,
                    'users': new_users,
                    'coordinator': new_coordinator,
                    'contact': new_contact
                }
                
                # Update total metrics
                total_users = sum(r['users'] for r in st.session_state.water_data['regions'])
                total_usage = sum(r['usage'] for r in st.session_state.water_data['regions'])
                
                st.session_state.user_metrics['total_users'] = total_users
                st.session_state.user_metrics['active_users'] = int(total_users * 0.86)  # Assume 86% active
                st.session_state.water_data['total_usage'] = total_usage
                
                st.success(f"✅ Record updated successfully for {selected_region}!")
                st.rerun()
    
    st.divider()
    
    # User activity chart
    st.subheader("📈 User Activity Analysis")
    weekly_users = pd.DataFrame({
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Active Users': [4200, 4350, 4180, 4510, 4680, 3920, 3650],
        'New Registrations': [45, 67, 23, 89, 156, 78, 34],
        'Water Requests': [8400, 8700, 8360, 9020, 9360, 7840, 7300]
    })
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=weekly_users['Day'], y=weekly_users['Active Users'], name="Active Users"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=weekly_users['Day'], y=weekly_users['Water Requests'], 
                  mode='lines+markers', name="Water Requests"),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Day of Week")
    fig.update_yaxes(title_text="Number of Users", secondary_y=False)
    fig.update_yaxes(title_text="Water Requests", secondary_y=True)
    fig.update_layout(title_text="Weekly User Activity & Water Requests")
    
    st.plotly_chart(fig, use_container_width=True)

elif tab_selection == "🗺️ Regional Distribution":
    st.header("Regional Water Distribution Analysis")
    
    # Regional overview cards
    st.subheader("Regional Status Overview")
    
    cols = st.columns(2)
    for i, region in enumerate(st.session_state.water_data['regions']):
        with cols[i % 2]:
            utilization = (region['usage'] / region['capacity']) * 100
            status_class = get_status_class(region['usage'], region['capacity'])
            status_text = get_status_text(region['usage'], region['capacity'])
            
            with st.container():
                st.markdown(f"### 📍 {region['name']}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Current Usage", f"{region['usage']:,}L")
                    st.metric("Users", f"{region['users']:,}")
                with col_b:
                    st.metric("Capacity", f"{region['capacity']:,}L")
                    st.metric("Utilization", f"{utilization:.1f}%")
                
                # Status indicator
                if status_text == "Normal":
                    st.success(f"Status: {status_text}")
                elif status_text == "High Usage":
                    st.warning(f"Status: {status_text}")
                else:
                    st.error(f"Status: {status_text}")
                
                st.progress(utilization / 100)
                
                # Contact info
                st.markdown(f"**Coordinator:** {region['coordinator']}")
                st.markdown(f"**Contact:** {region['contact']}")
    
    st.divider()
    
    # Regional comparison chart
    st.subheader("📊 Regional Usage Comparison")
    
    regions_df = pd.DataFrame(st.session_state.water_data['regions'])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Usage',
        x=regions_df['name'],
        y=regions_df['usage'],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Capacity',
        x=regions_df['name'],
        y=regions_df['capacity'],
        marker_color='darkblue',
        opacity=0.6
    ))
    
    fig.update_layout(
        title="Water Usage vs Capacity by Region",
        xaxis_title="Region",
        yaxis_title="Water (Liters)",
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution efficiency analysis
    st.subheader("🎯 Distribution Efficiency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Usage per capita by region
        regions_df['per_capita'] = regions_df['usage'] / regions_df['users']
        fig = px.bar(regions_df, x='name', y='per_capita',
                    title="Water Usage Per Capita by Region",
                    color='per_capita',
                    color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Capacity utilization
        regions_df['utilization'] = (regions_df['usage'] / regions_df['capacity']) * 100
        fig = px.pie(regions_df, values='utilization', names='name',
                    title="Capacity Utilization Distribution")
        st.plotly_chart(fig, use_container_width=True)

elif tab_selection == "⚡ Power Management":
    st.header("Power Management & Sustainability")
    
    # Power source status
    st.subheader("🔋 Current Power Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        solar = st.session_state.electrical_data['solar']
        solar_util = (solar['current'] / solar['capacity']) * 100
        st.markdown("### ☀️ Solar Power")
        st.metric("Current Output", f"{solar['current']}kW")
        st.metric("Capacity", f"{solar['capacity']}kW")
        st.progress(solar_util / 100, text=f"Utilization: {solar_util:.1f}%")
        st.markdown(f"**Status:** {solar['status']}")
    
    with col2:
        grid = st.session_state.electrical_data['grid']
        grid_util = (grid['current'] / grid['capacity']) * 100
        st.markdown("### 🏢 Grid Supply")
        st.metric("Current Load", f"{grid['current']}kW")
        st.metric("Capacity", f"{grid['capacity']}kW")
        st.progress(grid_util / 100, text=f"Utilization: {grid_util:.1f}%")
        st.markdown(f"**Status:** {grid['status']}")
    
    with col3:
        generator = st.session_state.electrical_data['generator']
        gen_util = (generator['current'] / generator['capacity']) * 100
        st.markdown("### 🔧 Generator Backup")
        st.metric("Current Load", f"{generator['current']}kW")
        st.metric("Capacity", f"{generator['capacity']}kW")
        st.progress(gen_util / 100, text=f"Utilization: {gen_util:.1f}%")
        st.markdown(f"**Status:** {generator['status']}")
    
    st.divider()
    
    # Power management controls
    st.subheader("⚙️ Power Management Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Optimization Schedule:**")
        schedule_data = pd.DataFrame({
            'Time Period': ['06:00 - 18:00', '18:00 - 22:00', '22:00 - 06:00', 'Emergency'],
            'Primary Source': ['Solar', 'Grid', 'Grid + Storage', 'Generator'],
            'Priority': ['High', 'Medium', 'Medium', 'Critical']
        })
        st.dataframe(schedule_data, use_container_width=True)
        
        # Power adjustment controls
        with st.expander("🔧 Adjust Power Sources"):
            new_solar = st.slider("Solar Output (kW)", 0, 60, solar['current'])
            new_grid = st.slider("Grid Load (kW)", 0, 50, grid['current'])
            new_gen = st.slider("Generator Load (kW)", 0, 40, generator['current'])
            
            if st.button("Apply Power Changes"):
                st.session_state.electrical_data['solar']['current'] = new_solar
                st.session_state.electrical_data['grid']['current'] = new_grid
                st.session_state.electrical_data['generator']['current'] = new_gen
                st.success("Power configuration updated!")
                st.rerun()
    
    with col2:
        st.markdown("**Sustainability Metrics:**")
        
        total_power = solar['current'] + grid['current'] + generator['current']
        renewable_percentage = (solar['current'] / total_power) * 100
        
        sustainability_metrics = pd.DataFrame({
            'Metric': [
                'Renewable Energy %',
                'Carbon Footprint',
                'Energy Efficiency',
                'Monthly Cost Savings'
            ],
            'Value': [
                f"{renewable_percentage:.1f}%",
                "2.1 tons CO₂/month",
                "87.3%",
                "₦245,000"
            ],
            'Target': [
                "60%",
                "< 2.0 tons",
                "> 85%",
                "> ₦200,000"
            ]
        })
        st.dataframe(sustainability_metrics, use_container_width=True)
        
        # Environmental impact chart
        impact_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'CO2 Emissions (tons)': [2.8, 2.5, 2.3, 2.1, 1.9, 2.1],
            'Renewable %': [35, 40, 42, 45, 48, 45]
        })
        
        fig = px.line(impact_data, x='Month', y='CO2 Emissions (tons)',
                     title="Environmental Impact Trend",
                     color_discrete_sequence=['#ef4444'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Power forecasting
    st.subheader("🔮 Power Demand Forecasting")
    
    # Generate hourly forecast data
    hours = list(range(24))
    solar_forecast = [0 if h < 6 or h > 18 else 30 + 15 * np.sin((h - 6) * np.pi / 12) for h in hours]
    demand_forecast = [20 + 10 * np.sin((h - 8) * np.pi / 16) + np.random.normal(0, 2) for h in hours]
    
    forecast_df = pd.DataFrame({
        'Hour': hours,
        'Solar Available': solar_forecast,
        'Predicted Demand': demand_forecast,
        'Grid Required': [max(0, d - s) for d, s in zip(demand_forecast, solar_forecast)]
    })
    
    fig = px.line(forecast_df, x='Hour', y=['Solar Available', 'Predicted Demand', 'Grid Required'],
                 title="24-Hour Power Demand Forecast",
                 labels={'value': 'Power (kW)', 'variable': 'Source'})
    st.plotly_chart(fig, use_container_width=True)

else:  # Regional Distribution (already covered above, but adding CSV upload functionality)
    st.header("📤 Data Management & CSV Analysis")
    
    # CSV upload section
    st.subheader("📁 Upload Global Water Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ CSV file uploaded successfully!")
            
            # Display basic info about the uploaded data
            st.markdown(f"**File contains:** {len(df)} rows and {len(df.columns)} columns")
            
            # Show first few rows
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Basic analysis
            if 'Country' in df.columns and 'Per Capita Water Use (Liters per Day)' in df.columns:
                st.subheader("🔍 Quick Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Countries with highest water usage
                    latest_year_data = df[df['Year'] == df['Year'].max()]
                    top_consumers = latest_year_data.nlargest(10, 'Per Capita Water Use (Liters per Day)')
                    
                    fig = px.bar(top_consumers, 
                               x='Country', 
                               y='Per Capita Water Use (Liters per Day)',
                               title="Top 10 Water Consumers (Per Capita)",
                               color='Water Scarcity Level',
                               color_discrete_map={'Low': '#10b981', 'Moderate': '#f59e0b', 'High': '#ef4444'})
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Water scarcity distribution
                    scarcity_counts = latest_year_data['Water Scarcity Level'].value_counts()
                    fig = px.pie(values=scarcity_counts.values, 
                               names=scarcity_counts.index,
                               title="Global Water Scarcity Distribution",
                               color_discrete_map={'Low': '#10b981', 'Moderate': '#f59e0b', 'High': '#ef4444'})
                    st.plotly_chart(fig, use_container_width=True)
                
                # Comparative analysis with Nigeria
                nigeria_data = df[df['Country'] == 'Nigeria']
                if not nigeria_data.empty:
                    latest_nigeria = nigeria_data[nigeria_data['Year'] == nigeria_data['Year'].max()].iloc[0]
                    
                    st.subheader("🇳🇬 Nigeria vs Malete Comparison")
                    
                    comp_col1, comp_col2, comp_col3 = st.columns(3)
                    
                    with comp_col1:
                        st.metric(
                            "Nigeria (National)",
                            f"{latest_nigeria['Per Capita Water Use (Liters per Day)']:.1f}L/day",
                            delta="Reference"
                        )
                    
                    with comp_col2:
                        malete_per_capita = (st.session_state.water_data['total_usage'] / st.session_state.user_metrics['active_users']) * 1000
                        st.metric(
                            "Malete (Current)",
                            f"{malete_per_capita:.1f}L/day",
                            delta=f"{malete_per_capita - latest_nigeria['Per Capita Water Use (Liters per Day)']:+.1f}L vs national"
                        )
                    
                    with comp_col3:
                        efficiency_score = min(100, (latest_nigeria['Per Capita Water Use (Liters per Day)'] / malete_per_capita) * 100)
                        st.metric(
                            "Efficiency Score",
                            f"{efficiency_score:.1f}%",
                            delta="vs national average"
                        )
        
        except Exception as e:
            st.error(f"❌ Error processing CSV file: {str(e)}")
    
    # Regional distribution map simulation
    st.subheader("🗺️ Regional Distribution Map")
    
    # Create a simple coordinate system for Malete regions
    map_data = pd.DataFrame({
        'Region': [region['name'] for region in st.session_state.water_data['regions']],
        'Latitude': [8.95, 8.97, 8.93, 8.96],  # Approximate coordinates for Malete
        'Longitude': [5.35, 5.33, 5.34, 5.37],
        'Usage': [region['usage'] for region in st.session_state.water_data['regions']],
        'Users': [region['users'] for region in st.session_state.water_data['regions']],
        'Utilization': [(region['usage'] / region['capacity']) * 100 for region in st.session_state.water_data['regions']]
    })
    
    fig = px.scatter_mapbox(
        map_data,
        lat='Latitude',
        lon='Longitude',
        size='Usage',
        color='Utilization',
        hover_name='Region',
        hover_data={'Users': True, 'Usage': True},
        color_continuous_scale='RdYlGn_r',
        title="Water Distribution Across Malete Regions",
        mapbox_style='open-street-map',
        zoom=12,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer with real-time updates
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 System Performance")
    total_capacity = sum(r['capacity'] for r in st.session_state.water_data['regions'])
    total_usage = sum(r['usage'] for r in st.session_state.water_data['regions'])
    system_efficiency = (total_usage / total_capacity) * 100
    
    if system_efficiency < 70:
        st.success(f"System Efficiency: {system_efficiency:.1f}% - Optimal")
    elif system_efficiency < 85:
        st.warning(f"System Efficiency: {system_efficiency:.1f}% - Good")
    else:
        st.error(f"System Efficiency: {system_efficiency:.1f}% - High Load")

with col2:
    st.markdown("### 🌱 Sustainability Score")
    
    # Calculate sustainability score based on multiple factors
    renewable_ratio = st.session_state.electrical_data['solar']['current'] / (
        st.session_state.electrical_data['solar']['current'] + 
        st.session_state.electrical_data['grid']['current'] + 
        st.session_state.electrical_data['generator']['current']
    ) * 100
    
    water_efficiency = st.session_state.water_data['efficiency']
    sustainability_score = (renewable_ratio * 0.4 + water_efficiency * 0.6)
    
    if sustainability_score >= 80:
        st.success(f"Score: {sustainability_score:.1f}/100 - Excellent")
    elif sustainability_score >= 60:
        st.warning(f"Score: {sustainability_score:.1f}/100 - Good")
    else:
        st.error(f"Score: {sustainability_score:.1f}/100 - Needs Improvement")

with col3:
    st.markdown("### 🚨 Alert Status")
    
    alerts = []
    
    # Check for high usage regions
    for region in st.session_state.water_data['regions']:
        util = (region['usage'] / region['capacity']) * 100
        if util > 90:
            alerts.append(f"Critical usage in {region['name']}")
        elif util > 80:
            alerts.append(f"High usage in {region['name']}")
    
    # Check power status
    if st.session_state.electrical_data['generator']['current'] > 10:
        alerts.append("Generator backup in use")
    
    if alerts:
        for alert in alerts[:3]:  # Show max 3 alerts
            st.error(f"⚠️ {alert}")
    else:
        st.success("✅ All systems normal")

# Auto-refresh functionality
if st.sidebar.checkbox("🔄 Auto-refresh (every 30 seconds)"):
    time.sleep(1)  # Small delay to prevent too frequent updates
    st.rerun()

# Export functionality
st.divider()
st.subheader("📤 Data Export & Reports")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export Usage Report"):
        # Create summary report
        report_data = {
            'Timestamp': [current_time.strftime('%Y-%m-%d %H:%M:%S')],
            'Total_Usage_L': [st.session_state.water_data['total_usage']],
            'Total_Users': [st.session_state.user_metrics['total_users']],
            'System_Efficiency': [st.session_state.water_data['efficiency']],
            'Sustainability_Score': [sustainability_score]
        }
        
        report_df = pd.DataFrame(report_data)
        csv = report_df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Download Report CSV",
            data=csv,
            file_name=f"malete_water_report_{current_time.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("🗺️ Export Regional Data"):
        regions_df = pd.DataFrame(st.session_state.water_data['regions'])
        csv = regions_df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Download Regional CSV",
            data=csv,
            file_name=f"malete_regional_data_{current_time.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col3:
    if st.button("⚡ Export Power Data"):
        power_df = pd.DataFrame([
            {'Source': 'Solar', 'Current_kW': st.session_state.electrical_data['solar']['current'], 
             'Capacity_kW': st.session_state.electrical_data['solar']['capacity'], 
             'Status': st.session_state.electrical_data['solar']['status']},
            {'Source': 'Grid', 'Current_kW': st.session_state.electrical_data['grid']['current'], 
             'Capacity_kW': st.session_state.electrical_data['grid']['capacity'], 
             'Status': st.session_state.electrical_data['grid']['status']},
            {'Source': 'Generator', 'Current_kW': st.session_state.electrical_data['generator']['current'], 
             'Capacity_kW': st.session_state.electrical_data['generator']['capacity'], 
             'Status': st.session_state.electrical_data['generator']['status']}
        ])
        
        csv = power_df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Download Power CSV",
            data=csv,
            file_name=f"malete_power_data_{current_time.strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )


st.sidebar.markdown("### 📈 Features:")
st.sidebar.markdown("""
- ✅ Real-time water usage monitoring
- ✅ Regional distribution tracking
- ✅ User management with update forms
- ✅ Power source optimization
- ✅ Global data comparison via CSV upload
- ✅ Sustainability scoring
- ✅ Data export functionality
- ✅ Interactive charts and maps
- ✅ Alert system for critical conditions
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <strong>Sustainable Water Framework for AI Operations</strong><br>
        Malete, Kwara State, Nigeria | Powered by Streamlit & Plotly<br>
        <em>Promoting sustainable water usage through intelligent monitoring and management</em>
    </div>
    """, 
    unsafe_allow_html=True
)