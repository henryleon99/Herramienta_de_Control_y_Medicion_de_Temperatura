import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, StringVar, OptionMenu
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import pandas as pd
from datetime import datetime, timedelta

# =======================
# Configuración inicial de productos
# =======================
productos = [
    {"nombre": "Arroz", "rango": (15,25)},
    {"nombre": "Frijoles", "rango": (16,24)},
    {"nombre": "Azúcar", "rango": (18,30)},
    {"nombre": "Café", "rango": (14,22)},
    {"nombre": "Harina", "rango": (16,26)},
    {"nombre": "Lentejas", "rango": (15,25)},
    {"nombre": "Galletas", "rango": (18,28)},
    {"nombre": "Aceite", "rango": (20,30)},
    {"nombre": "Sal", "rango": (15,25)},
    {"nombre": "Leche en polvo", "rango": (14,22)}
]

# =======================
# Generación de datos simulados (últimos 5 días con 24h cada uno)
# =======================
hoy = datetime.now().date()
fechas = [hoy - timedelta(days=i) for i in range(4,-1,-1)]  # 5 días

def generar_temp(rango):
    min_, max_ = rango
    if random.random() < 0.75:
        return random.randint(min_, max_)
    else:
        return max_ + random.randint(1,3)

def generar_datos():
    matriz_temperaturas = []
    for fecha in fechas:
        for hora in range(24):
            temps = [generar_temp(p["rango"]) for p in productos]
            matriz_temperaturas.append([fecha, f"{hora:02d}:00"] + temps)
    columnas = ["Fecha","Hora"]+[p["nombre"] for p in productos]
    return pd.DataFrame(matriz_temperaturas, columns=columnas)

df = generar_datos()

# =======================
# Crear ventana raíz
# =======================
root = tk.Tk()
root.title("Herramienta de Control de Temperatura")
try:
    root.state("zoomed")
except:
    root.attributes("-fullscreen", False)

# =======================
# Pantalla 0: Presentación
# =======================
frame_presentacion = tk.Frame(root)
frame_presentacion.pack(fill="both", expand=True)

titulo = tk.Label(frame_presentacion,
                  text="Herramienta de Control y Medición de \nTemperatura para Productos No \nPerecederos en Bodega Comercial",
                  font=("Arial", 26, "bold"), justify="center")
titulo.pack(expand=True, pady=60)

btn_frame = tk.Frame(frame_presentacion)
btn_frame.pack(pady=30)

btn_ir_principal = tk.Button(btn_frame, text="Ir a la Herramienta ▶", font=("Arial", 14),
                             command=lambda: mostrar_frame(frame_principal))
btn_ir_principal.pack(side="left", padx=15)

btn_salir = tk.Button(btn_frame, text="❌ Salir", font=("Arial", 14), command=root.quit)
btn_salir.pack(side="left", padx=15)

# =======================
# Pantalla 1: Principal
# =======================
frame_principal = tk.Frame(root)

hora_label = tk.Label(frame_principal, text="Hora: --:--", font=("Arial", 16, "bold"))
hora_label.pack(side=tk.TOP, pady=5)

fig = plt.Figure(figsize=(12,7))
gs = fig.add_gridspec(2, 2, width_ratios=[1,1], height_ratios=[1,1], wspace=0.3, hspace=0.5)
ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0])
ax_table = fig.add_subplot(gs[0,1])
ax_line = fig.add_subplot(gs[1,1])

canvas = FigureCanvasTkAgg(fig, master=frame_principal)
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

ani = None
sobrepasos_totales = []
sobrepasos_acumulados = []
datos_dia = []

