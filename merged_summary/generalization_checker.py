import pandas as pd
import io

def check_nand(df):
    """
    Checks the generalization: There is no full form that can express NAND.
    A NAND form can be expressed when Kp=1 and also when kneither=1, 
    but cannot be expressed when kboth=1.
    """
    print("--- 1. Checking Generalization: No NAND Connectives---")
    
    # Create a copy to safely clean data by stripping whitespace
    df_copy = df.copy()
    for col in ['full_form', 'can_express', 'Kp', 'kneither', 'kboth']:
        df_copy[col] = df_copy[col].str.strip()

    # Find forms that can be expressed when Kp = 1
    can_express_kp = set(df_copy[(df_copy['can_express'] == '1') & (df_copy['Kp'] == '1')]['full_form'].unique())

    # Find forms that can be expressed when kneither = 1 and the context shorthand is not 'negative'
    can_express_kneither = set(df_copy[(df_copy['can_express'] == '1') & (df_copy['kneither'] == '1') & (df['shorthand'] != 'negative')]['full_form'].unique())

    # Find forms that CANNOT be expressed when kboth = 1
    all_forms = set(df_copy['full_form'].unique())
    can_express_kboth = set(df_copy[(df_copy['can_express'] == '1') & (df_copy['kboth'] == '1')]['full_form'].unique())
    cannot_express_kboth = all_forms - can_express_kboth

    # A NAND form is the intersection of all three sets
    nand_forms = can_express_kp.intersection(can_express_kneither).intersection(cannot_express_kboth)

    if not nand_forms:
        print("Generalization HOLDS: No full form expresses NAND.")
    else:
        print("There are apparent counterexamples. The following forms can express NAND:")
        counterexample_df = df[df['full_form'].isin(nand_forms)][['source_file', 'full_form']].drop_duplicates().sort_values(by=['source_file', 'full_form'])
        print(counterexample_df.to_string(index=False))
    print("-" * 70)


def check_negation_for_kneither(df):
    """
    Checks the generalization: A form compatible with 'kneither=1' always involves negation.
    This is treated as the check for NOR-like properties.
    """
    print("--- 2. Checking Generalization: NOR Implies morpho-syntactic presence of negation---")

    # Create a copy to safely clean data by stripping whitespace
    df_copy = df.copy()
    for col in ['can_express', 'kneither', 'negation', 'source_file', 'full_form', 'shorthand']:
        df_copy[col] = df_copy[col].str.strip()

    # Filter for can_express = 1 and kneither = 1
    kneither_express_df = df_copy[(df_copy['can_express'] == '1') & (df_copy['kneither'] == '1') & (df['shorthand'] != 'negative')]

    # In this subset, find rows where negation is 'neither'
    counterexamples = kneither_express_df[kneither_express_df['negation'] == 'neither']

    if counterexamples.empty:
        print("Generalization HOLDS: Any form compatible with 'kneither=1' involves negation.")
    else:
        print("There are apparent counterexamples:")
        print(counterexamples[['source_file', 'full_form', 'shorthand']].to_string(index=False))
    print("-" * 70)


def check_juxtaposition_disjunction(df):
    """
    Checks the generalization: A simple juxtaposition cannot express disjunction.
    Disjunction is defined as a context where kboth=0 and kneither=0.
    """
    print("--- 3. Checking Generalization: Juxtaposition and Disjunction ---")
    
    # Create a copy to safely clean data by stripping whitespace
    df_copy = df.copy()
    for col in ['full_form', 'can_express', 'kboth', 'kneither', 'source_file', 'shorthand', 'question']:
        df_copy[col] = df_copy[col].str.strip()
    
    # Filter for juxtaposition forms
    juxt_forms = ['juxtaposition', '∅']
    juxt_df = df_copy[df_copy['full_form'].isin(juxt_forms)]

    # Find counterexamples: juxtaposition expressing disjunction
    counterexamples = juxt_df[
        (juxt_df['can_express'] == '1') &
        (juxt_df['kboth'] == '0') &
        (juxt_df['kneither'] == '0') &
        (juxt_df['question'] == '0')
    ]

    if counterexamples.empty:
        print("Generalization HOLDS: Juxtaposition does not express disjunction in this dataset.")
    else:
        print("Found cases where juxtaposition expresses disjunction:")
        print(counterexamples[['source_file', 'full_form', 'shorthand']].to_string(index=False))
    print("-" * 70)


def check_xor_complexity(df):
    """
    Checks the generalization: A connective that expresses exclusive disjunction (XOR)
    is always morphologically complex.
    UPDATED: An XOR connective must be incompatible with kboth='?' and only
    compatible with kboth='0' and kneither='0'.
    """
    print("--- 4. Checking Generalization: Morphological Complexity of XOR---")
    
    # Create a copy to safely clean data by stripping whitespace
    df_copy = df.copy()
    for col in ['full_form', 'can_express', 'kboth', 'kneither', 'source_file']:
        df_copy[col] = df_copy[col].str.strip()
    
    # 1. Pre-filter: Find forms that are explicitly INCOMPATIBLE with kboth = '?'
    incompatible_with_uncertainty = set(
        df_copy[(df_copy['kboth'] == '?') & (df_copy['can_express'] == '0')]['full_form'].unique()
    )

    exclusive_forms = []
    # 2. Iterate only through these pre-filtered forms
    for form in incompatible_with_uncertainty:
        # Get all contexts where the form can be expressed
        expressed_contexts = df_copy[(df_copy['full_form'] == form) & (df_copy['can_express'] == '1')]

        if expressed_contexts.empty:
            continue

        # 3. Check if all expressed contexts are strictly kboth=0 and kneither=0
        is_exclusive = all(expressed_contexts['kboth'] == '0') and \
                       all(expressed_contexts['kneither'] == '0')

        if is_exclusive:
            exclusive_forms.append(form)
    
    if not exclusive_forms:
        print("No connectives matching the strictest exclusive disjunction definition were found.")
        print("-" * 70)
        return

    print("Found the following exclusive disjunction connectives:")
    xor_df = df_copy[df_copy['full_form'].isin(exclusive_forms)][['source_file', 'full_form']].drop_duplicates().sort_values(by=['source_file', 'full_form'])
    print(xor_df.to_string(index=False))
    
    # Check for morphological complexity
    simple_counterexamples = []
    for form in exclusive_forms:
        if ' ' not in form and '…' not in form and '-' not in form:
            simple_counterexamples.append(form)
            
    if not simple_counterexamples:
        print("\nGeneralization HOLDS: All identified exclusive disjunctions appear morphologically complex.")
    else:
        print("\nThere are apparent counterexamples. The following exclusive disjunctions appear morphologically simple:")
        counterexample_df = df_copy[df_copy['full_form'].isin(simple_counterexamples)][['source_file', 'full_form']].drop_duplicates().sort_values(by=['source_file', 'full_form'])
        print(counterexample_df.to_string(index=False))
    print("-" * 70)


def main():
    """
    Main function to load data and run all generalization checks.
    """
    try:
        # Load the CSV file
        df = pd.read_csv('merged_output_vertical.csv', dtype=str).fillna('')
        print("✅ Successfully loaded 'merged_output_vertical.csv'.\n")

        # Run checks
        check_nand(df)
        check_negation_for_kneither(df)
        check_juxtaposition_disjunction(df)
        check_xor_complexity(df)

    except FileNotFoundError:
        print("Error: 'merged_output_vertical.csv' not found.")
        print("Please make sure the script is in the same directory as your CSV file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()