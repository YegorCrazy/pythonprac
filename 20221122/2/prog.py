import sys
inp = sys.stdin.read()
sys.stdout.write(inp.encode('latin1', 'replace').decode('cp1251', 'replace'))
