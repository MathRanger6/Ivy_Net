import pandas as pd

# Create sample DataFrames
df_left = pd.DataFrame({
    'pid_pde': ['A0', 'A1', 'A2'],
    'asg_uic_pde': ['BB0', 'BB1', 'BB2'],
    'fy': [1, 2, 3]
})
print(df_left)

df_right = pd.DataFrame({
    'uic_pde': ['BB0', 'BB1', 'BB2'],
    'fy': [1, 2, 3],
    'division_name': ['1CD', '2ID', '101ABN']
})
print(df_right)

# Method 1: Keep uic_pde for the merge but drop it afterwards
merged_df = pd.merge(df_left, df_right[['uic_pde', 'fy', 'division_name']], 
                     left_on=['asg_uic_pde', 'fy'], 
                     right_on=['uic_pde', 'fy'], 
                     how='left')
# Drop the uic_pde column after the merge
merged_df = merged_df.drop('uic_pde', axis=1)

print("Method 1 - Drop after merge:")
print(merged_df)

# Method 2: Use a different approach with suffixes
print("\nMethod 2 - Using suffixes:")
merged_df2 = pd.merge(df_left, df_right, 
                      left_on=['asg_uic_pde', 'fy'], 
                      right_on=['uic_pde', 'fy'], 
                      how='left',
                      suffixes=('', '_right'))
# Drop the uic_pde column
merged_df2 = merged_df2.drop('uic_pde', axis=1)
print(merged_df2) 