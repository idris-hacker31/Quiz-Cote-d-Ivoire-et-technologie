"""
 quiz_app.py : est une application conçue pour tester 
 la connaissance des utilisateurs sur la culture ivoirienne ainsi
 que sur les technologies modernes indispensable dans notre quotidien,
 surtout la "Sécurité informatique"

 """

import tkinter as tk                   # Importer le module tkinter pour l'interface de l'app
from tkinter import ttk, messagebox
import json, random, os


# CHARGEMENT DU DOSSIER "quiz_data.json" dans le code de l'application
DOSSIER = os.path.dirname(os.path.abspath(__file__))

def charger(ids):
    with open(os.path.join(DOSSIER, "quiz_data.json"), "r", encoding="utf-8") as f:
        toutes = json.load(f)["categories"]
    return [c for c in toutes if c["id"] in ids]

# PALETTE DE COULEURS
BG       = "#0A0E1A"
PANEL    = "#0F1B35"
CARD     = "#132040"
GOLD     = "#FFD700"
GOLD2    = "#FFA500"
VERT_T   = "#00E676"
VERT     = "#4CAF50"
ROUGE    = "#E53935"
TEXTE    = "#FFFFFF"
GRIS     = "#8EAFD4"
O_DEF    = "#0D2456"
O_BRD    = "#1565C0"
O_SEL    = "#1565C0"
O_OK     = "#1B5E20"
O_KO     = "#7F0000"
O_REV    = "#4A148C"
L_BG     = "#1976D2"
L_SEL    = "#E65100"

LETTRES  = ["A", "B", "C", "D"]
T_MAX    = 35
PALIERS  = [
    (1,"100"),(2,"200"),(3,"300"),(4,"500"),
    (5,"1K"),(6,"2K"),(7,"4K"),(8,"8K"),
    (9,"16K"),(10,"32K"),(11,"64K"),(12,"1M"),
]

def P(n, s="normal"): return ("Helvetica", n, s)
def G(n, s="normal"): return ("Georgia",   n, s)



