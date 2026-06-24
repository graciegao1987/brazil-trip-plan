import sys

path = '/Users/gracegao/WorkBuddy/2026-06-24-14-17-12/brazil_trip_plan.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the budgetData lines (around line 1272-1275, 0-indexed: 1271-1274)
# Build correct budgetData block
correct_block = """var budgetData = {
  total:  { flight:'$2,700', stay:'$150', food:'$100', ticket:'$60', transport:'$40', shop:'$50', total:'$3,100', subtitle:'\u4e09\u4eba\u603b\u8ba1 $3,100\uff08\u98de\u7968\u6309$900/\u4eba\uff09', bars:[90,5,3,2,1,1] },
  person: { flight:'$900',   stay:'$50',  food:'$33', ticket:'$20', transport:'$13', shop:'$17', total:'~$1,033', subtitle:'\u4eba\u5747\u7ea6 $1,033\uff08\u98de\u7968\u6309$900/\u4eba\uff09', bars:[87,5,3,2,1,1] }
};
"""

# Find the start line
start = -1
for i, line in enumerate(lines):
    if 'var budgetData' in line or 'var budgetData' in line or 'budgetData' in line:
        # Check if this line starts with 'var budgetData'
        if 'var budgetData' in line:
            start = i
            break

if start >= 0:
    # Find the end line (the '};' line)
    end = -1
    for i in range(start, min(start + 10, len(lines))):
        if '};' in lines[i] and ('person' in lines[i] or i > start + 2):
            end = i
            break
    
    if end >= 0:
        # Replace lines[start:end+1] with correct block
        new_lines = correct_block.split('\n')
        # Add newline to each line except last
        new_lines = [l + '\n' for l in new_lines if l]
        lines[start:end+1] = new_lines
        
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f'Fixed budgetData: replaced lines {start+1}-{end+1}')
    else:
        print('Could not find end of budgetData block')
        # Show surrounding lines
        for i in range(max(0,start-2), min(start+8, len(lines))):
            print(f'  {i+1}: {repr(lines[i][:120])}')
else:
    print('Could not find budgetData in file')
    # Search for it
    for i, line in enumerate(lines):
        if 'budget' in line.lower():
            print(f'  Found "budget" at line {i+1}: {repr(line[:100])}')
