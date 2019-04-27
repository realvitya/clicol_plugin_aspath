CLICOL PLUGIN ASPATH
====================
Plugin for clicol which helps troubleshooting by resolving sitecodes for AS path.

Example:

	 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ? __ATT ABC --- EFH__
	 *>                    10.123.234.154                         0 21302 13979 65120 64932 ? __ATT ABC --- EFH__

Sitecode mappings are read from `~/.clicol/plugin-aspath.db`.

Format of that file:
`{ASNUM}\t{DESCRIPTION}\t{SITECODE}`

3 columns required, more columns are ok. Column separator is TAB!
Example:

	21302	AT&T EAME	ATT	-	Vendor
	13979	AT&T NA	ATT

