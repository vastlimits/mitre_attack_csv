# MITRE ATT&amp;CK in CSV form

[![Rebuild the CSV from the latest JSON data](https://github.com/sduff/mitre_attack_csv/actions/workflows/main.yml/badge.svg)](https://github.com/sduff/mitre_attack_csv/actions/workflows/main.yml)

The uberAgent ESA Splunk app shows MITRE ATT&CK &copy; information for events. The information is stored in a CSV file that serves as the basis for a Splunk lookup. Every release comes with the newest ATT&CK information but if one wants the latest information between uberAgent releases, they may download the latest [annotation_mitre_attack.csv](https://raw.githubusercontent.com/vastlimits/mitre_attack_csv/main/annotation_mitre_attack.csv) anytime.

The CSV gets updated with the latest [ATT&CK Enterprise Techniques](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json) on a daily basis, if there are any changes to the source.

For more information please visit the [uberAgent documentation](https://docs.citrix.com/en-us/uberagent/current-release/)

This repository leverages the MITRE ATT&CK Enterprise Techniques data from https://github.com/mitre/cti, but is not associated with MITRE.

&copy; 2021 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.
https://attack.mitre.org/resources/terms-of-use/
