import os
import re
import sys
import argparse


def perform_substitution(input_file, reverse=False):
    """
    Format math block labels in qmd/ipynb files for editing or rendering.
    
    Note that adding cross-reference labels to math blocks adds latency
    to RStudio's math previews. Replacing the space after the fenced math
    block with a newline character (default option) resolves this:
    
        "$$ {#eq-*}" -> "$$\n{#eq-*}".
      
    However, doing so makes the cross-reference label invalid, so this
    action should be reversed (reverse option) prior to rendering:
      
        "$$\n{#eq-*}" -> "$$ {#eq-*}".

    """
    forward_pattern = r"(\$\$\s*)(\s)({#eq-[^}]+})"
    reverse_pattern = r"(\$\$\s*)(\n)({#eq-[^}]+})"
    
    if reverse:
        pattern_before = reverse_pattern
        pattern_after = forward_pattern
        substitution = r"\1 \3"
    else:
        pattern_before = forward_pattern
        pattern_after = reverse_pattern
        substitution = r"\1\n\3"
    
    with open(input_file, 'r') as f:
        content = f.read()

    # Find all matches and perform the substitution
    matches_before = re.findall(pattern_before, content)
    modified_content = re.sub(pattern_before, substitution, content)
    matches_after = re.findall(pattern_after, modified_content)

    # Check if any modifications were made
    if content != modified_content:
        for before, after in zip(matches_before, matches_after):
            print(f"'{''.join(before)}' -> '{''.join(after)}'")
    
        # Overwrite the original file with the modified content
        with open(input_file, 'w') as f:
            f.write(modified_content)
        
        print(f"Processed file written to: {input_file}")
    else:
        print("No modifications needed.")


def main():
    parser = argparse.ArgumentParser(
      description="Format math block labels for editing (spaces to newlines)."
    )
    parser.add_argument(
      "file",
      help="Path to the .qmd/.ipynb file to process."
    )
    parser.add_argument(
      "-r",
      "--reverse",
      action="store_true",
      help="Apply reverse substitution for rendering (newlines to spaces)."
    )

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    perform_substitution(args.file, args.reverse)


if __name__ == "__main__":
    main()
