Promotion Receipts + Diff Visibility Bundle v1

Purpose:
- upgrade repo_root promotion so every promotion writes:
  - a promotion receipt under payload/integrity/promotions/
  - before/after hashes
  - unified diff output for promoted text files
- keep workflow promotion disabled by default

Outputs:
- logs/repo_root_promotions.json
- payload/integrity/promotions/promotion_0001.json, etc.

Diff visibility:
- includes unified diff lines in the receipt
- truncated at max_diff_lines from config/repo_root_promoter_rules.json