def update(frame):
    if frame >= 24:
        return
    fila = datos_dia[frame]
    fecha_str, hora_str, *temps = fila
    hora_label.config(text=f"Fecha: {fecha_str} | Hora: {hora_str}")

    etiquetas = [f"{p['nombre']}\n({p['rango'][0]}-{p['rango'][1]}°C)" for p in productos]
    n = len(productos)
    idx = list(range(n))

    # --- Barras ---
    ax1.clear()
    ax1.set_ylim(0,35)
    ax1.set_title("Temperatura por hora", fontweight="bold")
    ax1.set_ylabel("Temperatura (°C)")
    bars = ax1.bar(idx, temps, color="blue")
    ax1.set_xticks(idx)
    ax1.set_xticklabels(etiquetas, rotation=45, ha="right")
    for bar, temp in zip(bars, temps):
        ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                 f"{temp}°C", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # --- Sobrepasos ---
    for i,t in enumerate(temps):
        if t < productos[i]["rango"][0] or t > productos[i]["rango"][1]:
            sobrepasos_totales[i] += 1
    sobrepasos_acumulados.append(sobrepasos_totales.copy())

    ax2.clear()
    ax2.set_title("Número de veces fuera de rango", fontweight="bold")
    ax2.set_ylabel("Cantidad de veces")
    bars2 = ax2.bar(idx, sobrepasos_totales, color="orange")
    ax2.set_xticks(idx)
    ax2.set_xticklabels([p["nombre"] for p in productos], rotation=45, ha="right")
    for bar,val in zip(bars2, sobrepasos_totales):
        ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                 str(val), ha="center", va="bottom", fontsize=8, fontweight="bold")

    # --- Matriz ---
    ax_table.clear()
    ax_table.axis("off")
    ax_table.set_title("Matriz de temperaturas", fontweight="bold")
    header = ["Hora"]+[p["nombre"] for p in productos]
    rows = [header]+[d[1:] for d in datos_dia[:frame+1]]
    tabla = ax_table.table(cellText=rows, loc="center", cellLoc="center")
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(7)
    tabla.scale(1, 0.79)  # 🔹 Reducir altura de las celdas

    # --- Promedio ---
    ax_line.clear()
    promedios = [sum([fila[i+2] for fila in datos_dia[:frame+1]])/(frame+1) for i in range(len(productos))]
    ax_line.plot(idx, promedios, marker="o", color="green")
    ax_line.set_ylim(0,35)
    ax_line.set_title("Promedio por producto", fontweight="bold")
    ax_line.set_ylabel("Temperatura promedio (°C)")
    ax_line.set_xticks(idx)
    ax_line.set_xticklabels(etiquetas, rotation=45, ha="right")
    for i,val in enumerate(promedios):
        ax_line.text(i, val+0.5, f"{val:.1f}°C", ha="center", va="bottom", fontsize=8, fontweight="bold")

    canvas.draw_idle()

def iniciar_animacion():
    global ani, sobrepasos_totales, sobrepasos_acumulados, datos_dia, df
    df = generar_datos()
    ultimo_dia = df["Fecha"].max()
    datos_dia = df[df["Fecha"]==ultimo_dia].values.tolist()
    sobrepasos_totales = [0]*len(productos)
    sobrepasos_acumulados = []
    if ani is not None:
        try: ani.event_source.stop()
        except: pass
    ani = animation.FuncAnimation(fig, update, frames=24, interval=500, repeat=False)
    canvas.draw_idle()

# =======================
# Exportar Excel
# =======================
def exportar_excel():
    win = Toplevel(root)
    win.title("Seleccionar rango de fechas")
    tk.Label(win, text="Fecha inicial:").pack()
    entry_inicio = DateEntry(win, date_pattern="yyyy-mm-dd", mindate=min(fechas), maxdate=max(fechas))
    entry_inicio.pack()
    tk.Label(win, text="Fecha final:").pack()
    entry_fin = DateEntry(win, date_pattern="yyyy-mm-dd", mindate=min(fechas), maxdate=max(fechas))
    entry_fin.pack()

    def confirmar():
        ini, fin = entry_inicio.get_date(), entry_fin.get_date()
        df_filtrado = df[(df["Fecha"]>=ini)&(df["Fecha"]<=fin)]
        if df_filtrado.empty:
            messagebox.showwarning("Aviso", "No hay datos en ese rango.")
            return
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if archivo:
            df_filtrado.to_excel(archivo, index=False)
            messagebox.showinfo("Éxito", f"Datos exportados a {archivo}")
            win.destroy()
    tk.Button(win, text="Exportar", command=confirmar).pack(pady=10)

# =======================
# Agregar/Quitar producto
# =======================
def agregar_producto():
    win = Toplevel(root); win.title("Agregar producto")
    tk.Label(win, text="Nombre:").pack(); e1=tk.Entry(win); e1.pack()
    tk.Label(win, text="Rango mínimo:").pack(); e2=tk.Entry(win); e2.pack()
    tk.Label(win, text="Rango máximo:").pack(); e3=tk.Entry(win); e3.pack()
    def confirmar():
        try:
            productos.append({"nombre":e1.get(), "rango":(int(e2.get()), int(e3.get()))})
            iniciar_animacion(); win.destroy()
        except: messagebox.showerror("Error","Datos inválidos")
    tk.Button(win, text="Agregar", command=confirmar).pack()

def quitar_producto():
    nombres=[p["nombre"] for p in productos]
    if not nombres: return
    win = Toplevel(root); win.title("Quitar producto")
    var=StringVar(win); var.set(nombres[0])
    OptionMenu(win,var,*nombres).pack()
    def confirmar():
        productos[:] = [p for p in productos if p["nombre"]!=var.get()]
        iniciar_animacion(); win.destroy()
    tk.Button(win,text="Eliminar",command=confirmar).pack()

