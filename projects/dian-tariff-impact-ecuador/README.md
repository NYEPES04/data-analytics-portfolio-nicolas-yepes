# Aranceles de Ecuador a Colombia: impacto sobre exportaciones no minero-energéticas

Estimación del impacto estructural de un arancel del 50% sobre las exportaciones de Colombia hacia Ecuador usando elasticidades-precio por subpartida HS6.

## Objetivo
Cuantificar cuánto se reducirían las exportaciones no minero-energéticas si el arancel del 50% impuesto por Ecuador se mantiene, utilizando un enfoque de elasticidad-precio basado en datos históricos.
Este ejercicio NO es un forecast de exportaciones 2026. Es una simulación estructural del efecto del arancel sobre una base real observada (2025).
---

## Datos
- Fuente: DIAN / DANE – Declaraciones de exportación (DEX)
- Periodo: 2023–2025
- Universo:
  - Exportaciones de Colombia a Ecuador
  - Exclusión: HS2 = 26, 27, 71 (minero-energéticos)

Total procesado:
- ~3.8 millones de registros originales
- ~460 mil registros tras limpieza

---

## Metodología

### 1. Construcción del panel
Agregación mensual por:
- HS6
- Unidad física

### 2. Estimación de elasticidad
Modelo log-log por celda:

ln(cantidad) = alpha + beta * ln(precio)

- Mínimo 18 observaciones
- Winsorización al 2%
- Guardrails: beta ∈ [-3.0, -0.1]

### 3. Shock arancelario

shock_log = lambda * ln(1 + phi * tau)

qty_new = qty_base * exp(beta * shock_log)

### Parámetros clave:
- tau = 50% (desde febrero 2026)
- phi = 1.0 (traslado completo)
- lambda dinámico:
  - Q1: 0.20
  - Q2: 0.60
  - Q3: 0.80
  - Q4: 1.00

---

## Resultados principales

- Elasticidad agregada: ~ -1.0
- Caída estimada:
  - ~7% en febrero
  - ~29% en diciembre (efecto pleno)
- FOB perdido estimado:
  - ~USD 333M (phi=1.0)

Sectores más afectados:
- Vehículos y autopartes
- Cosméticos
- Farmacéuticos
- Manufacturas diversas

---

## Interpretación

Este modelo:
✔ Aísla el efecto del arancel  
✔ Usa datos reales observados  
✔ Permite comparar escenarios  

Este modelo NO:
✘ Proyecta exportaciones 2026  
✘ Incluye tipo de cambio  
✘ Modela sustitución de proveedores  
✘ Incluye crecimiento económico  

---

## Validación (enero 2026)

- El modelo predice caída bajo tau=30%
- El dato real muestra un comportamiento atípico
- Interpretación: front-loading (anticipación de exportaciones)

---

## Estructura del proyecto

- `notebooks/`: modelo completo
- `outputs/`: resultados y visualizaciones

---

## Cómo reproducir

```bash
pip install -r requirements.txt
