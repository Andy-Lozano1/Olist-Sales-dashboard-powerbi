import pandas as pd
import numpy as np
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt

print("🔄 Conectando a la base de datos...")

conn = psycopg2.connect(
    host="localhost",
    database="olist_ecommerce",
    user="postgres",
    password="TU_CONTRASEÑA_AQUÍ"  
)

query = """
SELECT o.order_id, c.customer_unique_id, o.order_purchase_timestamp, c.customer_state
FROM ordenes o
JOIN clientes c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered';
"""

df = pd.read_sql_query(query, conn)
conn.close()

print("✅ ¡Datos cargados con éxito!")
print(f"📊 Total de filas importadas: {len(df)}")


print("\n⚙️ Calculando cohortes de retención...")

# Convertir la columna de tiempo a formato de fecha real en Python
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

df['mes_pedido'] = df['order_purchase_timestamp'].dt.to_period('M')

df['cohorte'] = df.groupby('customer_unique_id')['mes_pedido'].transform('min')

cohort_data = df.groupby(['cohorte', 'mes_pedido']).agg(clientes_unicos=('customer_unique_id', 'nunique')).reset_index()

cohort_data = df.groupby(['cohorte', 'mes_pedido']).agg(clientes_unicos=('customer_unique_id', 'nunique')).reset_index()
cohort_data['periodo_meses'] = (cohort_data['mes_pedido'] - cohort_data['cohorte']).apply(lambda x: x.n)

cohort_pivot = cohort_data.pivot(index='cohorte', columns='periodo_meses', values='clientes_unicos')

#Convertir los números a porcentajes (%) basados en el mes 0
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0) * 100


print("📊 Generando mapa de calor de retención...")

cohortes_2017 = [f'2017-0{i}' for i in range(1, 10)] + [f'2017-{i}' for i in range(10, 13)]
matriz_grafico = retention_matrix.loc[cohortes_2017, 0:6] # Ver del mes 0 al mes 6

plt.figure(figsize=(12, 8))
sns.heatmap(
    matriz_grafico, 
    annot=True,          
    fmt=".1f",           
    cmap="YlGnBu",       
    vmin=0, vmax=5       
)

plt.title('Matriz de Retención de Clientes - E-Commerce Olist (2017)', fontsize=14, fontweight='bold')
plt.xlabel('Meses transcurridos después de la primera compra', fontsize=12)
plt.ylabel('Cohorte (Mes de registro)', fontsize=12)

plt.savefig('mapa_calor_retencion.png', bbox_inches='tight', dpi=300)
print("💾 ¡Gráfico guardado con éxito como 'mapa_calor_retencion.png'!")
