import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests # 🌐 Essential for fetching live weather data!
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib # New: To save and load models and preprocessors

# --- 🚀 Stage 1: Gathering the Seeds (Data Loading & Initial Splitting) 🚀 ---
print("\n" + "="*90)
print("🚀🚀🚀 Welcome to Your Smart Farming Assistant! Let's Grow Together! 🚀🚀🚀")
print("--- 1. Loading and Splitting Your Precious Crop Data ---")
print("="*90 + "\n")

# 📂 Make sure your CSV file path is spot on!
try:
    raw_data = pd.read_csv('/content/sample_data/crop_dataset.csv')
    print("✅ Raw dataset loaded successfully! Here's a sneak peek at your fertile ground:\n")
    print(raw_data.head())
except FileNotFoundError:
    print("❌ Oh no! 'crop_dataset.csv' was not found. Please double-check the file path.")
    print("   Ensure the file is exactly in '/content/sample_data/'. We can't farm without data! 🐛")
    exit() # Exiting gracefully as the script cannot proceed without the dataset.

# 🌳 Dividing your farm into fertile plots for learning!
# We split the data to ensure our models learn effectively and generalize well.
train_df, test_df = train_test_split(raw_data, test_size=0.15, random_state=42)
train_df, val_df = train_test_split(train_df, test_size=0.15, random_state=42)

print("\n✨ Your Dataset has been Beautifully Split into Training, Validation, and Test Sets! ✨")
print(f"  🌱 **Training Farm Size:** {train_df.shape} rows for deep learning.")
print(f"  🌼 **Validation Patch Size:** {val_df.shape} rows for fine-tuning our experts.")
print(f"  🌾 **Test Field Size:** {test_df.shape} rows for the final, unbiased evaluation.")

# 🎯 Identifying your precious inputs and desired outputs!
input_cols = list(raw_data.columns) # Start with all columns from the raw data...
input_cols.remove('Crop Type')  # ...then remove the first target output: 'Crop Type'!
input_cols.remove('Fertilizer Name') # ...and the second target output: 'Fertilizer Name'!

# Prepare input and target dataframes for all splits
train_inputs = train_df[input_cols].copy()
train_targets1 = train_df['Crop Type'].copy() # Our first output: what crop to plant!
train_targets2 = train_df['Fertilizer Name'].copy() # Our second output: what fertilizer to use!

val_inputs = val_df[input_cols].copy()
val_targets1 = val_df['Crop Type'].copy()
val_targets2 = val_df['Fertilizer Name'].copy()

test_inputs = test_df[input_cols].copy()
test_targets1 = test_df['Crop Type'].copy()
test_targets2 = test_df['Fertilizer Name'].copy()

print(f"\n🏷️ **Input Features** (what we feed to our models): {input_cols}")
print("🎯 **Output Targets** (what our models predict): 'Crop Type', 'Fertilizer Name'")

# --- IMPORTANT: Define numeric and categorical columns *before* EDA plotting ---
# Identify numeric and categorical columns from the raw_data for EDA
# These will be used for plotting before the train_inputs are transformed
numeric_cols = raw_data[input_cols].select_dtypes(include=np.number).columns.tolist()
categorical_cols = raw_data[input_cols].select_dtypes(include='object').columns.tolist() # Only input categorical cols
all_categorical_cols = raw_data.select_dtypes(include='object').columns.tolist() # All categorical cols (including targets)

print(f"\n🔍 Identified Raw Numeric Columns for EDA: {numeric_cols}")
print(f"🎨 Identified Raw Categorical Columns for EDA: {all_categorical_cols}")


# --- 📈 Stage 1.5: Getting to Know Your Data (Exploratory Data Analysis - EDA) 📈 ---
print("\n" + "="*90)
print("📊📊📊 Exploring Your Data: Unveiling Hidden Stories! 📊📊📊")
print("--- 1.5. Understanding Your Raw Dataset Before Preprocessing ---")
print("="*90 + "\n")

print("🔍 **Dataset Information (raw_data.info()):**")
print("   (This shows column names, non-null counts, and data types – look for missing values!)\n")
raw_data.info()

print("\n\n📊 **Statistical Summary (raw_data.describe()):**")
print("   (Dive into min, max, mean, and quartiles for your numeric features.)\n")
print(raw_data.describe().to_string()) # .to_string() for better console formatting

