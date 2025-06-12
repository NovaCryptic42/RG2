import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time as time_module

# Speed of light in m/s
SPEED_OF_LIGHT = 3e8

def calculate_causality(distance, time):
    """
    Calculate if two events are causal based on distance and time separation.
    
    Args:
        distance (float): Spatial separation in meters
        time (float): Time separation in seconds
    
    Returns:
        tuple: (is_causal, speed_ratio)
    """
    if time == 0:
        return False, float('inf')
    
    speed_ratio = distance / time
    is_causal = speed_ratio <= SPEED_OF_LIGHT
    
    return is_causal, speed_ratio

def create_animated_diagram(distance, time, animation_step):
    """
    Crear un diagrama animado simple mostrando rayos de luz e información.
    
    Args:
        distance (float): Separación espacial en metros
        time (float): Separación temporal en segundos
        animation_step (float): Paso de la animación (0.0 a 1.0)
    
    Returns:
        matplotlib.figure.Figure: El diagrama animado
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Posiciones de los eventos
    event_b_pos = np.array([1, 3])  # Evento B (origen)
    event_a_pos = np.array([9, 6])  # Evento A (destino)
    
    # Calcular causalidad
    is_causal, speed_ratio = calculate_causality(distance, time)
    
    # Velocidad de la información relativa a la velocidad de la luz
    info_speed_factor = speed_ratio / SPEED_OF_LIGHT
    
    # Dibujar los puntos de eventos
    ax.plot(event_b_pos[0], event_b_pos[1], 'ro', markersize=15, label='Evento B')
    ax.plot(event_a_pos[0], event_a_pos[1], 'bo', markersize=15, label='Evento A')
    
    # Calcular posiciones actuales de los rayos basado en animation_step
    direction = event_a_pos - event_b_pos
    distance_between = np.linalg.norm(direction)
    direction_normalized = direction / distance_between
    
    # Posición del rayo de luz (siempre a velocidad c)
    light_progress = animation_step * distance_between
    light_pos = event_b_pos + direction_normalized * light_progress
    
    # Posición del rayo de información (velocidad variable)
    if info_speed_factor <= 1.0:  # Causal - más lento o igual que la luz
        info_progress = animation_step * distance_between * info_speed_factor
    else:  # No causal - más rápido que la luz
        info_progress = animation_step * distance_between * info_speed_factor
    
    if info_progress <= distance_between:
        info_pos = event_b_pos + direction_normalized * info_progress
    else:
        info_pos = event_a_pos
    
    # Dibujar trayectorias completas (líneas punteadas)
    ax.plot([event_b_pos[0], event_a_pos[0]], [event_b_pos[1], event_a_pos[1]], 
            'k--', alpha=0.3, linewidth=1, label='Trayectoria')
    
    # Dibujar rayos en movimiento
    if animation_step > 0:
        # Rayo de luz (amarillo)
        if light_progress <= distance_between:
            ax.plot([event_b_pos[0], light_pos[0]], [event_b_pos[1], light_pos[1]], 
                    'gold', linewidth=4, label='Rayo de luz')
            ax.plot(light_pos[0], light_pos[1], 'yo', markersize=8)
        else:
            ax.plot([event_b_pos[0], event_a_pos[0]], [event_b_pos[1], event_a_pos[1]], 
                    'gold', linewidth=4, label='Rayo de luz')
        
        # Rayo de información (verde si causal, rojo si no causal)
        info_color = 'green' if is_causal else 'red'
        info_label = 'Información (causal)' if is_causal else 'Información (no causal)'
        
        if info_progress <= distance_between:
            ax.plot([event_b_pos[0], info_pos[0]], [event_b_pos[1], info_pos[1]], 
                    info_color, linewidth=4, label=info_label)
            ax.plot(info_pos[0], info_pos[1], color=info_color, marker='o', markersize=8)
        else:
            ax.plot([event_b_pos[0], event_a_pos[0]], [event_b_pos[1], event_a_pos[1]], 
                    info_color, linewidth=4, label=info_label)
    
    # Configurar el gráfico
    ax.set_xlim(0, 10)
    ax.set_ylim(2, 7)
    ax.set_xlabel('Posición', fontsize=12)
    ax.set_ylabel('Posición', fontsize=12)
    ax.set_title('Análisis de Causalidad - Rayos de Luz e Información', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Añadir texto explicativo
    status_text = "CAUSAL" if is_causal else "NO CAUSAL"
    status_color = "green" if is_causal else "red"
    
    ax.text(0.5, 6.5, f"Estado: {status_text}", fontsize=14, fontweight='bold', 
            color=status_color, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    ax.text(0.5, 6.2, f"Velocidad requerida: {speed_ratio:.2e} m/s", fontsize=10)
    ax.text(0.5, 5.9, f"Factor de velocidad de luz: {info_speed_factor:.2f}", fontsize=10)
    
    plt.tight_layout()
    return fig

def main():
    """Aplicación principal de Streamlit"""
    
    st.title("Analizador de Causalidad Física")
    st.markdown("### Determina si dos eventos en el espacio-tiempo están causalmente conectados")
    
    st.markdown("""
    Esta aplicación analiza si dos eventos en el espacio-tiempo pueden estar causalmente relacionados basándose en el 
    principio fundamental de que **la información no puede viajar más rápido que la velocidad de la luz** (c = 3×10⁸ m/s).
    """)
    
    # Crear dos columnas para entrada
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Separación Espacial")
        distance = st.number_input(
            "Distancia entre eventos (metros)",
            min_value=0.0,
            value=1e9,
            step=1e6,
            format="%.2e",
            help="Ingresa la distancia espacial entre el Evento B y el Evento A"
        )
    
    with col2:
        st.subheader("Separación Temporal")
        time = st.number_input(
            "Diferencia de tiempo (segundos)",
            min_value=0.001,
            value=5.0,
            step=0.1,
            format="%.3f",
            help="Ingresa el tiempo transcurrido desde el Evento B hasta el Evento A"
        )
    
    # Calcular causalidad
    is_causal, speed_ratio = calculate_causality(distance, time)
    
    # Mostrar resultados
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
    
    # Controles de animación
    st.markdown("---")
    st.subheader("Diagrama Animado")
    
    # Inicializar estado de sesión
    if 'animation_step' not in st.session_state:
        st.session_state.animation_step = 0.0
    if 'is_animating' not in st.session_state:
        st.session_state.is_animating = False
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("Reiniciar Animación", type="primary"):
            st.session_state.animation_step = 0.0
            st.session_state.is_animating = False
        
        if st.button("Iniciar/Pausar Animación"):
            st.session_state.is_animating = not st.session_state.is_animating
        
        # Control manual cuando no está animando
        if not st.session_state.is_animating:
            st.session_state.animation_step = st.slider(
                "Progreso de la animación", 
                0.0, 1.0, 
                st.session_state.animation_step, 
                0.05
            )
    
    with col1:
        # Crear placeholder para la animación
        chart_placeholder = st.empty()
        
        # Lógica de animación usando auto-refresh
        if st.session_state.is_animating:
            st.session_state.animation_step += 0.02
            if st.session_state.animation_step >= 1.0:
                st.session_state.animation_step = 0.0
            
            # Generar y mostrar el frame actual
            fig = create_animated_diagram(distance, time, st.session_state.animation_step)
            chart_placeholder.pyplot(fig)
            
            # Recargar la página para continuar la animación
            st.rerun()
        else:
            # Mostrar frame estático
            fig = create_animated_diagram(distance, time, st.session_state.animation_step)
            chart_placeholder.pyplot(fig)
    
    # Explicación simple
    st.markdown("---")
    st.markdown("""
    **Explicación:** 
    
    El punto rojo (Evento B) envía dos señales hacia el punto azul (Evento A):
    - **Rayo amarillo**: Viaja a la velocidad de la luz (c = 3×10⁸ m/s)
    - **Rayo de información**: Viaja a la velocidad necesaria para la causalidad
    
    Si el rayo de información llega **después** que el rayo de luz → **CAUSAL**
    
    Si el rayo de información llega **antes** que el rayo de luz → **NO CAUSAL**
    """)

if __name__ == "__main__":
    main()
