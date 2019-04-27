CLICOL PLUGIN ASPATH
====================
Plugin for clicol which helps troubleshooting by resolving sitecodes for AS path.

Example:

	 * i  10.0.35.48/28    10.123.123.158           0    100      0 21302 13979 65120 64932 ? ATT ABC --- EFH
	 *>                    10.123.234.154                         0 21302 13979 65120 64932 ? ATT ABC --- EFH

Sitecode mappings are read from `~/.clicol/plugin-aspath.db`.
Format of that file:
{ASNUM}\t{DESCRIPTION}\t{SITECODE}

More column is ok. Column separator is TAB!
Example:
	21302   AT&T EAME       ATT     -       Vendor
	13979   AT&T NA ATT

