import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── LOAD DATA ──
df = pd.read_csv('cleaned_dataset.csv')
menu = pd.read_csv('menu_dataset.csv')

# Clean menu
menu = menu.iloc[:51]
menu = menu[menu['Restaurant Name'].notna()]
menu['Price'] = menu['Price'].astype(str).str.replace('₹','').str.replace(',','').str.strip()
menu['Price'] = pd.to_numeric(menu['Price'], errors='coerce')
menu = menu[menu['Price'].notna()]

# Clean ratings and cost
df['Dining_Rating_Clean'] = pd.to_numeric(
    df['Dining Rating'].replace({'New': None, 'N/A': None}), errors='coerce')
df['Cost_Clean'] = pd.to_numeric(
    df['Cost For Two'].replace({'N/A': None}), errors='coerce')

# Cuisine counts
all_cuisines = []
for c in df['Cuisine'].dropna():
    for item in c.split(','):
        all_cuisines.append(item.strip())
cuisine_counts = pd.Series(all_cuisines).value_counts()

# ── STYLING ──
DARK_BG    = '#0F1117'
CARD_BG    = '#1A1D27'
ACCENT1    = '#4F8EF7'
ACCENT2    = '#7B61FF'
ACCENT3    = '#00D4AA'
ACCENT4    = '#FF6B6B'
ACCENT5    = '#FFB347'
TEXT_WHITE = '#FFFFFF'
TEXT_GRAY  = '#9BA3B2'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'text.color': TEXT_WHITE,
    'axes.labelcolor': TEXT_GRAY,
    'xtick.color': TEXT_GRAY,
    'ytick.color': TEXT_GRAY,
})

# ── FIGURE ──
# Wide + tall so header has absolute room at the top
fig = plt.figure(figsize=(26, 24), facecolor=DARK_BG)
fig.patch.set_facecolor(DARK_BG)

# ─────────────────────────────────────────────
# HEADER  — 3 lines, each on its own y-level
# Use figure-fraction coordinates:
#   0.985  →  title
#   0.965  →  location / date
#   0.950  →  author
# The grid starts at 0.920 — well below all three.
# ─────────────────────────────────────────────

# Title — at top, centered, font 15 so it fits without cutting
fig.text(0.5, 0.992,
         'Cloud Kitchen Market Intelligence',
         ha='center', va='top',
         fontsize=15, fontweight='bold', color=TEXT_WHITE)

# Grid starts at 0.955 — safely below the title
gs = fig.add_gridspec(3, 2,
                      left=0.07, right=0.96,
                      top=0.910,
                      bottom=0.07,
                      hspace=0.55, wspace=0.35)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])
ax5 = fig.add_subplot(gs[2, :])

for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2A2D3A')

# ── CHART 1: Top 10 Cuisines ──
top10 = cuisine_counts.head(10)
bar_colors = [ACCENT1 if i < 2 else ACCENT2 if i < 5 else '#3A4A6B'
              for i in range(len(top10))]
bars1 = ax1.barh(top10.index[::-1], top10.values[::-1],
                 color=bar_colors[::-1], height=0.55, edgecolor='none')
ax1.set_title('Top 10 Cuisines by Restaurant Count',
              fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=8)
ax1.set_xlabel('Number of Restaurants', color=TEXT_GRAY, fontsize=9)
ax1.tick_params(axis='y', labelsize=9.5, colors=TEXT_WHITE)
ax1.tick_params(axis='x', labelsize=8)
ax1.set_xlim(0, top10.values.max() + 5)
for bar, val in zip(bars1, top10.values[::-1]):
    ax1.text(val + 0.3, bar.get_y() + bar.get_height()/2,
             str(val), va='center', color=TEXT_WHITE,
             fontsize=9, fontweight='bold')

# ── CHART 2: Pie ──
type_counts = df['Type'].value_counts()
pie_colors  = [ACCENT1, ACCENT3, ACCENT2, ACCENT4, ACCENT5]
wedges, texts, autotexts = ax2.pie(
    type_counts.values,
    labels=None,
    autopct='%1.0f%%',
    colors=pie_colors[:len(type_counts)],
    startangle=140,
    pctdistance=0.78,
    wedgeprops={'edgecolor': DARK_BG, 'linewidth': 2.5},
    radius=0.85
)
for at in autotexts:
    at.set_color(TEXT_WHITE); at.set_fontsize(9); at.set_fontweight('bold')
