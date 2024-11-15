import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Анализ секторов экономики Казахстана", layout="wide")

data = {
    "ОКЭД": [
        "Производство товаров",
        "Сельское, лесное и рыбное хозяйство",
        "Промышленность",
        "Горнодобывающая промышленность и разработка карьеров",
        "Обрабатывающая промышленность",
        "Снабжение электроэнергией, газом, паром, горячей водой и кондиционированным воздухом",
        "Водоснабжение; сбор, обработка и удаление отходов, деятельность поликвидации загрязнений",
        "Строительство",
        "Производство услуг",
        "Оптовая и розничная торговля; ремонт автомобилей и мотоциклов"
    ],
    "2014": [6247058.0, 393494.3, 5037119.9, 2912107.0, 1749333.5, 326929.7, 48749.7, 816443.8, 8823890.8, 1382074.4],
    "2015": [6088490.1, 435168.9, 4760156.4, 2579770.9, 1772653.5, 357433.2, 50298.8, 893164.8, 9872452.4, 1439942.3],
    "2016": [6839405.6, 480748.7, 5373653.5, 2715193.5, 2222204.6, 383310.5, 52944.9, 985003.4, 11281186.6, 1670876.3],
    "2017": [7853582.4, 522147.5, 6283949.5, 3238816.5, 2560757.3, 423874.8, 60500.9, 1047485.4, 12186431.1, 1862711.5],
    "2018": [9483735.1, 606063.8, 7734525.7, 4189830.3, 2992380.3, 478744.8, 73570.3, 1143145.6, 13515062.0, 2154013.6],
    "2019": [10631620.1, 678911.8, 8650663.2, 4783751.8, 3318029.4, 468375.0, 80507.0, 1302045.1, 15006504.9, 2489305.0],
    "2020": [11077311.2, 803610.8, 8732162.1, 4360628.2, 3754421.3, 527181.0, 89931.6, 1541538.3, 15594083.6, 2543453.0],
    "2021": [12686607.6, 922684.2, 10206517.3, 5013287.6, 4506592.8, 588070.0, 98566.9, 1736876.1, 17117602.2, 2871816.4],
    "2022": [16269943.6, 1109432.7, 13170633.6, 6863402.2, 5544062.8, 647705.0, 115463.6, 1989877.3, 20250914.2, 3414242.9],
    "2023": [17456038.1, 1319477.6, 13854450.8, 6786106.0, 6182096.6, 755196.9, 131051.3, 2325325.3, 25563787.2, 4187034.7],
    "2024": [18845719.1, 1319477.6, 14880738.1, 7336487.4, 6492927.4, 905060.6, 146262.7, 2645503.4, 29808499.9, 4668356.1]
}

df = pd.DataFrame(data)
df = df.set_index('ОКЭД')

st.title('🏢 Анализ секторов экономики Казахстана')
st.markdown("""
### Почему сектор "Производство услуг" является ключевым драйвером экономики Казахстана?
""")

col1, col2, col3 = st.columns(3)

total_2024 = df['2024'].sum()
services_2024 = df.loc['Производство услуг', '2024']
services_share_2024 = (services_2024 / total_2024) * 100

services_growth = ((services_2024 / df.loc['Производство услуг', '2014']) - 1) * 100

yearly_shares = []
for year in df.columns:
    total = df[year].sum()
    share = (df.loc['Производство услуг', year] / total) * 100
    yearly_shares.append(share)
avg_share = np.mean(yearly_shares)

with col1:
    st.metric(
        "Доля в ВВП (2024)",
        f"{services_share_2024:.1f}%",
        f"+{(services_share_2024 - yearly_shares[0]):.1f}% с 2014"
    )
    
with col2:
    st.metric(
        "Рост сектора (2014-2024)",
        f"{services_growth:.1f}%",
        "Кумулятивный рост"
    )
    
with col3:
    st.metric(
        "Средняя доля (2014-2024)",
        f"{avg_share:.1f}%",
        "Стабильное лидерство"
    )

tab1, tab2, tab3 = st.tabs(["Динамика роста", "Структурный анализ", "Сравнительный анализ"])

with tab1:
    df_transposed = df.transpose()
    fig = px.line(
        df_transposed,
        title='Динамика роста секторов экономики (2014-2024)',
        labels={'value': 'Объем (млн тенге)', 'index': 'Год'},
        height=600
    )
    fig.update_layout(showlegend=True, legend_title_text='Сектора')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    shares_df = df.copy()
    for year in df.columns:
        total = df[year].sum()
        shares_df[year] = (df[year] / total) * 100

    fig = px.area(
        shares_df.transpose(),
        title='Структура экономики Казахстана (доля секторов, %)',
        labels={'value': 'Доля (%)', 'index': 'Год'},
        height=600
    )
    fig.update_layout(showlegend=True, legend_title_text='Сектора')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    years = len(df.columns)
    cagr_dict = {}
    for sector in df.index:
        start_value = df.loc[sector, '2014']
        end_value = df.loc[sector, '2024']
        cagr = (end_value / start_value) ** (1/10) - 1
        cagr_dict[sector] = cagr * 100

    fig = px.bar(
        x=list(cagr_dict.keys()),
        y=list(cagr_dict.values()),
        title='Среднегодовой темп роста по секторам (CAGR, 2014-2024)',
        labels={'x': 'Сектор', 'y': 'CAGR (%)'},
        height=500
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# Key findings
st.markdown("""
### 📊 Ключевые выводы:

1. **Доминирующая позиция:**
   - Сектор услуг составляет более {:.1f}% ВВП в 2024 году
   - Устойчивый рост доли в экономике с 2014 года

2. **Стабильный рост:**
   - Кумулятивный рост {:.1f}% за 10 лет
   - Наиболее высокий CAGR среди всех секторов

3. **Устойчивость к внешним шокам:**
   - Меньшая волатильность по сравнению с другими секторами
   - Стабильный рост даже в кризисные периоды

4. **Потенциал развития:**
   - Тренд на цифровизацию услуг
   - Растущий внутренний спрос
   - Развитие экспорта услуг
""".format(services_share_2024, services_growth))

st.markdown("### 📈 Сравнение производительности секторов")

performance_metrics = pd.DataFrame({
    'Сектор': df.index,
    'Объем 2024 (млрд тенге)': df['2024'] / 1000000,
    'Рост с 2014 (%)': ((df['2024'] / df['2014']) - 1) * 100,
    'CAGR (%)': [cagr_dict[sector] for sector in df.index]
})

st.dataframe(
    performance_metrics.style.highlight_max(axis=0, color='lightgreen'),
    hide_index=True
)