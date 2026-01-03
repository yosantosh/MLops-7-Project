import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# 1. Load the California Housing dataset (fall back to synthetic if download fails)
try:
	california = datasets.fetch_california_housing()
	# Select only one feature for 2D visualization: 'Median Income' (Index 0)
	X = california.data[:, np.newaxis, 0]
	y = california.target
except Exception as e:
	print(f"Warning: couldn't fetch California dataset: {e}")
	print("Falling back to a synthetic regression dataset (1 feature).")
	from sklearn.datasets import make_regression
	X, y = make_regression(n_samples=1000, n_features=1, noise=10.0, random_state=42)

# Split the data into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------------------
# MODEL 1: Standard Discriminative (y = b0 + b1*x)
# Goal: Minimize Vertical Error (Squared Error of y)
# ---------------------------------------------------------
regr_disc = linear_model.LinearRegression()
regr_disc.fit(X_train, y_train)

# Make predictions normally
y_pred_disc = regr_disc.predict(X_test)

# ---------------------------------------------------------
# MODEL 2: Generative / Reformulated (x = phi0 + phi1*y)
# Goal: Minimize Horizontal Error (Squared Error of x)
# ---------------------------------------------------------
# Note: We SWAP X and y during training
regr_gen = linear_model.LinearRegression()
regr_gen.fit(y_train.reshape(-1, 1), X_train)

# Extract parameters from x = phi0 + phi1*y
phi1 = np.ravel(regr_gen.coef_)[0]
phi0 = np.ravel(regr_gen.intercept_)[0]

# INVERT the relationship to predict y given x
# y = (x - phi0) / phi1
y_pred_gen = (X_test - phi0) / phi1

# ---------------------------------------------------------
# METRICS & PLOTTING
# ---------------------------------------------------------

# Calculate Mean Squared Error (MSE) on the TEST set
mse_disc = mean_squared_error(y_test, y_pred_disc)
mse_gen = mean_squared_error(y_test, y_pred_gen)

print(f"--- Results on Test Data ---")
print(f"Discriminative MSE (Standard): {mse_disc:.4f}")
print(f"Generative MSE (Inverted):     {mse_gen:.4f}")
print(f"\nInterpretation: The Standard model should have lower MSE because it was explicitly optimized for this metric.")

# Plotting
plt.figure(figsize=(10, 6))

# 1. Scatter plot of the real test data
plt.scatter(X_test, y_test, color='lightgray', s=10, label='Test Data')

# 2. Plot Standard Model Line
plt.plot(X_test, y_pred_disc, color='blue', linewidth=2, label='Standard (Minimizes Vertical Error)')

# 3. Plot Generative Model Line
# (Note: The lines will cross at the mean of the data)
plt.plot(X_test, y_pred_gen, color='red', linestyle='--', linewidth=2, label='Generative (Minimizes Horizontal Error)')

plt.xlabel('Median Income (Feature)')
plt.ylabel('Median House Value (Target)')
plt.title('Comparison of Linear Regression Formulations')
plt.legend()
plt.grid(True, alpha=0.3)
out_path = 'regression_comparison.png'
plt.savefig(out_path, bbox_inches='tight')
print(f"Saved plot to {out_path}")