print("\n\n❓ **Missing Values Check (raw_data.isnull().sum()):**")
print("   (Crucial to see if any data points are missing before imputation.)\n")
print(raw_data.isnull().sum().to_string())

print("\n\n📈 **Visualizing Data Distributions for Insights!**")

# Plotting distributions for numeric columns
if numeric_cols: # Only plot if there are numeric columns
    num_numeric_plots = len(numeric_cols)
    cols_per_row = 3
    rows = (num_numeric_plots + cols_per_row - 1) // cols_per_row
    plt.figure(figsize=(cols_per_row * 6, rows * 5))
    for i, col in enumerate(numeric_cols):
        plt.subplot(rows, cols_per_row, i + 1)
        sns.histplot(raw_data[col], kde=True, color=sns.color_palette("coolwarm")[i % 6])
        plt.title(f'Distribution of {col}', fontsize=12)
        plt.xlabel(col, fontsize=10)
        plt.ylabel('Count', fontsize=10)
    plt.tight_layout()
    plt.suptitle('Distributions of Numeric Features', fontsize=18, y=1.02, color='darkgreen')
    plt.show()
else:
    print("No numeric columns found in input data for distribution plotting.")

# Plotting counts for all categorical columns (inputs and outputs)
if all_categorical_cols: # Only plot if there are categorical columns
    num_categorical_plots = len(all_categorical_cols)
    cols_per_row = 3
    rows = (num_categorical_plots + cols_per_row - 1) // cols_per_row
    plt.figure(figsize=(cols_per_row * 6, rows * 5))
    for i, col in enumerate(all_categorical_cols):
        plt.subplot(rows, cols_per_row, i + 1)
        sns.countplot(data=raw_data, x=col, palette='pastel', order=raw_data[col].value_counts().index)
        plt.title(f'Counts of {col}', fontsize=12)
        plt.xlabel(col, fontsize=10)
        plt.ylabel('Count', fontsize=10)
        plt.xticks(rotation=45, ha='right') # Rotate labels for readability
    plt.tight_layout()
    plt.suptitle('Counts of Categorical Features (Inputs & Outputs)', fontsize=18, y=1.02, color='darkblue')
    plt.show()
else:
    print("No categorical columns found for count plotting.")

print("\n✨ EDA Complete! You now have a deeper understanding of your dataset! ✨")


# --- 🌱 Stage 2: Nurturing the Soil (Data Preprocessing) 🌱 ---
print("\n" + "="*90)
print("🌿🌿🌿 Preparing Your Data for Optimal Growth! 🌿🌿🌿")
print("--- 2. Cleaning and Transforming Your Input Data ---")
print("="*90 + "\n")

# Re-identifying numeric and categorical columns from the 'train_inputs' DataFrame
# This is crucial for consistent preprocessing across train/val/test sets
numeric_cols = train_inputs.select_dtypes(include=np.number).columns.tolist()
categorical_cols = train_inputs.select_dtypes(include='object').columns.tolist()

print(f"🔍 Identified Numeric Columns for Preprocessing: {numeric_cols}")
print(f"🎨 Identified Categorical Columns for Preprocessing: {categorical_cols}")

# 💧 Imputation for Numeric Columns: Filling in the gaps!
# We fit our imputer ONLY on the training data to prevent data leakage.
imputer = SimpleImputer(strategy='mean')
imputer.fit(train_inputs[numeric_cols])

# Now, transform all datasets!
train_inputs.loc[:, numeric_cols] = imputer.transform(train_inputs[numeric_cols])
val_inputs.loc[:, numeric_cols] = imputer.transform(val_inputs[numeric_cols])
test_inputs.loc[:, numeric_cols] = imputer.transform(test_inputs[numeric_cols])
print("✅ Numeric columns imputed (missing values filled!).")

# 📏 Scaling for Numeric Columns: Standardizing for fair play!
# Fit our scaler ONLY on the training data.
scaler = MinMaxScaler()
scaler.fit(train_inputs[numeric_cols])

# Transform all datasets!
train_inputs.loc[:, numeric_cols] = scaler.transform(train_inputs[numeric_cols])
val_inputs.loc[:, numeric_cols] = scaler.transform(val_inputs[numeric_cols])
test_inputs.loc[:, numeric_cols] = scaler.transform(test_inputs[numeric_cols])
print("✅ Numeric columns scaled (values normalized between 0 and 1!).")

