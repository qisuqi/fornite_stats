from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import streamlit as st
import pandas as pd

FAUNADB_KEY = st.secrets['FAUNADB_KEY']
client = FaunaClient(secret=FAUNADB_KEY)


@st.cache
def get_all_products():
    all_products = client.query(q.map_(lambda x: q.get(x), q.paginate(q.match(q.index('all_items')), size=1000)))
    return pd.DataFrame(x['data'] for x in all_products['data'])


def save_values(values):
    print(f'* Saving: {values} *')


def query_index():
    result = client.query(q.count(q.match(q.index('all_items'))))
    return result


st. set_page_config(layout="wide")

all_products = get_all_products()
name_list = all_products['Name'].unique()
weapon_name_list = all_products['Weapon Name'].unique()
weapon_color_list = all_products['Weapon Color'].unique()
weapon_type_list = all_products['Weapon Type'].unique()

most_weapon_name = all_products['Weapon Name'].value_counts().idxmax()
location = all_products[all_products['Location'] != 'NP']
location1 = location[location['Got Out'] == 'No']
most_location = location1['Location'].value_counts()[:1].index.tolist()
most_location1 = str(most_location).strip("'[]'")
info1 = "The most deadly weapon name is " + most_weapon_name
info2 = 'The most deadly location is ' + most_location1

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Home", "Player", "Submit Death"]

if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Home"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Home")
    active_tab = "Home"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="https://share.streamlit.io/qisuqi/fornite_stats/main/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == 'Home':

    output_graphs = st.beta_container()

    with output_graphs:
        
        card1, card2 = st.beta_columns(2)
        
        with card1:
            st.info(info1)
        with card2:
            st.info(info2)

        col1, col2, col3 = st.beta_columns(3)

        with col1:
            st.vega_lite_chart(all_products, {
                'width': 'container',
                'height': 400,
                "transform": [{"filter": "datum['Weapon Name'] != 'NW'"}],
                "mark": {"type": "arc", "tooltip": {"content": "encoding"}},
                "encoding": {
                    "theta": {"aggregate": "count", "title": "No. of Deaths"},
                    "color": {
                        "field": "Weapon Name",
                        "type": "nominal",
                        "scale": {"scheme": "tableau20"}
                    }
                },
                "view": {"stroke": None}
            },  use_container_width=True)

        with col2:
            st.vega_lite_chart(all_products, {
                'width': 'container',
                'height': 400,
                "transform": [{"filter": "datum['Weapon Color'] != 'NC'"}],
                "mark": {"type": "arc", "tooltip": {"content": "encoding"}},
                "encoding": {
                    "theta": {"aggregate": "count", "title": "No. of Deaths"},
                    "color": {
                        "field": "Weapon Color",
                        "type": "nominal",
                        "scale": {"scheme": "tableau20"}
                    }
                },
                "view": {"stroke": None}
            },  use_container_width=True)

        with col3:
            st.vega_lite_chart(all_products, {
                'width': 'container',
                'height': 400,
                "transform": [{"filter": "datum['Weapon Type'] != 'NT'"}],
                "mark": {"type": "arc", "tooltip": {"content": "encoding"}},
                "encoding": {
                    "theta": {"aggregate": "count", "title": "No. of Deaths"},
                    "color": {
                        "field": "Weapon Type",
                        "type": "nominal",
                        "scale": {"scheme": "tableau20"}
                    }
                },
                "view": {"stroke": None}
            },  use_container_width=True)

        st.vega_lite_chart(all_products, {
            'width': 'container',
            'height': 500,
            "mark": "bar",
            "encoding": {
                "x": {"field": "Weapons", "type": "ordinal"},
                "y": {"aggregate": "count", "title": "Deaths"},
                "tooltip": [
                    {"aggregate": "count", "title": "Number of Deaths"},
                    {"field": "Name", "type": "ordinal"}
                ],
                "color": {
                    "field": "Name",
                    "type": "nominal",
                    "scale": {"scheme": "tableau20"}
                }
            }
            }, use_container_width=True)

        col4, col5 = st.beta_columns(2)

        with col4:
            st.vega_lite_chart(all_products, {
                "width": "container",
                "height": 500,
                "mark": "bar",
                "transform": [{"filter": "datum['Win'] != 'NA'"}],
                "encoding": {
                    "y": {
                        "aggregate": "count",
                        "title": "Win %",
                        "stack": "normalize",
                        "axis": {"format": "%"}
                    },
                    "x": {"field": "Location", "type": "nominal"},
                    "color": {"field": "Win", "scale": {"scheme": "tableau20"}},
                    "tooltip": [
                        {"aggregate": "count", "title": "No. of Deaths"},
                        {"field": "Got Out"}
                    ]
                },
                "config": {"view": {"stroke": "transparent"}, "axis": {"domainWidth": 1}}
            }, use_container_width=True)

        with col5:
            st.vega_lite_chart(all_products, {
                "width": "container",
                "height": 500,
                "mark": "bar",
                "transform": [{"filter": "datum['Got Out'] != 'NA'"}],
                "encoding": {
                    "y": {
                        "aggregate": "count",
                        "title": "Got Out %",
                        "stack": "normalize",
                        "axis": {"format": "%"}
                    },
                    "x": {"field": "Location", "type": "nominal"},
                    "color": {"field": "Got Out", "scale": {"scheme": "tableau20"}},
                    "tooltip": [
                        {"aggregate": "count", "title": "No. of Deaths"},
                        {"field": "Got Out"}
                    ]
                },
                "config": {"view": {"stroke": "transparent"}, "axis": {"domainWidth": 1}}
            }, use_container_width=True)

        st.vega_lite_chart(all_products, {
            "width": {"step": 36},
            "height": 500,
            "mark": "bar",
            "transform": [
                {"filter": "datum['Location'] != 'NP'"},
                {"filter": "datum['Got Out'] != 'NA'"}
            ],
            "encoding": {
                "column": {"field": "Location", "type": "ordinal", "spacing": 10},
                "y": {"aggregate": "count", "title": "Total Deaths"},
                "x": {"field": "Got Out", "type": "nominal"},
                "color": {"field": "Name", "scale": {"scheme": "tableau20"}},
                "tooltip": [
                    {"aggregate": "count", "title": "Number of Deaths"},
                    {"field": "Name", "type": "ordinal"}
                ],
            },
            "config": {"view": {"stroke": "transparent"}, "axis": {"domainWidth": 1}}
        })

        st.vega_lite_chart(all_products, {
            "width": "container",
            "height": 500,
            "transform": [{"filter": "datum['Weapon Name'] != 'NW'"}],
            "mark": "bar",
            "encoding": {
                "x": {
                    "field": "Date",
                    "type": "ordinal",
                    "sort": [
                        "Jan",
                        "Feb",
                        "Mar",
                        "Apr",
                        "May",
                        "Jun",
                        "Jul",
                        "Aug",
                        "Sep",
                        "Oct",
                        "Nov",
                        "Dec"
                    ],
                    "axis": {"grid": False}
                },
                "y": {"aggregate": "count", "title": "Deaths"},
                "tooltip": [
                    {"aggregate": "count", "title": "No. of Deaths"},
                    {"field": "Weapon Name", "title": "Weapon Name"}
                ],
                "color": {
                    "field": "Weapon Name",
                    "type": "nominal",
                    "scale": {"scheme": "tableau20"}
                }
            }
        }, use_container_width=True)

