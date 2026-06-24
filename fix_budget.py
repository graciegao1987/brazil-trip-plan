import sys

path = '/Users/gracegao/WorkBuddy/2026-06-24-14-17-12/brazil_trip_plan.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix budgetData object - replace the corrupted lines
old_budget = """var budgetData = {
  total:  { flight:'$,700', stay:'$', food:'$', ticket:'$', transport:'$', shop:'$', total:'$,100', subtitle:'三人总计 $3,100（机票按$900/人）', bars:[90,5,3,2,1,1] },
  person: { flight:'$',   stay:'$',  food:'$', ticket:'$', transport:'$', shop:'$', total:'~$1,033', subtitle:'人均约 $1,033（机票按$900/人）', bars:[87,5,3,2,1,1] }
};"""

new_budget = """var budgetData = {
  total:  { flight:'$2,700', stay:'$150', food:'$100', ticket:'$60', transport:'$40', shop:'$50', total:'$3,100', subtitle:'\u4e09\u4eba\u603b\u8ba1 $3,100\uff08\u98de\u7968\u6309$900/\u4eba\uff09', bars:[90,5,3,2,1,1] },
  person: { flight:'$900',   stay:'$50',  food:'$33', ticket:'$20', transport:'$13', shop:'$17', total:'~$1,033', subtitle:'\u4eba\u5747\u7ea6 $1,033\uff08\u98de\u7968\u6309$900/\u4eba\uff09', bars:[87,5,3,2,1,1] }
};"""

if old_budget in content:
    content = content.replace(old_budget, new_budget)
    print('Replaced budgetData successfully')
else:
    print('Could not find old budgetData')
    # Try to find it with flexible matching
    import re
    # Replace the whole var budgetData block
    new_block = '''var budgetData = {
  total:  { flight:'$2,700', stay:'$150', food:'$100', ticket:'$60', transport:'$40', shop:'$50', total:'$3,100', subtitle:'\u4e09\u4eba\u603b\u8ba1 $3,100', bars:[90,5,3,2,1,1] },
  person: { flight:'$900',   stay:'$50',  food:'$33', ticket:'$20', transport:'$13', shop:'$17', total:'~$1,033', subtitle:'\u4eba\u5747\u7ea6 $1,033', bars:[87,5,3,2,1,1] }
};'''
    # Use regex to replace the block
    pattern = r'var budgetData\s*=\s*\{[^}]+\},\s*person:\s*\{[^}]+\}\s*;'
    if re.search(pattern, content):
        content = re.sub(pattern, new_block, content, count=1)
        print('Replaced budgetData via regex')
    else:
        print('Regex also failed to match')
        # Show what's around line 1272
        lines = content.split('\n')
        for i in range(1270, min(1276, len(lines))):
            print(f'Line {i+1}: {repr(lines[i][:100])}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('File written')
