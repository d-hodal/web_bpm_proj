#######################
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import json
import gcsfs
# import numpy as np
# from os import path
# from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import seaborn as sns
# import matplotlib.patches as mpatches


#######################
# Page configuration
st.set_page_config(
    page_title="BPM Community Breakdown",
    page_icon="favicon_io/favicon-16x16.png",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.markdown(
    """
    <style>
    body {
        background-color: #c4c0d9;
    }
    </style>
    """,
    unsafe_allow_html=True
)



with open( "css_styles/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
#######################
# Load data

### Local

# df_reshaped = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/cleaned_data_for_ml.csv')
# df_analytics = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/data_for_analytics.csv')
# df_line = pd.read_excel('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/Community Growth.xlsx', header = 1)
# df_wordcloud = pd.read_csv('/home/dhodal/code/Shubhi-Varshney/data-bpm/raw_data/report-2024-04-10T1552.csv')



### GCS

# Credentials

service_account_json = st.secrets["gcp"]["service_account_json"]

credentials = json.loads(service_account_json) 

file_s = gcsfs.GCSFileSystem(project=credentials["project_id"], token=credentials)




# Bucket and files
bucket_name = 'personal_projects_ber'
file_path_analytics ='data_for_analytics.csv'
file_path_ml = "cleaned_data_for_ml.csv"
file_path_cg = "Community Growth.xlsx"
file_path_wc = "report-2024-04-10T1552.csv"


@st.cache_data
def load_csv(file_path):
    print(f'gs://{bucket_name}/{file_path}')
    with file_s.open(f'gs://{bucket_name}/{file_path}', 'rb') as f:
        df = pd.read_csv(f)
        
        return df

@st.cache_data(ttl="1d")
def load_excel(file_path, header_num=0):
    with file_s.open(f'{bucket_name}/{file_path}', 'rb') as f:
        df = pd.read_excel(f, header=header_num)
        return df

# Load DFs
df_gcs_an = load_csv(file_path_analytics)
df_gcs_ml = load_csv(file_path_ml)
df_gcs_cg = load_excel(file_path_cg, header_num=1)
df_gcs_wc = load_csv(file_path_wc)

df_analytics = df_gcs_an
df_reshaped = df_gcs_ml
df_line = df_gcs_cg
df_wordcloud = df_gcs_wc

########################

 # Links for about section hyperlinks
url_1 = "https://www.linkedin.com/in/email-shubhi-jain/"
url_2 = "https://www.linkedin.com/in/dominichodal"
url_3 = "https://www.linkedin.com/in/yulia-vilensky/"
url_4 = "https://linktr.ee/berlinproductmanagers"

#######################
# Info Links
info_1 = ""
info_2 = ""
info_3 = ""
info_4 = ""
info_5 = ""

# Sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
with st.sidebar:
    st.markdown("# BPM Community Dashboard")


    event_list = sorted(list(df_analytics.Event.unique()))

    selected_event = st.selectbox('Select an event', event_list, index=5)

    # with.st.sidebar.beta_container()
    with st.expander('About', expanded=False):
        st.write(
                "Made with 🖤 from Berlin,\n",
    "[Shubhi Jain](%s)" % url_1, "[Dominic Hodal](%s)," % url_2, "[Yulia Vilensky](%s)," % url_3, " & [BPM Team](%s)" % url_4
    )


# (https://www.linkedin.com/in/email-shubhi-jain/)
# (https://www.linkedin.com/in/yulia-vilensky/)

# Contents of ~/my_app/main_page.py

col_title = st.columns((1 ,6, 1), gap="small")

with col_title[1]:
    st.markdown('<span style="text-align: center; font-size: 40px; color: #4778FF;">Berlin Product Managers |  Community Dashboard</span>', unsafe_allow_html=True)

col_exp = st.columns((1 ,4, 2), gap="small")
# with col_exp[1]:

#     with st.expander("""
# Dear BPMers,
# This dashboard aims to support our community! Our mission is to Foster Product Culture in Berlin and have open communication; this is why our insights are available! 
# """):
#         st.markdown("""
# **Community Members**: To understand and gain insight into peers and foster better networking opportunities.\n
# **Hosting an event**: To comprehend what to expect from events through data analysis.\n
# **BPM sponsors**: To understand our audience, support ROI understanding, and ensure financial sustainability through sponsorship.\n
# **Berlin Community organizers**: To grasp event capacity, attendance rates, and strategies for building vibrant communities!
# """)
        
    
    
    
    



# event_name = df_line['Event Name'].iloc[selected_event]


#######################
# Dashboard Main Panel
col = st.columns((3, 4, 2.5), gap='medium',)

with col[0]:
    st.markdown('<span style="font-size: 30px; color: #4778FF;">Event Attendance</span>', unsafe_allow_html=True, help="Capacity versus attendees checked into event")
     #st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
   
   
    # st.info('This is a purely informational message', icon="ℹ️")           
    
    event_mask = df_analytics["Event"] == selected_event
    df_event_masked = df_analytics[event_mask]
    df_event_status = df_event_masked["Attendee Status"].value_counts()
   # attended  = df_event_status["Attending"]
    attended = df_event_status["Checked In"]
    venue_size = int(df_line['Venue size'].iloc[selected_event])

    at_percent_ = (attended / venue_size)*100
    at_percent = round(at_percent_, 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Participants", f"{attended}")
    col2.metric("Venue Capacity", f"{venue_size}")
    col3.metric("Attandance Rate", f"{at_percent}%")


with col[2]:
    st.markdown('<span style="font-size: 30px; color: #4778FF;">Participant Breakdown</span>', unsafe_allow_html=True, help="Attendee breakdown per selected event: The top chart shows attendees' job types, the bottom chart shows PM seniority breakdown")

    mask = df_analytics["Event"] == selected_event
    df_analytics_masked = df_analytics[mask]
    df_job_position = pd.DataFrame(df_analytics_masked["Your Job Position"].value_counts().reset_index())
    
    pie_colors =  ["#81D3C1", "#717c89","#8aa2a9","#90baad","#a1e5ab","#adf6b1", "#C1F9C4"]
    
    fig_pie = px.pie(df_job_position, values='count', names='Your Job Position', ) # 
    fig_pie.update_layout(showlegend=True, title= dict(text =str("Role"), font =dict(family="source sans pro", size=20, color = '#383971')))
    fig_pie.update_traces(hoverinfo='label+percent',
                  marker=dict(colors=pie_colors, ))
  
    st.plotly_chart(fig_pie, use_container_width=True,sharing="streamlit", )


    pod_mask = df_analytics_masked["Your Job Position"] == "Product"
    df_analytics_masked["Your Job Position"] = df_analytics_masked["Your Job Position"].fillna("Not given")
    df_seniority = df_analytics_masked[pod_mask]
    df_seniority["Choose your role"].value_counts()
    df_pod_list = pd.DataFrame(df_seniority["Choose your role"].value_counts().reset_index())


   #  st.markdown('<span style="font-size: 30px; color: #383971;">Seniority Breakdown</span>', unsafe_allow_html=True)
    
    pie_colors_2 =   ["#00C895","#39DEB6","#00B5B5", "#008AAB","#005F92",] # ["#005F92","#008AAB","#00B5B5", "#39DEB6","#00C895",]
    
    fig_pie_2 = px.pie(df_pod_list.iloc[:5], values='count', names='Choose your role', ) # 
    fig_pie_2.update_layout(showlegend=True, title= dict(text =str("Seniority"), font =dict(family="source sans pro", size=20, color = '#383971')))
    fig_pie_2.update_traces(hoverinfo='label+percent',
                  marker=dict(colors=pie_colors_2, ))
  
    st.plotly_chart(fig_pie_2, use_container_width=True,sharing="streamlit", )




with col[1]:
    st.markdown('<span style="font-size: 30px; color: #4778FF;">Social Media Growth</span>', unsafe_allow_html=True, help="How our social media engagement has grown per event, over time")


    df_line['Newsletter'] = df_line['Newsletter'].fillna(0)
    df_line['Socials'] = pd.to_datetime(df_line['Socials'], format='%d%b%Y:%H:%M:%S.%f')
    df_line['month'] = pd.DatetimeIndex(df_line['Socials']).month
    month_num = int(df_line['month'].iloc[(selected_event+ 1)])
    
    months = ["August", "September", "October", "November", "December", "January", "February", "March", "April", "May", "June", "July" ]
    

    list_l = list(df_line['LinkedIn'].iloc[:(selected_event+ 1)])
    list_2 = list(df_line['Newsletter'].iloc[:(selected_event+ 1)])
    list_3 = list(df_line['Instagram'].iloc[:(selected_event+ 1)])
    list_4 = months[:(selected_event + 1)]
  
    
    dict_growth = {
        "LinkedIn": list_l,
        "Mailing list": list_2,
        "Instagram": list_3,
        "Month": list_4
    }
    df_com_growth = pd.DataFrame(dict_growth)
    
    fig_line = go.Figure(data=go.Scatter(x=df_com_growth["Month"], y=df_com_growth["LinkedIn"], name="LinkedInS", line_color="#0A66C2",))
    fig_line.add_scatter(x=df_com_growth["Month"], y=df_com_growth["Mailing list"], name="Newsletter", line_color="#F76519")
    fig_line.add_scatter(x=df_com_growth["Month"], y=df_com_growth["Instagram"], name="Instagram", line_color="#E1306C")

# Update layout to change x-axis labels
    fig_line.update_layout(xaxis=dict(
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7],  # Positions of the ticks on the axis
        ticktext=months  # Labels for the ticks
))
  
    st.plotly_chart(fig_line, use_container_width=True,)
    


with col[1]:
    st.markdown('<span style="font-size: 30px; color: #4778FF;">What did people expect?</span>', unsafe_allow_html=True, help="See what people are people are talking about the most when they sign up for each or our events")
    
    #Event mask
    if selected_event > 5:
        event_num = selected_event
    else:
        event_num = 6
    
    # Worldcloud event mask    
    wc_mask = df_wordcloud["Event Name"].str.contains(f"{event_num}")
    df_wc_masked = df_wordcloud[wc_mask]

    #DF filtering
    df_wc_filtered = df_wc_masked.filter(like='What are your expectations for the upcoming event?').fillna("PM")

    # Text perparation
    text = []
    for column in df_wc_filtered:
        text.append(" ".join(review for review in df_wc_filtered[column]))
    text_joined = " ".join(review for review in text)

    # Stopword list
    stopwords = set(STOPWORDS)
    stopwords.update(["product", "manager", "PM", "people", "PMs", "products", "managers", "something", "learn", "network"])

    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text_joined)
    # Display the generated image:
    fig_wc, ax = plt.subplots()
    ax.scatter([1, 2, 3], [1, 2, 3])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    st.pyplot(fig_wc)
    
#     #Sankey graph
#     st.markdown('<span style="font-size: 30px; color: #4778FF;">Registration Flow</span>', unsafe_allow_html=True)
     

#     df_event_status = df_event_masked["Attendee Status"].value_counts()
#     attended  = df_event_status["Checked In"]
#     no_show  = df_event_status["Attending"]
#     cancelled = df_event_status["Not Attending"]
#     registered = attended + no_show + cancelled
#     # Overbooking ticket capacity
#     event_ticket_opened = df_line['Ticket opened'].iloc[selected_event + 1]
#     # Registered for event
#     san_registered = registered
#     # Got event ticket
#     san_ticketed = event_ticket_opened
#     # On event wait-list
#     san_wait_list = san_registered - san_ticketed
#     # Cancelled event ticket before event
#     cancelled = cancelled
#     # Had event ticket on day of event
#     confirmed = attended + no_show
#     # Actually attended the event
#     admitted = attended
#     # Didn't attend but had a ticket
#     no_show = confirmed - admitted
    
#     label = ["Registered", "Ticket", "Wait list", "Confirmed", "Cancelled", "Admitted", "No show"]
#     source = [0, 0, 1, 1, 2, 3, 3]
#     target = [1, 2, 3, 4, 3, 5, 6]
#     value = [san_registered, event_ticket_opened, san_wait_list, confirmed, cancelled, admitted, no_show]

    
#     color_san = ["#00487c","#4bb3fd","#3e6680","#0496ff", "#F82274", "#00FFE1", "#225DFF",]
    
#    # colors from pie chart -  ["#81D3C1", "#717c89","#8aa2a9","#90baad","#a1e5ab","#adf6b1", "#C1F9C4"] 
    
#     link= dict(source = source, target = target, value = value, color="#90baad")
#     node = dict(label = label, pad = 35, thickness = 10, color=color_san)
#     data = go.Sankey(link = link, node = node)

#     fig_san = go.Figure(data)
#     fig_san.update_layout(
#     hovermode = "x",
#     title = "Event ticket breakdown",
# )

#     st.plotly_chart(fig_san, use_container_width=True, sharing="streamlit",)


    

with col[0]:
    df_attendees = pd.DataFrame(df_reshaped["company"].value_counts().reset_index())
    st.markdown('<span style="font-size: 30px; color: #4778FF;">Top 10 Companies</span>', unsafe_allow_html=True)

    st.dataframe(df_attendees.iloc[:10],
                 column_order=("company", "count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "company": st.column_config.TextColumn(
                        "Companies",
                    ),
                    "count": st.column_config.ProgressColumn(
                        "Attendees",
                        format="%f",
                        min_value=0,
                        max_value=max(df_attendees["count"]),
                     )}
                 )


