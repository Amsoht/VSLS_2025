# =========================
# 2️⃣ Imports
# =========================
import matplotlib.pyplot as plt
import holoviews as hv
hv.extension('bokeh')  # Holoviews interaktive Backend
from IPython.display import display

# =========================
# 3️⃣ Wrapper Funktion
# =========================

def run_interactive(find_base_func, *args, **kwargs):
    """
    Führt eine Funktion aus, die Matplotlib-Plots erzeugt (wie `find_base`), 
    fängt alle erzeugten Figures ab und zeigt sie in einem Holoviews Layout interaktiv.
    
    Parameters
    ----------
    find_base_func : callable
        Funktion, die Matplotlib-Plots erzeugt
    *args, **kwargs :
        Argumente für find_base_func
    
    Returns
    -------
    result : any
        Rückgabewert der aufgerufenen Funktion
    """
    
    # ---- Backup von plt.show(), um direktes Anzeigen zu verhindern ----
    _original_show = plt.show
    plt.show = lambda *a, **k: None  # überschreiben
    
    # ---- Liste für abgefangene Figures ----
    figs_before = set(plt.get_fignums())  # Figures vor Funktionsaufruf
    result = find_base_func(*args, **kwargs)
    figs_after = set(plt.get_fignums())   # Figures nach Funktionsaufruf
    
    new_figs = [plt.figure(num) for num in figs_after - figs_before]
    
    # ---- Holoviews Layout bauen ----
    hv_plots = []
    for fig in new_figs:
        for ax in fig.axes:
            for line in ax.get_lines():
                xdata = line.get_xdata()
                ydata = line.get_ydata()
                label = line.get_label()
                hv_plots.append(hv.Curve((xdata, ydata), label=label if label else ax.get_title()))
    
    if hv_plots:
        layout = hv.Layout(hv_plots).cols(1)  # vertikal stapeln
        display(layout)
    
    # ---- plt.show wiederherstellen ----
    plt.show = _original_show
    
    return result

# =========================
# 4️⃣ Anwendung
# =========================

# Angenommen, du hast:
# baseline = base.find_base(x, y, plot=True)

# Du machst jetzt einfach:
# baseline = run_interactive(base.find_base, x, y, plot=True)

# Fertig! Alle interaktiven Plots erscheinen im Notebook untereinander.