# PANNEAU QUIZ (contenu d'un onglet)
class PanneauQuiz:
    def __init__(self, frame, categories, titre, accent):
        self.f_outer    = frame          # frame parent (onglet)
        self.categories = categories
        self.titre      = titre
        self.accent     = accent

        self.cat        = None
        self.questions  = []
        self.num_q      = 0
        self.total_q    = 0
        self.score      = 0
        self.choix      = None
        self.ordre      = []
        self.verrou     = False
        self.tval       = T_MAX
        self.tjob       = None

        self._creer_scroll()
        self._accueil()

    #  scrollbar de l'application
    def _creer_scroll(self):
        """Canvas scrollable + scrollbar fine et moderne style Claude."""
        for w in self.f_outer.winfo_children():
            w.destroy()

        # Canvas principal (contenu)
        self.canvas = tk.Canvas(self.f_outer, bg=BG,
                                highlightthickness=0, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Canvas scrollbar personnalisée (fine, à droite)
        self.sb_canvas = tk.Canvas(
            self.f_outer, width=10, bg=BG,
            highlightthickness=0, bd=0
        )
        self.sb_canvas.pack(side="right", fill="y")

        # Frame contenu intérieur
        self.f = tk.Frame(self.canvas, bg=BG)
        self.canvas_win = self.canvas.create_window(
            (0, 0), window=self.f, anchor="nw"
        )

        # Connecter le canvas à la scrollbar custom
        self.canvas.configure(yscrollcommand=self._sb_update_from_canvas)

        # État de la scrollbar
        self._sb_visible   = False   # visible seulement au survol
        self._sb_dragging  = False
        self._sb_drag_y    = 0
        self._sb_top       = 0.0    # fraction 0-1 de la position
        self._sb_size      = 1.0    # fraction 0-1 de la taille du curseur
        self._sb_hide_job  = None   # timer pour masquer la scrollbar

        # Bindings redimensionnement
        self.f.bind("<Configure>",      self._on_frame_cfg)
        self.canvas.bind("<Configure>", self._on_canvas_cfg)

        # Molette souris
        self.canvas.bind_all("<MouseWheel>", self._scroll_mouse)
        self.canvas.bind_all("<Button-4>",   self._scroll_mouse)
        self.canvas.bind_all("<Button-5>",   self._scroll_mouse)

        # Survol sur le canvas principal → afficher la scrollbar
        self.canvas.bind("<Enter>", self._sb_show)
        self.canvas.bind("<Leave>", self._sb_schedule_hide)
        self.f.bind("<Enter>",      self._sb_show)
        self.f.bind("<Leave>",      self._sb_schedule_hide)

        # Interactions avec la scrollbar elle-même
        self.sb_canvas.bind("<ButtonPress-1>",   self._sb_click)
        self.sb_canvas.bind("<B1-Motion>",        self._sb_drag)
        self.sb_canvas.bind("<ButtonRelease-1>",  self._sb_release)
        self.sb_canvas.bind("<Enter>",            self._sb_show)
        self.sb_canvas.bind("<Leave>",            self._sb_schedule_hide)

    # Callbacks redimensionnement
    def _on_frame_cfg(self, e=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._sb_update_from_canvas()

    def _on_canvas_cfg(self, e):
        self.canvas.itemconfig(self.canvas_win, width=e.width)
        self._sb_update_from_canvas()

    # Molette
    def _scroll_mouse(self, e):
        if e.num == 4:   self.canvas.yview_scroll(-1, "units")
        elif e.num == 5: self.canvas.yview_scroll(1,  "units")
        else:            self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        self._sb_update_from_canvas()
        self._sb_show()
        self._sb_schedule_hide()

    #  Logique scrollbar custom 
    def _sb_update_from_canvas(self, *args):
        """Lit la position du canvas et met à jour la scrollbar."""
        try:
            top, bottom     = self.canvas.yview()
            self._sb_top    = top
            self._sb_size   = bottom - top
            self._sb_redraw()
        except Exception:
            pass

    def _sb_redraw(self):
        """Dessine le curseur fin et arrondi sur sb_canvas."""
        c = self.sb_canvas
        c.delete("all")

        if not self._sb_visible:
            return

        h = c.winfo_height()
        w = c.winfo_width()
        if h <= 0 or self._sb_size >= 1.0:
            return   # pas besoin de scrollbar si tout est visible

        # Dimensions du curseur
        margin   = 2
        bar_w    = 4   # largeur du curseur en pixels
        x1       = w - margin - bar_w
        x2       = w - margin
        min_h    = 30  # hauteur minimale du curseur

        cursor_h = max(min_h, int(h * self._sb_size))
        y1       = int(h * self._sb_top)
        y2       = y1 + cursor_h

        # Contraindre dans les limites
        if y2 > h: y1 = h - cursor_h; y2 = h
        if y1 < 0: y1 = 0; y2 = cursor_h

        # Couleur : plus claire si drag, normale sinon
        couleur = "#AAAAAA" if self._sb_dragging else "#666666"

        # Dessiner le curseur arrondi (via arc + rectangle)
        r = bar_w // 2   # rayon des coins arrondis
        c.create_arc(x1, y1, x2, y1 + bar_w*2,
                     start=0, extent=180, fill=couleur, outline="")
        c.create_arc(x1, y2 - bar_w*2, x2, y2,
                     start=180, extent=180, fill=couleur, outline="")
        if y2 - y1 > bar_w * 2:
            c.create_rectangle(x1, y1 + r, x2, y2 - r,
                               fill=couleur, outline="")

    # Afficher / masquer
    def _sb_show(self, e=None):
        if self._sb_hide_job:
            self.f_outer.after_cancel(self._sb_hide_job)
            self._sb_hide_job = None
        self._sb_visible = True
        self._sb_redraw()

    def _sb_schedule_hide(self, e=None):
        """Masque la scrollbar après 1,2 secondes d'inactivité."""
        if self._sb_hide_job:
            self.f_outer.after_cancel(self._sb_hide_job)
        self._sb_hide_job = self.f_outer.after(1200, self._sb_hide)

    def _sb_hide(self):
        if not self._sb_dragging:
            self._sb_visible  = False
            self._sb_hide_job = None
            self._sb_redraw()

    # Clic et drag sur la scrollbar
    def _sb_click(self, e):
        self._sb_dragging = True
        self._sb_drag_y   = e.y
        self._sb_show()

    def _sb_drag(self, e):
        if not self._sb_dragging:
            return
        h    = self.sb_canvas.winfo_height()
        dy   = e.y - self._sb_drag_y
        frac = dy / h if h > 0 else 0
        self.canvas.yview_moveto(self._sb_top + frac)
        self._sb_drag_y = e.y
        self._sb_update_from_canvas()

    def _sb_release(self, e):
        self._sb_dragging = False
        self._sb_redraw()
        self._sb_schedule_hide()

    # utilitaires 
    def _vider(self):
        self._stop()
        self._creer_scroll()
        # Connecter le canvas à la scrollbar custom
        self.canvas.configure(yscrollcommand=self._sb_update_from_canvas)
        self.canvas.yview_moveto(0)

    def _stop(self):
        if self.tjob:
            self.f_outer.after_cancel(self.tjob)
            self.tjob = None

    
    # ACCUEIL  — 4 cartes en grille 2×2
    def _accueil(self):
        self._vider()

        # Titre compact
        th = tk.Frame(self.f, bg=BG, pady=8)
        th.pack(fill="x")
        tk.Label(th, text=self.titre, font=G(18,"bold"),
                 bg=BG, fg=self.accent).pack()
        tk.Label(th, text="Choisissez une categorie",
                 font=P(10), bg=BG, fg=GRIS).pack(pady=(2,0))
        tk.Frame(self.f, height=2, bg=self.accent).pack(fill="x", padx=30, pady=(4,6))

        # Grille 2×2 compacte
        grille = tk.Frame(self.f, bg=BG)
        grille.pack(fill="both", expand=True, padx=20, pady=4)
        grille.grid_rowconfigure(0, weight=1)
        grille.grid_rowconfigure(1, weight=1)
        grille.grid_columnconfigure(0, weight=1)
        grille.grid_columnconfigure(1, weight=1)

        for i, cat in enumerate(self.categories):
            r, c = divmod(i, 2)
            self._carte(grille, cat, r, c)

    def _carte(self, parent, cat, row, col):
        coul = cat["couleur"]

        outer = tk.Frame(parent, bg=coul, padx=2, pady=2)
        outer.grid(row=row, column=col, padx=10, pady=8, sticky="nsew")

        inner = tk.Frame(outer, bg=CARD, cursor="hand2", padx=14, pady=10)
        inner.pack(fill="both", expand=True)

        # bande couleur haute
        tk.Frame(inner, height=3, bg=coul).pack(fill="x", pady=(0,6))

        # emoji + titre + description sur une seule colonne compacte
        top_row = tk.Frame(inner, bg=CARD)
        top_row.pack(fill="x")
        tk.Label(top_row, text=cat["emoji"], font=("Helvetica",26),
                 bg=CARD, fg=coul).pack(side="left", padx=(0,10))
        info = tk.Frame(top_row, bg=CARD)
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=cat["titre"].upper(), font=P(11,"bold"),
                 bg=CARD, fg=GOLD, anchor="w").pack(fill="x")
        tk.Label(info, text=cat["description"], font=P(9),
                 bg=CARD, fg=GRIS, wraplength=220,
                 justify="left", anchor="w").pack(fill="x")

        # Bouton JOUER — fond coloré, bien visible
        tk.Button(inner,
                  text="▶  JOUER",
                  font=P(11,"bold"),
                  bg=coul, fg=BG,
                  activebackground=TEXTE, activeforeground=BG,
                  relief="flat", padx=20, pady=8,
                  cursor="hand2", bd=0,
                  command=lambda c=cat: self._demarrer(c)
                  ).pack(pady=(8,2))

        for w in [outer, inner, top_row, info]:
            w.bind("<Button-1>", lambda e, c=cat: self._demarrer(c))

    # ══════════════════════════════════════════
    # DÉMARRAGE DES QUESTIONS
    # ══════════════════════════════════════════
    def _demarrer(self, cat):
        self.cat      = cat
        self.questions= cat["questions"][:]
        random.shuffle(self.questions)
        self.num_q    = 0
        self.total_q  = len(self.questions)
        self.score    = 0
        self.choix    = None
        self.verrou   = False
        self._construire_jeu()
        self._charger_q()

    # ══════════════════════════════════════════
    # INTERFACE JEU  — layout fixe en grille
    # ══════════════════════════════════════════
    def _construire_jeu(self):
        self._vider()
        coul = self.cat["couleur"]

        # ── Ligne 0 : bandeau nav
        nav = tk.Frame(self.f, bg=PANEL, pady=6)
        nav.pack(fill="x")

        tk.Button(nav, text=" ← Accueil ",
                  font=P(10,"bold"),
                  bg=GOLD2, fg=BG,
                  activebackground=GOLD, activeforeground=BG,
                  relief="flat", padx=10, pady=5,
                  cursor="hand2", bd=0,
                  command=self._confirmer_quit
                  ).pack(side="left", padx=12)

        tk.Label(nav,
                 text=f"{self.cat['emoji']}  {self.cat['titre'].upper()}",
                 font=P(12,"bold"), bg=PANEL, fg=coul
                 ).pack(side="left", padx=8)

        self.lbl_score = tk.Label(nav, text="Score : 0",
                                   font=P(12,"bold"), bg=PANEL, fg=GOLD)
        self.lbl_score.pack(side="right", padx=14)

        # ── Ligne 1 : barre de progression + num question + timer
        prog_row = tk.Frame(self.f, bg=BG)
        prog_row.pack(fill="x", padx=14, pady=(4,0))

        self.lbl_num = tk.Label(prog_row, text="", font=P(9),
                                bg=BG, fg=GRIS)
        self.lbl_num.pack(side="left")

        self.canvas_t = tk.Canvas(prog_row, width=46, height=46,
                                   bg=BG, highlightthickness=0)
        self.canvas_t.pack(side="right")
        self._draw_timer(T_MAX)

        sty = ttk.Style()
        sty.theme_use("default")
        sty.configure("G.Horizontal.TProgressbar",
                      troughcolor=PANEL, background=self.accent, thickness=6)
        self.prog = ttk.Progressbar(self.f, style="G.Horizontal.TProgressbar",
                                    orient="horizontal", mode="determinate",
                                    maximum=self.total_q)
        self.prog.pack(fill="x", padx=14, pady=(2,0))

        # ── Corps principal : gauche (question+options) | droite (paliers)
        corps = tk.Frame(self.f, bg=BG)
        corps.pack(fill="both", expand=True, padx=14, pady=4)

        # Gauche
        g = tk.Frame(corps, bg=BG)
        g.pack(side="left", fill="both", expand=True)

        self.lbl_theme = tk.Label(g, text="", font=G(9,"italic"),
                                   bg=BG, fg=GRIS)
        self.lbl_theme.pack(anchor="w", pady=(0,2))

        # Panneau question
        q_out = tk.Frame(g, bg=self.accent, padx=2, pady=2)
        q_out.pack(fill="x")
        q_in = tk.Frame(q_out, bg=PANEL, padx=14, pady=12)
        q_in.pack(fill="both")
        self.lbl_q = tk.Label(q_in, text="", font=G(13,"bold"),
                               bg=PANEL, fg=TEXTE,
                               wraplength=560, justify="center")
        self.lbl_q.pack()

        # Options A/B/C/D
        self.cadre_o = tk.Frame(g, bg=BG)
        self.cadre_o.pack(fill="x", pady=(6,0))
        self.o_out = []; self.o_in = []; self.l_let = []; self.l_txt = []

        for i in range(4):
            r, c = divmod(i, 2)
            out = tk.Frame(self.cadre_o, bg=O_BRD, padx=2, pady=2, cursor="hand2")
            out.grid(row=r, column=c, padx=4, pady=4, sticky="ew")
            self.cadre_o.grid_columnconfigure(c, weight=1)

            inn = tk.Frame(out, bg=O_DEF)
            inn.pack(fill="both")

            lb = tk.Frame(inn, bg=L_BG, width=38, height=38)
            lb.pack(side="left"); lb.pack_propagate(False)
            ll = tk.Label(lb, text=LETTRES[i], font=P(12,"bold"),
                          bg=L_BG, fg=GOLD)
            ll.pack(expand=True)

            lt = tk.Label(inn, text="", font=P(10),
                          bg=O_DEF, fg=TEXTE,
                          wraplength=280, justify="left", padx=8, pady=8)
            lt.pack(side="left", fill="x", expand=True)

            for w in [out, inn, lb, ll, lt]:
                w.bind("<Button-1>", lambda e, x=i: self._select(x))
                w.bind("<Enter>",    lambda e, x=i: self._hon(x))
                w.bind("<Leave>",    lambda e, x=i: self._hoff(x))

            self.o_out.append(out); self.o_in.append(inn)
            self.l_let.append(ll);  self.l_txt.append(lt)

        # Feedback
        self.lbl_fb = tk.Label(g, text="", font=P(10,"bold"),
                                bg=BG, fg=VERT,
                                wraplength=620, justify="left")
        self.lbl_fb.pack(anchor="w", pady=(4,0))

        # ── BOUTON VALIDER — ancré en bas de la colonne gauche
        self.btn_v = tk.Button(
            g,
            text="  ✔   VALIDER MA RÉPONSE  ",
            font=P(13,"bold"),
            bg=self.accent, fg=BG,
            activebackground=TEXTE, activeforeground=BG,
            relief="flat", padx=30, pady=12,
            cursor="hand2", bd=0,
            command=self._valider
        )
        self.btn_v.pack(pady=(8,4))

        # Droite : paliers
        d = tk.Frame(corps, bg=PANEL, width=120, padx=8, pady=8)
        d.pack(side="right", fill="y", padx=(10,0))
        d.pack_propagate(False)
        tk.Label(d, text="PALIERS", font=P(8,"bold"),
                 bg=PANEL, fg=self.accent).pack(pady=(0,4))
        self.pal_wgts = []
        for num, label in reversed(PALIERS):
            lf = tk.Frame(d, bg=PANEL)
            lf.pack(fill="x", pady=1)
            ln = tk.Label(lf, text=f"{num:02d}", font=P(8,"bold"),
                          bg=PANEL, fg=GRIS, width=3)
            ln.pack(side="left")
            lv = tk.Label(lf, text=label, font=P(8),
                          bg=PANEL, fg=GRIS, anchor="w")
            lv.pack(side="left")
            self.pal_wgts.append((num, lf, ln, lv))

    # ══════════════════════════════════════════
    # CHARGER QUESTION
    # ══════════════════════════════════════════
    def _charger_q(self):
        self._stop()
        q = self.questions[self.num_q]
        self.prog["value"] = self.num_q
        self.lbl_num.config(text=f"Question  {self.num_q+1} / {self.total_q}")
        self.lbl_theme.config(text=f"Theme : {q['region']}")
        self.lbl_q.config(text=q["question"])
        self.lbl_fb.config(text="")
        self.lbl_score.config(text=f"Score : {self.score}")

        self.ordre = q["options"][:]
        random.shuffle(self.ordre)
        self.choix  = None
        self.verrou = False

        for i in range(4):
            self.l_txt[i].config(text=self.ordre[i])
            self._col(i, "normal")

        self.btn_v.config(
            text="  ✔   VALIDER MA RÉPONSE  ",  
            bg=self.accent, fg=BG,
            command=self._valider, state="normal")

        self._maj_pal()
        self.tval = T_MAX
        self._tick()

    #  sélection / hover 
    def _select(self, idx):
        if self.verrou: return
        self.choix = idx
        for i in range(4): self._col(i, "selec" if i==idx else "normal")

    def _hon(self, idx):
        if self.verrou or self.choix==idx: return
        self._col(idx, "hover")

    def _hoff(self, idx):
        if self.verrou or self.choix==idx: return
        self._col(idx, "normal")

    def _col(self, idx, e):
        s = {
            "normal": (O_DEF, O_BRD, L_BG,    GOLD,      TEXTE),
            "hover":  ("#0D3470","#1E88E5","#1565C0", GOLD, TEXTE),
            "selec":  (O_SEL,  GOLD,  L_SEL,   BG,        TEXTE),
            "bonne":  (O_OK,  "#4CAF50","#1B5E20","#A5D6A7","#E8F5E9"),
            "mauvaise":(O_KO, "#D32F2F","#B71C1C","#EF9A9A","#FFEBEE"),
            "revele": (O_REV, "#9C27B0","#4A148C","#CE93D8","#F3E5F5"),
        }
        bg,bd,lbg,lfg,tfg = s.get(e, s["normal"])
        self.o_out[idx].config(bg=bd)
        self.o_in[idx].config(bg=bg)
        self.l_let[idx].config(bg=lbg, fg=lfg)
        self.l_txt[idx].config(bg=bg,  fg=tfg)

    # validation 
    def _valider(self):
        if self.choix is None:
            messagebox.showwarning("Attention",
                                   "Selectionnez une reponse (A, B, C ou D).")
            return
        self._stop()
        self.verrou   = True
        bonne         = self.questions[self.num_q]["reponse"]
        choix_txt     = self.ordre[self.choix]
        idx_bonne     = self.ordre.index(bonne)
        expl          = self.questions[self.num_q].get("explication","")
        est_der       = (self.num_q+1 >= self.total_q)
        txt_suiv      = "  🏆  VOIR MON SCORE  " if est_der else "  ➡  QUESTION SUIVANTE  "

        if choix_txt == bonne:
            self.score += 1
            pts = PALIERS[self.num_q][1]
            self._col(self.choix, "bonne")
            fb = f"✅  Bonne reponse !  +{pts} pts"
            if expl: fb += f"\n💡 {expl}"
            self.lbl_fb.config(text=fb, fg="#4CAF50")
            self.btn_v.config(text=txt_suiv,
                              bg="#27AE60", fg=TEXTE,
                              activebackground="#2ECC71",
                              command=self._suivant)
        else:
            self._col(self.choix, "mauvaise")
            self.f_outer.after(600, lambda: self._col(idx_bonne, "revele"))
            fb = f"❌  Mauvaise reponse !  Bonne : {bonne}"
            if expl: fb += f"\n💡 {expl}"
            self.lbl_fb.config(text=fb, fg=ROUGE)
            self.btn_v.config(text=txt_suiv,
                              bg="#C0392B", fg=TEXTE,
                              activebackground=ROUGE,
                              command=self._suivant)

        self.lbl_score.config(text=f"Score : {self.score}")

    def _suivant(self):
        self.num_q += 1
        if self.num_q >= self.total_q: self._resultats()
        else: self._charger_q()

    # ── timer 
    def _tick(self):
        self._draw_timer(self.tval)
        if self.tval <= 0: self._timeout(); return
        self.tval -= 1
        self.tjob = self.f_outer.after(1000, self._tick)

    def _draw_timer(self, val):
        cv = self.canvas_t; cv.delete("all")
        cx=cy=23; r=20
        cv.create_oval(cx-r,cy-r,cx+r,cy+r, fill=PANEL, outline=self.accent, width=2)
        if val > 0:
            ang = 360*val/T_MAX
            c2  = VERT if val>10 else (GOLD if val>5 else ROUGE)
            cv.create_arc(cx-r+3,cy-r+3,cx+r-3,cy+r-3,
                          start=90,extent=-ang,style="arc",outline=c2,width=3)
        c3 = VERT if val>10 else (GOLD if val>5 else ROUGE)
        cv.create_text(cx,cy,text=str(val),font=("Helvetica",12,"bold"),fill=c3)

    def _timeout(self):
        self.verrou   = True
        bonne         = self.questions[self.num_q]["reponse"]
        idx_bonne     = self.ordre.index(bonne)
        self._col(idx_bonne, "revele")
        self.lbl_fb.config(text=f"⏱ Temps ecoule !  Bonne reponse : {bonne}", fg=ROUGE)
        est_der = (self.num_q+1 >= self.total_q)
        self.btn_v.config(
            text="  🏆  VOIR MON SCORE  " if est_der else "  ➡  QUESTION SUIVANTE  ",
            bg="#C0392B", fg=TEXTE, command=self._suivant)

    # ── paliers ──────────────────────────────
    def _maj_pal(self):
        for num,lf,ln,lv in self.pal_wgts:
            if num == self.num_q+1:
                lf.config(bg=GOLD2); ln.config(bg=GOLD2,fg=BG)
                lv.config(bg=GOLD2,fg=BG,font=P(8,"bold"))
            elif num <= self.num_q:
                lf.config(bg=PANEL); ln.config(bg=PANEL,fg=VERT)
                lv.config(bg=PANEL,fg=VERT,font=P(8))
            else:
                lf.config(bg=PANEL); ln.config(bg=PANEL,fg=GRIS)
                lv.config(bg=PANEL,fg=GRIS,font=P(8))

    
    # RÉSULTATS
    # ══════════════════════════════════════════
    def _resultats(self):
        self._vider()
        coul = self.cat["couleur"]
        pct  = round(self.score/self.total_q*100)

        if pct==100: sym,men,cm="CHAMPION !","Score parfait !",GOLD
        elif pct>=80: sym,men,cm="EXCELLENT !","Tres bon niveau !",GOLD
        elif pct>=60: sym,men,cm="TRES BIEN !","Vous vous en sortez bien.",GRIS
        elif pct>=40: sym,men,cm="PAS MAL !","Encore quelques efforts.",GOLD2
        else:         sym,men,cm="COURAGE !","Continuez a apprendre !",ROUGE

        tk.Frame(self.f,height=5,bg=self.accent).pack(fill="x")

        c = tk.Frame(self.f,bg=PANEL,padx=50,pady=20)
        c.pack(fill="both",expand=True,padx=30,pady=12)

        tk.Label(c,text=f"{self.cat['emoji']}  {self.cat['titre'].upper()}",
                 font=P(11),bg=PANEL,fg=coul).pack()
        tk.Label(c,text=sym,font=G(22,"bold"),bg=PANEL,fg=cm).pack(pady=(6,2))
        tk.Label(c,text=men,font=P(11),bg=PANEL,fg=GRIS).pack()

        sf = tk.Frame(c,bg=BG,padx=30,pady=10)
        sf.pack(pady=10,fill="x")
        tk.Label(sf,text=f"{self.score} / {self.total_q}",
                 font=G(36,"bold"),bg=BG,fg=GOLD).pack()
        tk.Label(sf,text=f"soit {pct}% de bonnes reponses",
                 font=P(10),bg=BG,fg=GRIS).pack()

        bar = tk.Frame(c,bg="#1A237E",height=12)
        bar.pack(fill="x",pady=(0,14))
        bar.update_idletasks()
        wf = max(4, int(bar.winfo_width()*self.score/self.total_q))
        tk.Frame(bar,bg=self.accent,height=12,width=wf).place(x=0,y=0)

        btns = tk.Frame(c,bg=PANEL); btns.pack()

        tk.Button(btns, text="  🔄  REJOUER  ",
                  font=P(12,"bold"),
                  bg=self.accent, fg=BG,
                  activebackground=TEXTE, activeforeground=BG,
                  relief="flat", padx=22, pady=10,
                  cursor="hand2", bd=0,
                  command=lambda: self._demarrer(self.cat)
                  ).pack(side="left", padx=10)

        tk.Button(btns, text="  🏠  MENU  ",
                  font=P(12,"bold"),
                  bg="#455A64", fg=TEXTE,
                  activebackground=GRIS, activeforeground=BG,
                  relief="flat", padx=22, pady=10,
                  cursor="hand2", bd=0,
                  command=self._accueil
                  ).pack(side="left", padx=10)

        tk.Frame(self.f,height=4,bg=self.accent).pack(fill="x",side="bottom")

    # ── retour accueil ───────────────────────
    def _confirmer_quit(self):
        self._stop()
        if messagebox.askyesno("Revenir au menu ?",
                               "Votre progression sera perdue.\nConfirmer ?"):
            self._accueil()
        else:
            if not self.verrou: self._tick()


# APPLICATION  — une fenêtre, deux onglets
# ══════════════════════════════════════════════
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz — Cote d'Ivoire & Technologie")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.geometry("980x780")
        self.root.minsize(900, 700)
        self._build()

    def _build(self):
        # ── En-tête (compact)
        h = tk.Frame(self.root, bg=BG, pady=8)
        h.pack(fill="x")
        tk.Label(h, text="★  ★  ★  ★  ★  ★  ★",
                 font=P(10,"bold"), bg=BG, fg=GOLD2).pack()
        tk.Label(h, text="QUIZ INTERACTIF",
                 font=G(20,"bold"), bg=BG, fg=GOLD).pack(pady=(3,1))
        tk.Label(h, text="Cote d'Ivoire  •  Python  •  Cybersecurite",
                 font=G(9,"italic"), bg=BG, fg=GRIS).pack()
        tk.Frame(self.root, height=3, bg=GOLD).pack(fill="x", padx=20)

        # ── Barre onglets
        barre = tk.Frame(self.root, bg="#071428", pady=0)
        barre.pack(fill="x")

        # Conteneur onglets
        self.conteneur = tk.Frame(self.root, bg=BG)
        self.conteneur.pack(fill="both", expand=True)

        # Frames des deux onglets
        self.f_ci   = tk.Frame(self.conteneur, bg=BG)
        self.f_tech = tk.Frame(self.conteneur, bg=BG)

        # Panneaux
        cats_ci   = charger(["culture","gastronomie","sport","ethnies"])
        cats_tech = charger(["python","cybersecurite"])

        self.p_ci   = PanneauQuiz(self.f_ci,   cats_ci,   "QUIZ CÔTE D'IVOIRE", GOLD)
        self.p_tech = PanneauQuiz(self.f_tech, cats_tech, "QUIZ TECHNOLOGIE",   VERT_T)

        # Boutons onglets — grands, colorés, bien visibles
        self.btn_ci = tk.Button(
            barre,
            text="  🇨🇮  CÔTE D'IVOIRE  ",
            font=P(12,"bold"),
            bg=GOLD, fg=BG,
            activebackground=TEXTE, activeforeground=BG,
            relief="flat", padx=18, pady=10,
            cursor="hand2", bd=0,
            command=self._show_ci
        )
        self.btn_ci.pack(side="left", padx=(12,3), pady=6)

        self.btn_tech = tk.Button(
            barre,
            text="  💻  TECHNOLOGIE  ",
            font=P(12,"bold"),
            bg=VERT_T, fg=BG,
            activebackground=TEXTE, activeforeground=BG,
            relief="flat", padx=18, pady=10,
            cursor="hand2", bd=0,
            command=self._show_tech
        )
        self.btn_tech.pack(side="left", padx=3, pady=6)

        # Démarrer sur Côte d'Ivoire
        self._show_ci()

    def _show_ci(self):
        self.f_tech.pack_forget()
        self.f_ci.pack(fill="both", expand=True)
        self.btn_ci.config(bg=GOLD,    fg=BG,    relief="sunken")
        self.btn_tech.config(bg="#004D2E", fg=VERT_T, relief="flat")

    def _show_tech(self):
        self.f_ci.pack_forget()
        self.f_tech.pack(fill="both", expand=True)
        self.btn_tech.config(bg=VERT_T, fg=BG,   relief="sunken")
        self.btn_ci.config(bg="#4A3500",  fg=GOLD, relief="flat")


# 
if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()