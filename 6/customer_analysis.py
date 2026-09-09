import pandas as pd
import os

# ============================================================
# CUSTOMER SEGMENTATION AND RETENTION ANALYSIS
# ============================================================

FILE_NAME = "C:/Users/anil1/OneDrive/Desktop/MPI/6/shopping_behavior.csv"

# 1. Load dataset
df = pd.read_csv(FILE_NAME)

print("=" * 60)
print("CUSTOMER SEGMENTATION AND RETENTION ANALYSIS")
print("=" * 60)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nDataset information:")
df.info()

print("\nMissing values:")
print(df.isnull().sum())

print("\nStatistical summary:")
print(df.describe(include="all"))


# 2. Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# Make purchase amount name consistent
if "purchase_amount_(usd)" in df.columns:
    df.rename(
        columns={"purchase_amount_(usd)": "purchase_amount"},
        inplace=True
    )


# 3. Convert numeric columns
numeric_columns = [
    "age",
    "purchase_amount",
    "previous_purchases",
    "review_rating"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# 4. Missing Review Rating
if "review_rating" in df.columns and "category" in df.columns:

    print("\nMissing Review Ratings Before:",
          df["review_rating"].isna().sum())

    df["review_rating"] = (
        df.groupby("category")["review_rating"]
        .transform(
            lambda x: x.fillna(x.median())
        )
    )

    df["review_rating"] = df["review_rating"].fillna(
        df["review_rating"].median()
    )

    print("Missing Review Ratings After:",
          df["review_rating"].isna().sum())


# 5. Age Group
if "age" in df.columns:

    def age_group(age):
        if age < 25:
            return "Young Adult"
        elif age < 40:
            return "Adult"
        elif age < 60:
            return "Middle-aged"
        else:
            return "Senior"

    df["age_group"] = df["age"].apply(age_group)


# 6. Purchase Frequency Days
if "frequency_of_purchases" in df.columns:

    frequency_map = {
        "daily": 1,
        "weekly": 7,
        "bi-weekly": 14,
        "biweekly": 14,
        "monthly": 30,
        "quarterly": 90,
        "annually": 365,
        "yearly": 365
    }

    df["purchase_frequency_days"] = (
        df["frequency_of_purchases"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(frequency_map)
    )


# 7. Remove redundant promo column
if "promo_code_used" in df.columns:
    df.drop(
        columns=["promo_code_used"],
        inplace=True
    )


# 8. Remove duplicate records
print("\nDuplicate records:",
      df.duplicated().sum())

df.drop_duplicates(inplace=True)


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

if "previous_purchases" in df.columns:

    def customer_segment(purchases):

        if purchases <= 2:
            return "New"

        elif purchases <= 10:
            return "Returning"

        else:
            return "Loyal"

    df["customer_segment"] = (
        df["previous_purchases"]
        .apply(customer_segment)
    )


# ============================================================
# BUSINESS ANALYSIS
# ============================================================

# 1. Revenue by Gender
print("\n1. Revenue by Gender")

revenue_gender = (
    df.groupby("gender")["purchase_amount"]
    .sum()
    .reset_index()
    .sort_values(
        "purchase_amount",
        ascending=False
    )
)

print(revenue_gender)


# 2. High Spending Discount Users
print("\n2. High Spending Discount Users")

average_purchase = df["purchase_amount"].mean()

discount_users = df[
    (df["purchase_amount"] > average_purchase) &
    (
        df["discount_applied"]
        .astype(str)
        .str.lower()
        .isin(["yes", "true", "1"])
    )
]

print("Average purchase:",
      round(average_purchase, 2))

print("High-spending discount users:",
      len(discount_users))


# 3. Top 5 Products by Rating
print("\n3. Top 5 Products by Rating")

top_products = (
    df.groupby("item_purchased")["review_rating"]
    .mean()
    .reset_index()
    .sort_values(
        "review_rating",
        ascending=False
    )
    .head(5)
)

print(top_products)


# 4. Shipping Type Comparison
print("\n4. Shipping Type Comparison")

shipping = (
    df.groupby("shipping_type")["purchase_amount"]
    .mean()
    .reset_index()
)

print(shipping)


# 5. Subscriber vs Non-Subscriber
print("\n5. Subscriber vs Non-Subscriber")

subscription = (
    df.groupby("subscription_status")
    .agg(
        customers=("subscription_status", "count"),
        total_revenue=("purchase_amount", "sum"),
        average_purchase=("purchase_amount", "mean")
    )
    .reset_index()
)

print(subscription)


# 6. Discount Dependent Products
print("\n6. Discount Dependent Products")

discount_products = (
    df.assign(
        discount_flag=
        df["discount_applied"]
        .astype(str)
        .str.lower()
        .isin(["yes", "true", "1"])
    )
    .groupby("item_purchased")["discount_flag"]
    .mean()
    .reset_index()
)

discount_products["discount_rate_percent"] = (
    discount_products["discount_flag"] * 100
)

discount_products = discount_products.sort_values(
    "discount_rate_percent",
    ascending=False
)

print(
    discount_products[
        ["item_purchased", "discount_rate_percent"]
    ]
)


# 7. Customer Segmentation
print("\n7. Customer Segmentation")

segmentation = (
    df["customer_segment"]
    .value_counts()
    .reset_index()
)

segmentation.columns = [
    "customer_segment",
    "number_of_customers"
]

print(segmentation)


# 8. Top 3 Products per Category
print("\n8. Top 3 Products per Category")

product_counts = (
    df.groupby(
        ["category", "item_purchased"]
    )
    .size()
    .reset_index(
        name="total_orders"
    )
)

product_counts["rank"] = (
    product_counts
    .groupby("category")["total_orders"]
    .rank(
        method="first",
        ascending=False
    )
)

top_3 = product_counts[
    product_counts["rank"] <= 3
].sort_values(
    ["category", "total_orders"],
    ascending=[True, False]
)

print(top_3)


# 9. Repeat Buyers and Subscription
print("\n9. Repeat Buyers and Subscription")

repeat_buyers = df[
    df["previous_purchases"] > 0
]

repeat_subscription = (
    repeat_buyers
    .groupby("subscription_status")
    .size()
    .reset_index(
        name="repeat_buyers"
    )
)

print(repeat_subscription)


# 10. Revenue by Age Group
print("\n10. Revenue by Age Group")

age_revenue = (
    df.groupby("age_group")["purchase_amount"]
    .sum()
    .reset_index()
    .sort_values(
        "purchase_amount",
        ascending=False
    )
)

print(age_revenue)


# ============================================================
# SAVE CLEANED DATA AND RESULTS
# ============================================================

df.to_csv(
    "cleaned_customer_data.csv",
    index=False
)

os.makedirs(
    "analysis_results",
    exist_ok=True
)

revenue_gender.to_csv(
    "analysis_results/revenue_by_gender.csv",
    index=False
)

top_products.to_csv(
    "analysis_results/top_5_products.csv",
    index=False
)

shipping.to_csv(
    "analysis_results/shipping_comparison.csv",
    index=False
)

subscription.to_csv(
    "analysis_results/subscription_analysis.csv",
    index=False
)

discount_products.to_csv(
    "analysis_results/discount_products.csv",
    index=False
)

segmentation.to_csv(
    "analysis_results/customer_segmentation.csv",
    index=False
)

top_3.to_csv(
    "analysis_results/top_3_products_per_category.csv",
    index=False
)

repeat_subscription.to_csv(
    "analysis_results/repeat_buyers_subscription.csv",
    index=False
)

age_revenue.to_csv(
    "analysis_results/revenue_by_age_group.csv",
    index=False
)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nCreated:")
print("1. cleaned_customer_data.csv")
print("2. analysis_results/ folder")
print("3. Customer segmentation")
print("4. Ten business analyses")
