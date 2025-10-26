import pandas as pd
import numpy as np
import sys

# This map defines the 16 context types (shorthands) you requested,
# mapping the specific context IDs from the questionnaire to a general type.
CONTEXT_SHORTHAND_MAP = {
    'conj-nocontrast-sta': 'conj-nocontrast-sta',
    'conj-nocontrast-sta-2': 'conj-nocontrast-sta',
    'conj-nocontrast-sta-3': 'conj-nocontrast-sta',
    'conj-nocontrast-sta-mod': 'conj-nocontrast-sta',
    'conj-nocontrast-epi': 'conj-nocontrast-epi',
    'conj-contrast-sta': 'conj-contrast-sta',
    'conj-contrast-sta-mod': 'conj-contrast-sta',
    'conj-contrast-sta-2': 'conj-contrast-sta',
    'conj-contrast-sta-3': 'conj-contrast-sta',
    'conj-contrast-sta-4': 'conj-contrast-sta',
    'conj-contrast-epi': 'conj-contrast-epi',
    'conj-contrast-epi-2': 'conj-contrast-epi',
    'conj-contrast-negp-sta': 'conj-contrast-negp-sta',
    'conj-contrast-negp-epi': 'conj-contrast-negp-epi',
    'disj-spk-1': 'disj-spk',
    'disj-spk-2': 'disj-spk',
    'disj-spk-3': 'disj-spk',
    'disj-spk-4': 'disj-spk',
    'disj-spk-4-prime': 'disj-spk',
    'disj-spk-5': 'disj-spk',
    'disj-nspk-epi': 'disj-nspk-epi',
    'disj-nspk-epi-exc-2': 'disj-nspk-epi',
    'disj-nspk-sta-exc': 'disj-nspk-sta-exc',
    'disj-nspk-sta-exc-mod': 'disj-nspk-sta-exc',
    'disj-nspk-sta-exc-2': 'disj-nspk-sta-exc',
    'disj-nspk-sta-exc-3': 'disj-nspk-sta-exc',
    'disj-nspk-sta-exc-4': 'disj-nspk-sta-exc',
    'disj-nspk-sta-exc-5': 'disj-nspk-sta-exc',
    'disj-nspk-sta-inc': 'disj-nspk-sta-inc',
    'disj-nspk-sta-inc-mod': 'disj-nspk-sta-inc',
    'disj-nspk-sta-inc-2': 'disj-nspk-sta-inc',
    'disj-nspk-sta-inc-3': 'disj-nspk-sta-inc',
    'disj-nspk-sta-inc-4': 'disj-nspk-sta-inc',
    'disj-nspk-sta-inc-5': 'disj-nspk-sta-inc',
    'disj-nspk-epi-q': 'disj-nspk-q-exc',
    'disj-nspk-epi-q-mod': 'disj-nspk-q-exc',
    'disj-nspk-sta-inc-q': 'disj-nspk-q-inc',
    'neither-sta': 'neither-sta',
    'neither-sta-2': 'neither-sta',
    'neither-sta-3': 'neither-sta',
    'neither-sta-4': 'neither-sta',
    'neither-epi': 'neither-epi',
    'neither-epi-2': 'neither-epi',
    'fc': 'fc',
    'negative': 'negative',
    'disj-nspk-epi-tel': 'disj-nspi-epi',
    'conj-nocontrast-epi-tel': 'conj-nocontrast-epi',
    'conj-contrast-epi-tel': 'conj-contrast-epi',
    'disj-spk-tel': 'disj-spk',
    'disj-nspk-epi-exc-tel': 'disj-nspk-epi-exc',
    'disj-nspk-epi-inc-tel': 'disj-nspk-epi-inc',
    'neither-epi-tel': 'neither-epi',
    'conj-nocontrast-epi-tur': 'conj-nocontrast-epi',
    'conj-contrast-epi-tur': 'conj-contrast-epi',
    'disj-nspk-epi-tur': 'disj-nspk-epi',
    'disj-nspk-epi-inc-tur': 'disj-nspk-epi-inc',
    'disj-nspk-epi-exc-tur': 'disj-nspk-epi-exc',
    'neither-epi-tur': 'neither-epi'
}

def get_shorthand(context_ref):
    """Maps a specific context_ref to its shorthand type."""
    return CONTEXT_SHORTHAND_MAP.get(context_ref)

def normalize_judgment(judgment):
    """Converts a judgment string ('felicitous', '#', '?', etc.) into 1, 0, or '?'."""
    val = str(judgment).strip().lower()
    
    if val in ['felicitous', '✓', '✓ ']: # Added trim for '✓ '
        return 1
    if val in ['infelicitous', '#']:
        return 0
    
    # Per your note, no symbol (empty, None, nan) counts as felicitous
    if val in ['nan', 'none', '']:
        return 1
        
    # Any other symbol containing a '?' is questionable
    if '?' in val or '#/*' in val:
        return '?'
        
    # Default for any other unknown symbol (that's not empty) is felicitous
    return 1

# Removed the language-specific infer_negation function