# =======================
# Pantalla 2: Proyección
# =======================
def abrir_proyeccion():
    riesgos={p["nombre"]:0 for p in productos}
    for _,row in df.iterrows():
        for i,p in enumerate(productos):
            t=row[p["nombre"]]
            if t<p["rango"][0] or t>p["rango"][1]:
                riesgos[p["nombre"]]+=1
    riesgos_sorted=dict(sorted(riesgos.items(), key=lambda x:x[1], reverse=True))
    top3=dict(list(riesgos_sorted.items())[:3])
    proyeccion={k:(v/5)*4 for k,v in riesgos_sorted.items()}
    total=sum(proyeccion.values()) or 1
    acum,porcent=0,[]
    for v in proyeccion.values():
        acum+=v; porcent.append((acum/total)*100)

    win=Toplevel(root); win.title("Proyección de Riesgos")
    try: win.state("zoomed")
    except: pass

    # 🔹 Botones arriba
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="⬅ Volver a Presentación (Pantalla 0)",
              command=lambda: (mostrar_frame(frame_presentacion), win.destroy())).pack(side="left", padx=5)
    tk.Button(btn_frame, text="⬅ Volver a Principal (Pantalla 1)",
              command=lambda: (mostrar_frame(frame_principal), win.destroy())).pack(side="left", padx=5)
    tk.Button(btn_frame, text="❌ Cerrar Proyección", command=win.destroy).pack(side="left", padx=5)

    # 🔹 Gráficos
    fig2=plt.Figure(figsize=(12, 10))
    gs2=fig2.add_gridspec(2,2,height_ratios=[1,1], hspace=0.3)  # 🔹 Menos altura para el Pareto
    ax_top3=fig2.add_subplot(gs2[0,0]); ax_linea=fig2.add_subplot(gs2[0,1]); ax_pareto=fig2.add_subplot(gs2[1,:])

    # Top3
    idx=list(range(len(top3)))
    bars=ax_top3.bar(idx, top3.values(), color="red")
    ax_top3.set_title("Top 3 productos con mayor riesgo",fontweight="bold")
    ax_top3.set_xticks(idx); ax_top3.set_xticklabels(top3.keys(),rotation=30,ha="right")
    for b,v in zip(bars,top3.values()): ax_top3.text(b.get_x()+b.get_width()/2,v+0.5,str(v),ha="center")

    # Linea
    idx2=list(range(len(riesgos_sorted)))
    ax_linea.plot(idx2,riesgos_sorted.values(),marker="o",color="blue")
    prom=sum(riesgos_sorted.values())/len(riesgos_sorted) if riesgos_sorted else 0
    ax_linea.axhline(prom,color="gray",linestyle="--",label=f"Prom: {prom:.1f}"); ax_linea.legend()
    ax_linea.set_title("Tendencia de Riesgos",fontweight="bold")
    ax_linea.set_xticks(idx2); ax_linea.set_xticklabels(riesgos_sorted.keys(),rotation=45,ha="right")

    # Pareto
    idx3=list(range(len(proyeccion)))
    bars=ax_pareto.bar(idx3, proyeccion.values(), color="purple", alpha=0.6)
    ax_pareto2=ax_pareto.twinx()
    ax_pareto2.plot(idx3, porcent, marker="o", color="red")
    ax_pareto.set_title("Proyección a 4 días (Pareto)", fontweight="bold")
    ax_pareto.set_xticks(idx3); ax_pareto.set_xticklabels(proyeccion.keys(),rotation=45,ha="right")

    canvas2=FigureCanvasTkAgg(fig2,master=win); canvas2.get_tk_widget().pack(fill=tk.BOTH,expand=True)
    tk.Label(win,text="📊 El gráfico de Pareto muestra la proyección a 4 días.\nLas barras son veces fuera de rango y la línea roja el % acumulado.",font=("Arial",11)).pack(pady=8)

# =======================
# Panel lateral de botones en Pantalla Principal
# =======================
frame_botones=tk.Frame(frame_principal); frame_botones.pack(side=tk.RIGHT,fill=tk.Y)
tk.Button(frame_botones,text="▶ Start Simulación",command=iniciar_animacion).pack(fill="x",pady=5)
tk.Button(frame_botones,text="📊 Exportar Excel",command=exportar_excel).pack(fill="x",pady=5)
tk.Button(frame_botones,text="➕ Agregar producto",command=agregar_producto).pack(fill="x",pady=5)
tk.Button(frame_botones,text="➖ Quitar producto",command=quitar_producto).pack(fill="x",pady=5)
tk.Button(frame_botones,text="📈 Ver Proyección",command=abrir_proyeccion).pack(fill="x",pady=5)
tk.Button(frame_botones,text="⬅ Volver a Presentación",command=lambda:mostrar_frame(frame_presentacion)).pack(fill="x",pady=5)
tk.Button(frame_botones,text="❌ Salir",command=root.quit).pack(fill="x",pady=5)

# =======================
# Función mostrar frames
# =======================
def mostrar_frame(frame):
    for f in (frame_presentacion, frame_principal):
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# Mostrar pantalla inicial
mostrar_frame(frame_presentacion)

root.mainloop()