# 🏷️ One-Hot Encoding for Categorical Columns: Turning words into numbers!
# Fit our encoder ONLY on the training data.
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoder.fit(train_inputs[categorical_cols])
encoded_cols = list(encoder.get_feature_names_out(categorical_cols))

# Transform and combine with original numeric features
train_inputs_encoded = pd.DataFrame(encoder.transform(train_inputs[categorical_cols]),
                                    columns=encoded_cols,
                                    index=train_inputs.index)
val_inputs_encoded = pd.DataFrame(encoder.transform(val_inputs[categorical_cols]),
                                  columns=encoded_cols,
                                  index=val_inputs.index)
test_inputs_encoded = pd.DataFrame(encoder.transform(test_inputs[categorical_cols]),
                                   columns=encoded_cols,
                                   index=test_inputs.index)

# Drop original categorical columns and concatenate the new encoded ones
train_inputs = pd.concat([train_inputs.drop(columns=categorical_cols), train_inputs_encoded], axis=1)
val_inputs = pd.concat([val_inputs.drop(columns=categorical_cols), val_inputs_encoded], axis=1)
test_inputs = pd.concat([test_inputs.drop(columns=categorical_cols), test_inputs_encoded], axis=1)
print("✅ Categorical columns one-hot encoded (words converted to numbers!).")

# Renaming for consistency with model training (now these are the final feature sets!)
x_train = train_inputs
x_val = val_inputs
x_test = test_inputs

print("\n✨ Preprocessing Complete! Your data is sparkling clean and ready for experts! ✨")
print(f"  📊 Final Training Features Shape (x_train): {x_train.shape}")
print(f"  📊 Final Validation Features Shape (x_val): {x_val.shape}")
print(f"  📊 Final Test Features Shape (x_test): {x_test.shape}")


# --- 🧠 Stage 3: Cultivating the Experts (Model Training) 🧠 ---
print("\n" + "="*90)
print("🧠🧠🧠 Training Your Smart Farming Experts! 🧠🧠🧠")
print("--- 3. Building Prediction Models ---")
print("="*90 + "\n")

## 🧑‍🌾 Expert 1: The Crop Whisperer (Predicts Crop Type)
print("\n✨ Training The Crop Whisperer... (Predicts Crop Type) ✨")
model_crop_type = DecisionTreeClassifier(random_state=42)
model_crop_type.fit(x_train, train_targets1)
print(f"  📈 Training Accuracy: {model_crop_type.score(x_train, train_targets1):.4f}")
print(f"  🎯 Validation Accuracy: {model_crop_type.score(x_val, val_targets1):.4f}")
print(f"  🏆 Test Accuracy: {model_crop_type.score(x_test, test_targets1):.4f}")

## 🧪 Expert 2: The Nutrient Guru (Predicts Fertilizer Name)
print("\n✨ Training The Nutrient Guru... (Predicts Fertilizer Name) ✨")
model_fertilizer_name = DecisionTreeClassifier(random_state=42)
model_fertilizer_name.fit(x_train, train_targets2)
print(f"  📈 Training Accuracy: {model_fertilizer_name.score(x_train, train_targets2):.4f}")
print(f"  🎯 Validation Accuracy: {model_fertilizer_name.score(x_val, val_targets2):.4f}")
print(f"  🏆 Test Accuracy: {model_fertilizer_name.score(x_test, test_targets2):.4f}")

print("\n🎉 Both Expert Models are Trained and Ready to Share Their Wisdom! 🎉")


# --- 📊 Stage 4: Unearthing Hidden Gems (Feature Importance) 📊 ---
print("\n" + "="*90)
print("🔍🔍🔍 Unveiling What Matters Most! (Feature Importance) 🔍🔍🔍")
print("--- 4. Discovering Key Influencers ---")
print("="*90 + "\n")

