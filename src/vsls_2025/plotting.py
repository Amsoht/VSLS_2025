# =========================
# 2️⃣ Imports
# =========================
import matplotlib.pyplot as plt
import holoviews as hv
hv.extension('bokeh')  # Holoviews interaktive Backend
from IPython.display import display
import numpy as np

# =========================
# 3️⃣ Wrapper Funktion
# =========================
def run_interactive(
    runfunc,
    *args,
    layout="tabs",   # "tabs" | "grid" | "column"
    ncols=2,
    **kwargs
):
    """
    Führt eine matplotlib-basierte Funktion aus, fängt ALLE erzeugten Figures ab
    und zeigt sie interaktiv mit Holoviews an.
    
    layout:
        - "tabs": jeder Plot in eigenem Tab
        - "grid": Grid-Layout
        - "column": untereinander
    """
    # --- plt.show unterdrücken ---
    _orig_show = plt.show
    plt.show = lambda *a, **k: None
    
    figs_before = set(plt.get_fignums())
    result = runfunc(*args, **kwargs)
    figs_after = set(plt.get_fignums())
    new_figs = [plt.figure(i) for i in figs_after - figs_before]
    
    hv_objs = []
    
    for fig_i, fig in enumerate(new_figs, start=1):
        for ax_i, ax in enumerate(fig.axes, start=1):
            title = ax.get_title() or f"Figure {fig_i}, Axes {ax_i}"
            xlabel = ax.get_xlabel() or "x"
            ylabel = ax.get_ylabel() or "y"
            
            # Sammle alle Elemente dieser Axes in einer Liste
            ax_elements = []
            
            # ---- Lines (plot) ----
            for line in ax.get_lines():
                label = line.get_label()
                if label.startswith('_'):  # Matplotlib interne Labels ignorieren
                    label = None
                ax_elements.append(
                    hv.Curve(
                        (line.get_xdata(), line.get_ydata()),
                        kdims=[xlabel], 
                        vdims=[ylabel],
                        label=label or "Curve"
                    )
                )
            
            # ---- Scatter ----
            for col in ax.collections:
                offsets = col.get_offsets()
                if offsets.size > 0:
                    ax_elements.append(
                        hv.Scatter(
                            (offsets[:, 0], offsets[:, 1]),
                            kdims=[xlabel], 
                            vdims=[ylabel],
                            label="Scatter"
                        )
                    )
            
            # ---- Images (imshow) ----
            for im in ax.images:
                arr = im.get_array()
                ax_elements.append(
                    hv.Image(arr, label="Image").opts(cmap='viridis')
                )
            
            # Wenn mehrere Elemente in einer Axes: überlagern mit *
            if ax_elements:
                if len(ax_elements) == 1:
                    combined = ax_elements[0].opts(title=title)
                else:
                    # Overlay: mehrere Kurven/Scatter in einem Plot
                    combined = hv.Overlay(ax_elements).opts(
                        title=title,
                        legend_position='right'
                    )
                hv_objs.append((title, combined))
    
    if not hv_objs:
        print("⚠️ Keine plottbaren Objekte gefunden.")
    else:
        if layout == "tabs":
            panel = hv.Tabs(hv_objs)
        elif layout == "grid":
            # Nur die Plot-Objekte für Layout
            panel = hv.Layout([obj for _, obj in hv_objs]).cols(ncols)
        else:  # column
            panel = hv.Layout([obj for _, obj in hv_objs]).cols(1)
        
        # 🔥 WICHTIG: shared_axes=False für unabhängiges Zoomen!
        panel = panel.opts(shared_axes=False)
        
        display(panel)
    
    plt.show = _orig_show
    plt.close('all')  # Aufräumen
    
    return result

# =========================
# 4️⃣ Anwendung
# =========================

# Angenommen, du hast:
# baseline = base.find_base(x, y, plot=True)

# Du machst jetzt einfach:
# baseline = run_interactive(base.find_base, x, y, plot=True)

# Fertig! Alle interaktiven Plots erscheinen im Notebook untereinander.