if active_tab == 'Player':

    user_input = st.beta_container()
    output_graphs = st.beta_container()

    with st.sidebar:

        #st.header("Fill in the form")

        #with st.form(key='form'):
         #   st.selectbox(f'Name', name_list, key=1)
          #  st.selectbox(f'Weapon Name', weapon_name_list, key=2)
           # st.selectbox(f'Weapon Color', weapon_color_list, key=3)
           # st.selectbox(f'Weapon Type', weapon_type_list, key=4)
            #submitted = st.form_submit_button('Submit')

        st.header('Choose an option')
        players = st.sidebar.selectbox('Choose a player', name_list)
        df_players = all_products[(all_products.Name == players)].copy()

    with output_graphs:

        col1, col2, col3 = st.beta_columns(3)

        with col1:
            st.vega_lite_chart(df_players, {
                'width': 'container',
                'height': 400,
                "transform": [{"filter": "datum['Weapon Name'] != 'NW'"}],
                "mark": {"type": "arc", "tooltip": {"content": "encoding"}},
                "encoding": {
                    "theta": {"aggregate": "count", "title": "No. of Deaths"},
                    "color": {
                        "field": "Weapon Name",
                        "type": "nominal",
                        "scale": {"scheme": "tableau20"}
                    }
                },
                "view": {"stroke": None}
            },  use_container_width=True)

        with col2:
            st.vega_lite_chart(df_players, {
                'width': 'container',
                'height': 400,
                "transform": [{"filter": "datum['Weapon Color'] != 'NC'"}],
                "mark": {"type": "arc", "tooltip": {"content": "encoding"}},
                "encoding": {
                    "theta": {"aggregate": "count", "title": "No. of Deaths"},
                    "color": {
                        "field": "Weapon Color",
                        "type": "nominal",
                        "scale": {"scheme": "tableau20"}
                    }
                },
                "view": {"stroke": None}
            },  use_container_width=True)

        with col3:
            st.vega_lite_chart(df_players, {
                'width': 'container',
                'height': 400,
                "transform": [{"filter": "datum['Weapon Type'] != 'NT'"}],
                "mark": {"type": "arc", "tooltip": {"content": "encoding"}},
                "encoding": {
                    "theta": {"aggregate": "count", "title": "No. of Deaths"},
                    "color": {
                        "field": "Weapon Type",
                        "type": "nominal",
                        "scale": {"scheme": "tableau20"}
                    }
                },
                "view": {"stroke": None}
            },  use_container_width=True)

        st.vega_lite_chart(df_players, {
            'width': 'container',
            'height': 500,
            "mark": "bar",
            "encoding": {
                "x": {"field": "Weapons", "type": "ordinal"},
                "y": {"aggregate": "count", "title": "Deaths"},
                "tooltip": [
                    {"aggregate": "count", "title": "Number of Deaths"},
                    {"field": "Name", "type": "ordinal"}
                ],
                "color": {
                    "field": "Name",
                    "type": "nominal",
                    "scale": {"scheme": "tableau20"}
                }
            }
            }, use_container_width=True)

        col4, col5 = st.beta_columns(2)

        with col4:
            st.vega_lite_chart(df_players, {
                "width": "container",
                "height": 500,
                "mark": "bar",
                "transform": [{"filter": "datum['Win'] != 'NA'"}],
                "encoding": {
                    "y": {
                        "aggregate": "count",
                        "title": "Win %",
                        "stack": "normalize",
                        "axis": {"format": "%"}
                    },
                    "x": {"field": "Location", "type": "nominal"},
                    "color": {"field": "Win", "scale": {"scheme": "tableau20"}},
                    "tooltip": [
                        {"aggregate": "count", "title": "No. of Deaths"},
                        {"field": "Got Out"}
                    ]
                },
                "config": {"view": {"stroke": "transparent"}, "axis": {"domainWidth": 1}}
            }, use_container_width=True)

        with col5:
            st.vega_lite_chart(df_players, {
                "width": "container",
                "height": 500,
                "mark": "bar",
                "transform": [{"filter": "datum['Got Out'] != 'NA'"}],
                "encoding": {
                    "y": {
                        "aggregate": "count",
                        "title": "Got Out %",
                        "stack": "normalize",
                        "axis": {"format": "%"}
                    },
                    "x": {"field": "Location", "type": "nominal"},
                    "color": {"field": "Got Out", "scale": {"scheme": "tableau20"}},
                    "tooltip": [
                        {"aggregate": "count", "title": "No. of Deaths"},
                        {"field": "Got Out"}
                    ]
                },
                "config": {"view": {"stroke": "transparent"}, "axis": {"domainWidth": 1}}
            }, use_container_width=True)

        st.vega_lite_chart(df_players, {
            "width": {"step": 28},
            "height": 500,
            "mark": "bar",
            "transform": [
                {"filter": "datum['Location'] != 'NP'"},
                {"filter": "datum['Got Out'] != 'NA'"}
            ],
            "encoding": {
                "column": {"field": "Location", "type": "ordinal", "spacing": 10},
                "y": {"aggregate": "count", "title": "Total Deaths"},
                "x": {"field": "Got Out", "type": "nominal"},
                "color": {"field": "Name", "scale": {"scheme": "tableau20"}},
                "tooltip": [
                    {"aggregate": "count", "title": "Number of Deaths"},
                    {"field": "Name", "type": "ordinal"}
                ],
            },
            "config": {"view": {"stroke": "transparent"}, "axis": {"domainWidth": 1}}
        })

        st.vega_lite_chart(df_players, {
            "width": "container",
            "height": 500,
            "transform": [{"filter": "datum['Weapon Name'] != 'NW'"}],
            "mark": "bar",
            "encoding": {
                "x": {
                    "field": "Date",
                    "type": "ordinal",
                    "sort": [
                        "Jan",
                        "Feb",
                        "Mar",
                        "Apr",
                        "May",
                        "Jun",
                        "Jul",
                        "Aug",
                        "Sep",
                        "Oct",
                        "Nov",
                        "Dec"
                    ],
                    "axis": {"grid": False}
                },
                "y": {"aggregate": "count", "title": "Deaths"},
                "tooltip": [
                    {"aggregate": "count", "title": "No. of Deaths"},
                    {"field": "Weapon Name", "title": "Weapon Name"}
                ],
                "color": {
                    "field": "Weapon Name",
                    "type": "nominal",
                    "scale": {"scheme": "tableau20"}
                }
            }
        }, use_container_width=True)

if active_tab == 'Submit Death':
    st.title("Can't do the conditional form, go submit on the OG website :(")
    st.markdown('<a target="_blank" href="https://fortnitedeathstats.netlify.app/">Go submit the death</a>',
                unsafe_allow_html=True)


#f submitted:
 #   values = {'Name': name, 'Weapon Name': weapon_name}
  #  save_values(values)
   # name, weapon_name = None, None
    #submitted = False