# 🌟 Feature importance for The Crop Whisperer (Crop Type Model)
print("\n✨ **Top 10 Influencers for Crop Type Prediction:** ✨")
importance_crop_df = pd.DataFrame({
    'Feature': x_train.columns,
    'Importance': model_crop_type.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance_crop_df.head(10).to_string(index=False)) # .to_string for cleaner console output

# Plotting Feature Importance for Crop Type with a splash of color!
plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=importance_crop_df.head(10), palette='viridis')
plt.title('Top 10 Feature Importances for Crop Type Prediction 🌾', fontsize=16, color='darkgreen')
plt.xlabel('Importance Score', fontsize=12, color='darkblue')
plt.ylabel('Feature', fontsize=12, color='darkblue')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 🧪 Feature importance for The Nutrient Guru (Fertilizer Name Model)
print("\n✨ **Top 10 Influencers for Fertilizer Name Prediction:** ✨")
importance_fertilizer_df = pd.DataFrame({
    'Feature': x_train.columns,
    'Importance': model_fertilizer_name.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance_fertilizer_df.head(10).to_string(index=False))

# Plotting Feature Importance for Fertilizer Name with another colorful palette!
plt.figure(figsize=(12, 6))
sns.barplot(x='Importance', y='Feature', data=importance_fertilizer_df.head(10), palette='magma')
plt.title('Top 10 Feature Importances for Fertilizer Name Prediction 🧪', fontsize=16, color='darkred')
plt.xlabel('Importance Score', fontsize=12, color='darkblue')
plt.ylabel('Feature', fontsize=12, color='darkblue')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# --- 🔮 Stage 5: Predicting Tomorrow's Harvest (Live Prediction System) 🔮 ---
print("\n" + "="*90)
print("🔮🔮🔮 Predicting Tomorrow's Harvest! Your Personalized Recommendations! 🔮🔮🔮")
print("--- 5. Your Interactive Smart Farming Recommender ---")
print("="*90 + "\n")

# 💧 Helper Function to estimate moisture based on humidity
def estimate_moisture(humidity):
    # This is a simplified estimation. For truly precise farming, consider soil moisture sensors!
    print("  (💡 Estimating soil moisture based on humidity...)")
    if humidity > 80: return 70
    elif humidity > 60: return 60
    elif humidity > 40: return 50
    elif humidity > 20: return 40
    else: return 30

# 🌐 Your WeatherAPI key and desired location! (Currently set for Bengaluru)
API_KEY = 'c8038b38b6be4e6c9a540208251505'
LOCATION = 'Bengaluru' # 📍 Feel free to change this city or make it a user input!

# Function to fetch live weather data from WeatherAPI
def get_weather(api_key, location):
    print(f"\n🌍 Fetching live weather data for {location}, India (Current Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S %Z')})...")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Will raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        print(f"  🌡️ Current Temperature: {temp}°C")
        print(f"  💧 Current Humidity: {humidity}%")
        return temp, humidity
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error fetching weather data from WeatherAPI: {e}")
        print("  Using default values (Temp=25°C, Humidity=60%) as a fallback. Please check your API key or internet connection. 🌧️")
        return 25, 60 # Default values if API call fails

# --- Gather Live Inputs ---
temperature, humidity = get_weather(API_KEY, LOCATION) # Get live weather info!
moisture = estimate_moisture(humidity) # Estimate soil moisture

print("\n--- 🧑‍🌾 Now, tell us about your soil's current conditions! ---")
nitrogen = int(input("  🧪 Enter Nitrogen (N) value in your soil (e.g., 37): "))
potassium = int(input("  🧪 Enter Potassium (K) value in your soil (e.g., 0): "))
phosphorous = int(input("  🧪 Enter Phosphorous (P) value in your soil (e.g., 0): "))

# Dynamically extract soil types from your training data's encoded columns for consistency!
soil_types_from_data = [col.replace('Soil Type_', '') for col in encoded_cols if col.startswith('Soil Type_')]
# Fallback in case 'Soil Type_' not found (unlikely if data is consistent, but good for robustness)
if not soil_types_from_data and 'Soil Type' in all_categorical_cols: # Check if 'Soil Type' was an original categorical column
    soil_types_from_data = raw_data['Soil Type'].unique().tolist() # Get unique types from raw data

print("\n--- Select Your Soil Type from the options below: ---")
for i, s in enumerate(soil_types_from_data):
    print(f"  {i}: {s}")
soil_choice = int(input("  🔢 Enter the number corresponding to your soil type: "))
selected_soil = soil_types_from_data[soil_choice]
print(f"  🌍 You selected: **{selected_soil}**")

# --- Prepare New Data for Prediction ---
print("\n--- Applying the Magic Dust (Preprocessing Your Live Input Data)... ---")

# Creating a fresh DataFrame for your new raw input data, just like training data!
new_input_data_raw = pd.DataFrame({
    'Temparature': [temperature],
    'Humidity': [humidity],
    'Moisture': [moisture],
    'Nitrogen': [nitrogen],
    'Potassium': [potassium],
    'Phosphorous': [phosphorous],
    'Soil Type': [selected_soil]
})

# Apply the exact same preprocessing steps as training data, using the *already fitted* transformers!
new_input_data_raw.loc[:, numeric_cols] = imputer.transform(new_input_data_raw[numeric_cols]) # 1. Impute (if any missing values)
new_input_data_scaled = pd.DataFrame(scaler.transform(new_input_data_raw[numeric_cols]),
                                     columns=numeric_cols,
                                     index=new_input_data_raw.index) # 2. Scale

# 3. One-Hot Encode (creating new columns for categorical data)
new_input_data_encoded_temp = pd.DataFrame(encoder.transform(new_input_data_raw[categorical_cols]),
                                           columns=encoded_cols,
                                           index=new_input_data_raw.index)

# Combine all preprocessed features for the final prediction input!
final_new_data_for_prediction = pd.concat([new_input_data_scaled, new_input_data_encoded_temp], axis=1)

print("\n✨ Your Live Input Data is Perfectly Prepared for Our Experts! ✨")
print("  Here's what our models will see (all features, one row):")
# Use .T to transpose for better readability for a single row DataFrame
print(final_new_data_for_prediction.T.to_string())
print(f"\n  Total Prepared Features: {final_new_data_for_prediction.shape[1]} columns.")


# --- 🎯 Stage 6: Harvesting the Insights (Making Predictions) 🎯 ---
print("\n" + "="*90)
print("🎉🎉🎉 Harvesting Your Intelligent Recommendations! 🎉🎉🎉")
print("--- 6. Generating Predictions for Your Farm ---")
print("="*90 + "\n")

# Asking The Crop Whisperer for its wisdom!
predicted_crop_type = model_crop_type.predict(final_new_data_for_prediction)
print(f"\n🔮 Based on your current conditions, the **Predicted Crop Type** for your farm is: \033[1m\033[92m{predicted_crop_type[0].upper()}\033[0m! (Go Green! 💚)")

# Asking The Nutrient Guru for its secret formula!
predicted_fertilizer_name = model_fertilizer_name.predict(final_new_data_for_prediction)
print(f"🧪 And the **Predicted Fertilizer Name** to nourish your crop is: \033[1m\033[96m{predicted_fertilizer_name[0].upper()}\033[0m! (Boost Growth! 💙)")

print("\n" + "="*90)
print("✨ Your Smart Farming Assistant has delivered its precise insights! ✨")
print("Happy Farming! May your yields be bountiful! 🧑‍🌾")
print("="*90 + "\n")


# --- NEW: Stage 7: Preserving the Wisdom (Saving Models and Preprocessors) ---
print("\n" + "="*90)
print("💾💾💾 Preserving Your Smart Farming Wisdom! 💾💾💾")
print("--- 7. Saving Models and Preprocessing Objects ---")
print("="*90 + "\n")

try:
    # Ensure a directory for models exists
    import os
    os.makedirs('models', exist_ok=True)

    # Save the models
    joblib.dump(model_crop_type, 'models/model_crop_type.joblib')
    joblib.dump(model_fertilizer_name, 'models/model_fertilizer_name.joblib')
    print("✅ Prediction models saved: 'model_crop_type.joblib', 'model_fertilizer_name.joblib'")

    # Save the preprocessors
    joblib.dump(imputer, 'models/imputer.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    joblib.dump(encoder, 'models/encoder.joblib')
    joblib.dump(input_cols, 'models/input_cols.joblib') # Save input column order
    joblib.dump(numeric_cols, 'models/numeric_cols.joblib') # Save identified numeric columns
    joblib.dump(categorical_cols, 'models/categorical_cols.joblib') # Save identified categorical columns

    print("✅ Preprocessing objects saved: 'imputer.joblib', 'scaler.joblib', 'encoder.joblib'")
    print("✅ Input column lists saved: 'input_cols.joblib', 'numeric_cols.joblib', 'categorical_cols.joblib'")
    print("\n📦 All essential components for your API are now safely stored in the 'models/' directory!")

except Exception as e:
    print(f"❌ Error saving models or preprocessors: {e}")