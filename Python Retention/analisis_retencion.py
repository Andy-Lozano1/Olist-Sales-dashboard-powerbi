import pandas as pd
import numpy as np
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt

print("🔄 Conectando a la base de datos...")

# 1. Establecer la conexión con tu pgAdmin
conn = psycopg2.connect(
    host="localhost",
    database="olist_ecommerce",
    user="postgres",
    password="4306"  # ⚠️ Pon aquí tu contraseña real
)

# 2. Tu consulta SQL para traer la información de órdenes
query = """
SELECT o.order_id, c.customer_unique_id, o.order_purchase_timestamp, c.customer_state
FROM ordenes o
JOIN clientes c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered';
"""

# 3. Cargar los datos directamente en un DataFrame de Pandas
df = pd.read_sql_query(query, conn)
conn.close()

print("✅ ¡Datos cargados con éxito!")
print(f"📊 Total de filas importadas: {len(df)}")


print("\n⚙️ Calculando cohortes de retención...")

# 4. Convertir la columna de tiempo a formato de fecha real en Python
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 5. Crear el mes del pedido (ej. 2017-01)
df['mes_pedido'] = df['order_purchase_timestamp'].dt.to_period('M')

# 6. Descubrir el mes de la PRIMERA compra de cada cliente (su Cohorte)
df['cohorte'] = df.groupby('customer_unique_id')['mes_pedido'].transform('min')

cohort_data = df.groupby(['cohorte', 'mes_pedido']).agg(clientes_unicos=('customer_unique_id', 'nunique')).reset_index()

# 7. Agrupar por cohorte y mes de pedido para contar clientes únicos
cohort_data = df.groupby(['cohorte', 'mes_pedido']).agg(clientes_unicos=('customer_unique_id', 'nunique')).reset_index()
# 8. Calcular el número de meses que pasaron entre la primera compra y las siguientes
cohort_data['periodo_meses'] = (cohort_data['mes_pedido'] - cohort_data['cohorte']).apply(lambda x: x.n)

# 9. Pivotar la tabla para darle forma de matriz de retención
cohort_pivot = cohort_data.pivot(index='cohorte', columns='periodo_meses', values='clientes_unicos')

# 10. Convertir los números a porcentajes (%) basados en el mes 0
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0) * 100


print("📊 Generando mapa de calor de retención...")

# 11. Seleccionar los datos de todo el año 2017 para el gráfico
cohortes_2017 = [f'2017-0{i}' for i in range(1, 10)] + [f'2017-{i}' for i in range(10, 13)]
matriz_grafico = retention_matrix.loc[cohortes_2017, 0:6] # Ver del mes 0 al mes 6

# 12. Configurar el tamaño y diseño del gráfico
plt.figure(figsize=(12, 8))
sns.heatmap(
    matriz_grafico, 
    annot=True,          # Pone los números porcentuales dentro de los cuadros
    fmt=".1f",           # Muestra solo un decimal (ej. 0.5%)
    cmap="YlGnBu",       # Escala de colores atractiva
    vmin=0, vmax=5       # Escala optimizada para e-commerce
)

plt.title('Matriz de Retención de Clientes - E-Commerce Olist (2017)', fontsize=14, fontweight='bold')
plt.xlabel('Meses transcurridos después de la primera compra', fontsize=12)
plt.ylabel('Cohorte (Mes de registro)', fontsize=12)

# 13. Guardar el gráfico como una imagen real en tu carpeta
plt.savefig('mapa_calor_retencion.png', bbox_inches='tight', dpi=300)
print("💾 ¡Gráfico guardado con éxito como 'mapa_calor_retencion.png'!")
