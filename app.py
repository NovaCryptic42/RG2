import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

# Speed of light in m/s (more precise value)
SPEED_OF_LIGHT = 299792458

# Configure matplotlib for better performance
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 100

@st.cache_data
def calculate_causality(distance, time_diff):
    """
    Calculate if two events are causal based on distance and time separation.
    
    Args:
        distance (float): Spatial separation in meters
        time_diff (float): Time separation in seconds
    
    Returns:
        tuple: (is_causal, speed_ratio)
    """
    if time_diff == 0:
        return False, float('inf')
    
    speed_ratio = distance / time_diff
    is_causal = speed_ratio <= SPEED_OF_LIGHT
    
    return is_causal, speed_ratio

def create_causality_diagram(distance, time_diff):
    """
    Create a static diagram showing causality analysis.
    
    Args:
        distance (float): Spatial separation in meters
        time_diff (float): Time separation in seconds
    
    Returns:
        matplotlib.figure.Figure: The causality diagram
    """
    fig = Figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    
    # Event positions
    event_a_pos = np.array([1, 3])  # Event A (origin)
    event_b_pos = np.array([9, 6])  # Event B (destination)
    
    # Calculate causality
    is_causal, speed_ratio = calculate_causality(distance, time_diff)
    
    # Information speed factor relative to light speed
    info_speed_factor = speed_ratio / SPEED_OF_LIGHT
    
    # Draw event points
    ax.plot(event_a_pos[0], event_a_pos[1], 'ro', markersize=15, label='Evento A (Origen)', zorder=5)
    ax.plot(event_b_pos[0], event_b_pos[1], 'bo', markersize=15, label='Evento B (Destino)', zorder=5)
    
    # Draw trajectory line
    ax.plot([event_a_pos[0], event_b_pos[0]], [event_a_pos[1], event_b_pos[1]], 
            'k--', alpha=0.5, linewidth=2, label='Trayectoria')
    
    # Draw complete rays
    # Light ray (yellow)
    ax.plot([event_a_pos[0], event_b_pos[0]], [event_a_pos[1], event_b_pos[1]], 
            'gold', linewidth=6, label='Rayo de luz (c)', alpha=0.9)
    
    # Information ray (green if causal, red if non-causal)
    info_color = 'limegreen' if is_causal else 'red'
    info_label = 'Información (CAUSAL)' if is_causal else 'Información (NO CAUSAL)'
    
    ax.plot([event_a_pos[0], event_b_pos[0]], [event_a_pos[1], event_b_pos[1]], 
            info_color, linewidth=6, label=info_label, alpha=0.9)
    
    # Configure the plot
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(1.5, 7.5)
    ax.set_xlabel('Posición Espacial', fontsize=12, fontweight='bold')
    ax.set_ylabel('Posición Espacial', fontsize=12, fontweight='bold')
    ax.set_title('Análisis de Causalidad - Propagación de Información vs Luz', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=1)
    ax.legend(fontsize=11, loc='upper left', framealpha=0.9)
    
    # Add status information box
    status_text = "CAUSAL" if is_causal else "NO CAUSAL"
    status_color = "limegreen" if is_causal else "red"
    
    # Create info box
    info_box = f"""Estado: {status_text}
Velocidad requerida: {speed_ratio:.2e} m/s
Factor vs luz: {info_speed_factor:.2f}x"""
    
    ax.text(0.02, 0.98, info_box, transform=ax.transAxes, fontsize=11, 
            verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", 
                     edgecolor=status_color, linewidth=2, alpha=0.9))
    
    # Add physics explanation
    physics_text = """Principio: Información ≤ Velocidad de la luz
c = 3×10⁸ m/s (máximo universal)"""
    
    ax.text(0.98, 0.02, physics_text, transform=ax.transAxes, fontsize=10, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    fig.tight_layout()
    return fig

def main():
    """Main Streamlit application"""
    
    # Configure page
    st.set_page_config(
        page_title="Analizador de Causalidad Física",
        layout="wide"
    )
    
    st.title("Analizador de Causalidad Física")
    st.markdown("### Determina si dos eventos en el espacio-tiempo están causalmente conectados")
    
    st.markdown("""
    Esta aplicación analiza si dos eventos en el espacio-tiempo pueden estar causalmente relacionados 
    basándose en el principio fundamental de que la información no puede viajar más rápido que la 
    velocidad de la luz (c = 299,792,458 m/s).
    """)
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Separación Espacial")
        distance = st.number_input(
            "Distancia entre eventos (metros)",
            min_value=1.0,
            value=1e9,
            step=1e6,
            format="%.2e",
            help="Ingresa la distancia espacial entre el Evento A y el Evento B"
        )
    
    with col2:
        st.subheader("Separación Temporal")
        time_diff = st.number_input(
            "Diferencia de tiempo (segundos)",
            min_value=0.001,
            value=5.0,
            step=0.1,
            format="%.3f",
            help="Ingresa el tiempo transcurrido desde el Evento A hasta el Evento B"
        )
    
    # Calculate causality
    is_causal, speed_ratio = calculate_causality(distance, time_diff)
    
    # Display results
    st.markdown("---")
    st.subheader("Resultados del Análisis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if is_causal:
            st.success("**EVENTOS CAUSALES**")
            st.markdown("Estos eventos **pueden** estar causalmente conectados.")
        else:
            st.error("**EVENTOS NO CAUSALES**")
            st.markdown("Estos eventos **no pueden** estar causalmente conectados.")
    
    with col2:
        st.metric(
            label="Velocidad de Información Requerida",
            value=f"{speed_ratio:.2e} m/s",
            delta=f"{((speed_ratio/SPEED_OF_LIGHT - 1) * 100):.1f}% vs velocidad de la luz"
        )
    
    with col3:
        st.metric(
            label="Velocidad de la Luz",
            value=f"{SPEED_OF_LIGHT:.0e} m/s",
            delta="Velocidad máxima permitida"
        )
    

    
    # Educational explanation
    st.markdown("---")
    st.subheader("Explicación Física")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **¿Qué estamos viendo?**
        
        - **Evento A (Origen)**: Punto donde se genera la información
        - **Evento B (Destino)**: Punto donde debe llegar la información
        - **Rayo de luz**: Viaja siempre a c = 299,792,458 m/s (límite universal)
        - **Rayo de información**: Velocidad necesaria para la causalidad
        """)
    
    with col2:
        st.markdown("""
        **Interpretación de resultados:**
        
        - **CAUSAL**: La información llega después que la luz
        - **NO CAUSAL**: La información llegaría antes que la luz
        - **Principio**: Ninguna información puede superar la velocidad de la luz
        - **Consecuencia**: Eventos muy distantes no pueden influirse instantáneamente
        """)

if __name__ == "__main__":
    main()
