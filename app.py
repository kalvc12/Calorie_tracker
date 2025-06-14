
import streamlit as st
import requests
import pandas as pd
import datetime
import os

st.set_page_config(page_title='Personal Calorie & Macro Tracker', page_icon='🍏')

LOG_FILE = 'food_log.csv'

def search_food(query):
    """Search OpenFoodFacts for the first product match."""
    params = {
        'search_terms': query,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': 1
    }
    resp = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params=params, timeout=10)
    if resp.status_code != 200:
        st.error('Error contacting OpenFoodFacts')
        return None
    data = resp.json()
    if data.get('count', 0) == 0:
        return None
    return data['products'][0]

def extract_nutrients(product):
    """Return kcal & macros per 100 g from product record."""
    n = product.get('nutriments', {})
    return {
        'energy_kcal_100g': n.get('energy-kcal_100g') or n.get('energy-kcal'),
        'protein_100g': n.get('proteins_100g'),
        'carbs_100g': n.get('carbohydrates_100g'),
        'fat_100g': n.get('fat_100g')
    }

def load_log():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE, parse_dates=['date'])
    else:
        return pd.DataFrame(columns=['date', 'food', 'quantity_g', 'kcal', 'protein', 'carbs', 'fat'])

def save_log(df):
    df.to_csv(LOG_FILE, index=False)

st.title('🍏 Personal Calorie & Macro Tracker')

# Search & add food
query = st.text_input('Search food (powered by OpenFoodFacts):')
quantity = st.number_input('Serving size (g)', 0.0, 2000.0, 100.0, step=10.0)

if st.button('Add to log') and query.strip():
    product = search_food(query.strip())
    if not product:
        st.warning('No products found.')
    else:
        nutrients = extract_nutrients(product)
        if not nutrients['energy_kcal_100g']:
            st.warning('Nutrient data incomplete for this item.')
        else:
            kcal = nutrients['energy_kcal_100g'] * quantity / 100
            protein = (nutrients['protein_100g'] or 0) * quantity / 100
            carbs = (nutrients['carbs_100g'] or 0) * quantity / 100
            fat = (nutrients['fat_100g'] or 0) * quantity / 100

            df = load_log()
            df = pd.concat([df, pd.DataFrame([{
                'date': datetime.date.today(),
                'food': product.get('product_name', query.title()),
                'quantity_g': quantity,
                'kcal': kcal,
                'protein': protein,
                'carbs': carbs,
                'fat': fat
            }])], ignore_index=True)
            save_log(df)
            st.success(f'Added {query.title()} ({quantity} g)')

# Daily summary
df = load_log()
today = df[df['date'] == pd.Timestamp(datetime.date.today())]

st.subheader('Today\'s Log')
if not today.empty:
    st.dataframe(today[['food', 'quantity_g', 'kcal', 'protein', 'carbs', 'fat']].reset_index(drop=True))

    totals = today[['kcal', 'protein', 'carbs', 'fat']].sum()
    st.subheader('Totals for Today')
    st.write(totals.to_frame(name='Total').T)
else:
    st.write('No entries yet today.')

st.markdown('---')
st.caption('Data source: OpenFoodFacts • App created with Streamlit')
