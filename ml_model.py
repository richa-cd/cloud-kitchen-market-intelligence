
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# ── LOAD DATA ──
df = pd.read_csv('cleaned_dataset.csv')

# ── CLEAN DATA ──
df['Cost_Clean'] = pd.to_numeric(
    df['Cost For Two'].replace({'N/A': None}), errors='coerce')
df['Rating_Clean'] = pd.to_numeric(
    df['Dining Rating'].replace({'New': None, 'N/A': None}), errors='coerce')

df = df.dropna(subset=['Cost_Clean'])
df['Rating_Clean'] = df['Rating_Clean'].fillna(df['Rating_Clean'].mean())
df['Type'] = df['Type'].fillna('Unknown')
df['Cuisine'] = df['Cuisine'].fillna('Unknown')

# ── FEATURE ENGINEERING ──
df['Primary_Cuisine'] = df['Cuisine'].apply(lambda x: x.split(',')[0].strip())

le_cuisine = LabelEncoder()
le_type    = LabelEncoder()
df['Cuisine_Encoded'] = le_cuisine.fit_transform(df['Primary_Cuisine'])
df['Type_Encoded']    = le_type.fit_transform(df['Type'])

features = ['Rating_Clean', 'Cuisine_Encoded', 'Type_Encoded']
X = df[features]
y = df['Cost_Clean']

print("="*55)
print("  CLOUD KITCHEN ML PRICE PREDICTOR")
print("  Gangapur Road, Nashik")
print("="*55)
print(f"\n  Dataset size: {len(df)} restaurants")
print(f"  Features used: Rating, Cuisine Type, Restaurant Type")
print(f"  Target: Cost For Two (Rs.)")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

print(f"\n  Training samples: {len(X_train)}")
print(f"  Testing samples:  {len(X_test)}")

lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
lr_mae  = mean_absolute_error(y_test, lr_pred)
lr_r2   = r2_score(y_test, lr_pred)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_mae  = mean_absolute_error(y_test, rf_pred)
rf_r2   = r2_score(y_test, rf_pred)

print("\n" + "="*55)
print("  MODEL RESULTS")
print("="*55)
print(f"\n  Linear Regression:")
print(f"    Mean Absolute Error : Rs.{lr_mae:.0f}")
print(f"    R2 Score            : {lr_r2:.2f}")
print(f"\n  Random Forest:")
print(f"    Mean Absolute Error : Rs.{rf_mae:.0f}")
print(f"    R2 Score            : {rf_r2:.2f}")

best_model = "Random Forest" if rf_r2 > lr_r2 else "Linear Regression"
print(f"\n  Best Model: {best_model} ✓")

print("\n" + "="*55)
print("  SAMPLE PREDICTIONS (Random Forest)")
print("="*55)

test_cases = [
    {"name": "New Thai Cloud Kitchen",    "rating": 4.2, "cuisine": "North Indian", "type": "Cloud Kitchen"},
    {"name": "Premium Dine-In Restaurant","rating": 4.5, "cuisine": "Continental",  "type": "Dine-In"},
    {"name": "Budget Cafe",               "rating": 3.8, "cuisine": "Fast Food",    "type": "Cafe"},
    {"name": "New Restaurant (No Rating)","rating": 4.0, "cuisine": "Chinese",      "type": "Dine-In"},
]

print(f"\n  {'Restaurant':<30} {'Predicted Cost For Two':>22}")
print(f"  {'-'*52}")
for case in test_cases:
    try:    cuisine_enc = le_cuisine.transform([case['cuisine']])[0]
    except: cuisine_enc = 0
    try:    type_enc = le_type.transform([case['type']])[0]
    except: type_enc = 0
    input_data = pd.DataFrame([[case['rating'], cuisine_enc, type_enc]], columns=features)
    pred = rf.predict(input_data)[0]
    print(f"  {case['name']:<30} Rs.{pred:>8.0f}")

print("\n" + "="*55)
print("  FEATURE IMPORTANCE (What affects price most?)")
print("="*55)
importance = pd.Series(rf.feature_importances_,
                       index=['Rating', 'Cuisine', 'Restaurant Type'])
importance = importance.sort_values(ascending=False)
for feat, imp in importance.items():
    bar = '█' * int(imp * 40)
    print(f"  {feat:<18} {bar} {imp:.1%}")

