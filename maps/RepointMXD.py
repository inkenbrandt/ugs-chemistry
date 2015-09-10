# repoint mxds at dev or AT Database
# requires that you have database connections in
# catalog with the names below
import arcpy
import glob
import sys


db = r'Database Connections\\'
local = db + 'UGSWaterChemistry as dbo.sde'
dev = db + 'UGSWaterChemistry_TEST as ugswaterchemistry.sde'
at = db + ''
target = None

if len(sys.argv) > 1:
    target = sys.argv[1]

if not target:
    target = raw_input('Local (L), Dev (D), or AT (A)? ')

if target == 'D':
    dest = dev
elif target == 'A':
    dest = at
else:
    dest = local

print('updating mxd\'s to use {}'.format(dest))

for f in glob.glob('*.mxd'):
    print(f)
    mxd = arcpy.mapping.MapDocument(f)
    l = arcpy.mapping.ListLayers(mxd)[0]
    mxd.findAndReplaceWorkspacePaths(l.workspacePath, dest, True)
    mxd.save()

print('done')