def resolve_judgments(judgment_list):
    """
    Analyzes a list of normalized judgments (1, 0, '?') for a group.
    Returns the final 'can_express' value (1, 0, or '?').
    """
    # Use set to find unique judgments
    unique_judgments = set(judgment_list)
    
    # If '?' is present, the result is always '?'
    if '?' in unique_judgments:
        return '?'
        
    # If 1 and 0 are both present (and no '?'), it's a conflict
    if 1 in unique_judgments and 0 in unique_judgments:
        return '?'
        
    # If only one type of judgment (or empty), return it
    if len(unique_judgments) == 1:
        return unique_judgments.pop()
        
    # Default case (e.g., empty list)
    return '?'

def generate_summary_table(q_file, ex_file, ev_file):
    """
    Generates the summary table from the three input CSV files.
    
    Args:
        q_file (str): Filepath to the questionnaire_table.csv
        ex_file (str): Filepath to the language's example table CSV
        ev_file (str): Filepath to the language's evidence table CSV

    Returns:
        pandas.DataFrame: The generated summary table.
    """
    try:
        # 1. Load Data
        q_df = pd.read_csv(q_file)
        ex_df = pd.read_csv(ex_file)
        ev_df = pd.read_csv(ev_file)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        return None

    # 2. Prepare Data (Merge and Pre-process)
    
    # Merge evidence with examples to get 'expression' and 'full_form'
    merged_df = pd.merge(
        ev_df,
        ex_df[['ref', 'expression', 'full_form']],
        left_on='example',
        right_on='ref',
        how='left',
        suffixes=('_ev', '_ex')
    )
    
    # Merge with questionnaire to get context properties
    q_props = q_df[['ref', 'kboth', 'kneither', 'contrast', 'stative', 'negated_p', 'Kp', 'question', 'fc']]
    merged_df = pd.merge(
        merged_df,
        q_props,
        left_on='context',
        right_on='ref',
        how='left',
        suffixes=('', '_q')
    )

    # 3. Apply Mappings
    # Apply shorthand mapping
    merged_df['shorthand'] = merged_df['context'].apply(get_shorthand)
    
    # Normalize the judgment strings
    merged_df['norm_judgment'] = merged_df['judgment'].apply(normalize_judgment)
    
    # Drop any rows that didn't map to a shorthand (i.e., contexts we don't care about)
    merged_df = merged_df.dropna(subset=['shorthand'])

    # 4. Group and Aggregate
    group_keys = ['expression', 'full_form', 'shorthand']
    
    # Define aggregation functions
    agg_funcs = {
        'ref_ev': lambda x: ','.join(sorted(set(str(i) for i in x))), # Aggregate evidence refs
        'norm_judgment': list, # Collect all judgments to check for conflicts
        'kboth': 'first',
        'kneither': 'first',
        'contrast': 'first',
        'stative': 'first',
        'negated_p': 'first',
        'Kp': 'first',
        'question': 'first',
        'fc': 'first'
    }
    
    summary_df = merged_df.groupby(group_keys).agg(agg_funcs).reset_index()

    # 5. Post-Process (Resolve Conflicts and Add Missing Columns)
    
    # Resolve judgments to get 'can_express'
    summary_df['can_express'] = summary_df['norm_judgment'].apply(resolve_judgments)
    
    # Add 'comments' column for conflicts
    summary_df['comments'] = np.where(
        summary_df['can_express'] == '?', 'Conflicting evidence.', ''
    )
    
    # Rename evidence ref column
    summary_df = summary_df.rename(columns={'ref_ev': 'evidence'})

    # 6. Final Formatting
    # Define and order final columns (removed 'negation')
    output_columns = [
        'expression', 'full_form', 'shorthand', 
        'kboth', 'kneither', 'contrast', 'stative', 'negated_p', 'Kp', 'question', 'fc', 
        'can_express', 'evidence', 'comments'
    ]
    
    # Ensure all required columns exist, fill with NaN if any are missing
    for col in output_columns:
        if col not in summary_df.columns:
            summary_df[col] = np.nan
            
    final_df = summary_df[output_columns].sort_values(by=group_keys)
    
    return final_df

# --- Main execution ---
if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Change these file paths to process a new language
    
    # Using Hausa files as the example:
    QUESTIONNAIRE_FILE = 'questionnaire_table.csv'
    EXAMPLE_FILE = 'Turkish_examples.csv' # e.g., 'Hausa_examples.csv'
    EVIDENCE_FILE = 'Turkish_evidence.csv'   # e.g., 'Hausa_evidence.csv'
    OUTPUT_FILE = 'Turkish_summary_generated_no_negation.csv' # e.g., 'Hausa_summary_generated.csv'
    
    # --- END CONFIGURATION ---

    print(f"Generating summary table (no negation) from:\n  {QUESTIONNAIRE_FILE}\n  {EXAMPLE_FILE}\n  {EVIDENCE_FILE}\n")
    
    summary_table = generate_summary_table(QUESTIONNAIRE_FILE, EXAMPLE_FILE, EVIDENCE_FILE)
    
    if summary_table is not None:
        # Save the resulting table to a new CSV file
        summary_table.to_csv(OUTPUT_FILE, index=False, na_rep='NaN')
        print(f"Successfully generated and saved summary table to:\n  {OUTPUT_FILE}")

