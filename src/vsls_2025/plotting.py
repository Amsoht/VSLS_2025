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
    layout="grid",   # "grid" | "column" | "dropdown"
    ncols=2,
    **kwargs
):
    """
    Führt eine matplotlib-basierte Funktion aus, fängt ALLE erzeugten Figures ab
    und zeigt sie interaktiv mit Holoviews an.
    """
    # --- plt.show UND display unterdrücken ---
    _orig_show = plt.show
    _orig_close = plt.close
    
    plt.show = lambda *a, **k: None
    plt.ion()  # Interactive mode ON - verhindert automatisches Display
    
    figs_before = set(plt.get_fignums())
    result = func(*args, **kwargs)
    figs_after = set(plt.get_fignums())
    
    new_figs = [plt.figure(i) for i in sorted(figs_after - figs_before)]
    
    print(f"🔍 Gefangene Figures: {len(new_figs)}")
    
    hv_objs = []
    
    for fig_i, fig in enumerate(new_figs, start=1):
        for ax_i, ax in enumerate(fig.axes, start=1):
            title = ax.get_title() or f"Figure {fig.number}"
            xlabel = ax.get_xlabel() or "x"
            ylabel = ax.get_ylabel() or "y"
            
            ax_elements = []
            
            # ---- Lines ----
            for line in ax.get_lines():
                label = line.get_label()
                if label.startswith('_'):
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
                    # Farben extrahieren falls vorhanden
                    colors = col.get_facecolors()
                    if len(colors) == len(offsets):
                        # Mit Farben
                        ax_elements.append(
                            hv.Scatter(
                                (offsets[:, 0], offsets[:, 1], colors[:, 0]),
                                kdims=[xlabel, ylabel], 
                                vdims=['color'],
                                label="Scatter"
                            ).opts(color='color', cmap='viridis')
                        )
                    else:
                        ax_elements.append(
                            hv.Scatter(
                                (offsets[:, 0], offsets[:, 1]),
                                kdims=[xlabel], 
                                vdims=[ylabel],
                                label="Scatter"
                            )
                        )
            
            # ---- Images ----
            for im in ax.images:
                arr = im.get_array()
                ax_elements.append(
                    hv.Image(arr, label="Image").opts(cmap='viridis')
                )
            
            if ax_elements:
                if len(ax_elements) == 1:
                    combined = ax_elements[0].opts(title=title, width=600, height=400)
                else:
                    combined = hv.Overlay(ax_elements).opts(
                        title=title,
                        legend_position='right',
                        width=600, 
                        height=400
                    )
                hv_objs.append((title, combined))
    
    if not hv_objs:
        print("⚠️ Keine plottbaren Objekte gefunden.")
    else:
        if layout == "dropdown":
            # Dropdown-Menü statt Tabs
            panel = hv.HoloMap({name: obj for name, obj in hv_objs}, kdims='Plot')
        elif layout == "grid":
            panel = hv.Layout([obj for _, obj in hv_objs]).cols(ncols)
        else:  # column
            panel = hv.Layout([obj for _, obj in hv_objs]).cols(1)
        
        # 🔥 WICHTIG: shared_axes=False
        panel = panel.opts(shared_axes=False)
        
        display(panel)
    
    # Aufräumen: ALLE Figures schließen
    for fig in new_figs:
        plt.close(fig)
    
    plt.ioff()  # Interactive mode OFF
    plt.show = _orig_show
    
    return result

# =========================
# 4️⃣ Anwendung
# =========================

# Angenommen, du hast:
# baseline = base.find_base(x, y, plot=True)

# Du machst jetzt einfach:
# baseline = run_interactive(base.find_base, x, y, plot=True)

# Fertig! Alle interaktiven Plots erscheinen im Notebook untereinander.