# ── STYLING ──
DARK_BG    = '#0F1117'
CARD_BG    = '#1A1D27'
ACCENT1    = '#4F8EF7'
ACCENT2    = '#7B61FF'
ACCENT3    = '#00D4AA'
ACCENT4    = '#FF6B6B'
TEXT_WHITE = '#FFFFFF'
TEXT_GRAY  = '#9BA3B2'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'text.color': TEXT_WHITE,
    'axes.labelcolor': TEXT_GRAY,
    'xtick.color': TEXT_GRAY,
    'ytick.color': TEXT_GRAY,
})

# ── FIGURE — tall enough for title + 3 charts ──
fig, axes = plt.subplots(1, 3, figsize=(20, 7), facecolor=DARK_BG)
fig.patch.set_facecolor(DARK_BG)

# Title using fig.text so it never clips
fig.text(0.5, 0.97,
         'ML Price Prediction Model — Gangapur Road, Nashik',
         ha='center', va='top',
         fontsize=14, fontweight='bold', color=TEXT_WHITE)

# Adjust subplots to leave room for title at top and footer at bottom
fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.18,
                    wspace=0.35)

for ax in axes:
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor('#2A2D3A')

# ── Plot 1: Actual vs Predicted ──
axes[0].scatter(y_test, rf_pred, color=ACCENT1, alpha=0.7, s=80, edgecolor='none')
min_val = min(y_test.min(), rf_pred.min())
max_val = max(y_test.max(), rf_pred.max())
axes[0].plot([min_val, max_val], [min_val, max_val],
             color=ACCENT4, linestyle='--', linewidth=2, label='Perfect Fit')
axes[0].set_title('Actual vs Predicted Cost',
                  fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=10)
axes[0].set_xlabel('Actual Cost (Rs.)', fontsize=10)
axes[0].set_ylabel('Predicted Cost (Rs.)', fontsize=10)
axes[0].legend(fontsize=9, frameon=False, labelcolor=TEXT_WHITE)
axes[0].tick_params(labelsize=8)

# ── Plot 2: Feature Importance ──
feat_names = ['Rating', 'Cuisine', 'Rest. Type']
feat_vals  = rf.feature_importances_
bars = axes[1].barh(feat_names, feat_vals,
                    color=[ACCENT1, ACCENT2, ACCENT3],
                    height=0.4, edgecolor='none')
axes[1].set_title('Feature Importance',
                  fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=10)
axes[1].set_xlabel('Importance Score', fontsize=10)
axes[1].tick_params(labelsize=9, colors=TEXT_WHITE)
for bar, val in zip(bars, feat_vals):
    axes[1].text(val + 0.005, bar.get_y() + bar.get_height()/2,
                 f'{val:.1%}', va='center',
                 color=TEXT_WHITE, fontsize=9, fontweight='bold')

# ── Plot 3: Model Comparison ──
models  = ['Linear\nRegression', 'Random\nForest']
r2_vals = [max(0, lr_r2), max(0, rf_r2)]
mae_vals= [lr_mae, rf_mae]
x = np.arange(len(models))
b1 = axes[2].bar(x - 0.2, r2_vals, 0.35,
                 label='R² Score', color=ACCENT1, edgecolor='none')
b2 = axes[2].bar(x + 0.2, [m/1000 for m in mae_vals], 0.35,
                 label='MAE/1000', color=ACCENT3, edgecolor='none')
axes[2].set_title('Model Comparison',
                  fontsize=11, fontweight='bold', color=TEXT_WHITE, pad=10)
axes[2].set_xticks(x)
axes[2].set_xticklabels(models, fontsize=10, color=TEXT_WHITE)
axes[2].tick_params(axis='y', labelsize=8)
axes[2].legend(fontsize=9, frameon=False, labelcolor=TEXT_WHITE)
for bar in b1:
    axes[2].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01,
                 f'{bar.get_height():.2f}',
                 ha='center', fontsize=8,
                 fontweight='bold', color=TEXT_WHITE)

# ── Footer ──
fig.text(0.5, 0.04,
         'Model trained on 33 Zomato restaurants ',
         ha='center', fontsize=9, color=TEXT_GRAY)

plt.savefig('ml_model_charts.png', dpi=180,
            bbox_inches='tight', facecolor=DARK_BG)
plt.show()
print("\n  ML charts saved as ml_model_charts.png!")
print("\n  ML Model Complete!")