ax2.set_title('Restaurant Type Mix',
              fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=8)
legend_patches = [mpatches.Patch(color=pie_colors[i], label=type_counts.index[i])
                  for i in range(len(type_counts))]
ax2.legend(handles=legend_patches, loc='lower center',
           bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8,
           frameon=False, labelcolor=TEXT_WHITE)

# ── CHART 3: Rating Distribution ──
ratings = df['Dining_Rating_Clean'].dropna()
n, bins, patches3 = ax3.hist(ratings, bins=8,
                              color=ACCENT1, edgecolor=DARK_BG, linewidth=1.5)
for p in patches3:
    if p.get_x() >= ratings.mean():
        p.set_facecolor(ACCENT3)
ax3.axvline(ratings.mean(), color=ACCENT4, linestyle='--', linewidth=2,
            label=f'Avg Rating: {ratings.mean():.2f}')
ax3.set_title('Dining Rating Distribution',
              fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=8)
ax3.set_xlabel('Rating', color=TEXT_GRAY, fontsize=9)
ax3.set_ylabel('No. of Restaurants', color=TEXT_GRAY, fontsize=9)
ax3.legend(fontsize=9, frameon=False, labelcolor=TEXT_WHITE)
ax3.tick_params(labelsize=8)

# ── CHART 4: Avg Cost by Type ──
cost_by_type = df.groupby('Type')['Cost_Clean'].mean().sort_values(ascending=False)
bar_colors4  = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5]
bars4 = ax4.bar(range(len(cost_by_type)), cost_by_type.values,
                color=bar_colors4[:len(cost_by_type)],
                width=0.5, edgecolor='none')
ax4.set_title('Avg Cost For Two by Restaurant Type',
              fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=8)
ax4.set_ylabel('Average Cost (Rs.)', color=TEXT_GRAY, fontsize=9)
ax4.set_xticks(range(len(cost_by_type)))
ax4.set_xticklabels(cost_by_type.index, rotation=15, ha='right',
                    fontsize=9, color=TEXT_WHITE)
ax4.tick_params(axis='y', labelsize=8)
ax4.set_ylim(0, cost_by_type.values.max() + 200)
for bar, val in zip(bars4, cost_by_type.values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 25,
             f'Rs.{val:.0f}', ha='center', fontsize=8,
             fontweight='bold', color=TEXT_WHITE)

# ── CHART 5: Menu Price by Restaurant — FULL WIDTH ──
menu_avg    = menu.groupby('Restaurant Name')['Price'].mean().sort_values(ascending=False)
full_names  = list(menu_avg.index)
bar_cycle   = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5]
bar_colors5 = [bar_cycle[i % len(bar_cycle)] for i in range(len(menu_avg))]
bars5 = ax5.bar(range(len(menu_avg)), menu_avg.values,
                color=bar_colors5, width=0.4, edgecolor='none')
ax5.set_title('Average Menu Item Price by Restaurant',
              fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=8)
ax5.set_ylabel('Avg Item Price (Rs.)', color=TEXT_GRAY, fontsize=9)
ax5.set_xticks(range(len(menu_avg)))
ax5.set_xticklabels(full_names, rotation=0, fontsize=10, color=TEXT_WHITE)
ax5.tick_params(axis='y', labelsize=9)
ax5.set_xlim(-0.5, len(menu_avg) - 0.5)
ax5.set_ylim(0, menu_avg.values.max() + 60)
for bar, val in zip(bars5, menu_avg.values):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'Rs.{val:.0f}', ha='center', fontsize=10,
             fontweight='bold', color=TEXT_WHITE)

# ── FOOTER ──
fig.text(0.5, 0.022,
         'Data Source: Zomato.com   •   Collected & Analysed by Richa Dhiman ',
         ha='center', fontsize=9, color=TEXT_GRAY)

plt.savefig('analysis_charts.png', dpi=180,
            bbox_inches='tight', facecolor=DARK_BG)
plt.show()
print("\nCharts saved!")