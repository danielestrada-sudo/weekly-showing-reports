import os
import glob
import re

for file in glob.glob('*/index.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if we have the broken pattern where a span ends right before the comment
    if re.search(r'</span>\s*<!-- VISITOR LOCATIONS TAB -->', content):
        print(f"Fixing broken HTML in {file}")
        
        # We need to insert \n            </div>\n        </div>\n        right before <!-- VISITOR LOCATIONS TAB -->
        fixed_content = content.replace(
            '</span><!-- VISITOR LOCATIONS TAB -->', 
            '</span>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <!-- VISITOR LOCATIONS TAB -->'
        )
        
        # wait, let me use regex sub to replace anything between </span> and <!-- VISITOR LOCATIONS TAB -->
        fixed_content = re.sub(
            r'</span>\s*<!-- VISITOR LOCATIONS TAB -->',
            r'</span>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <!-- VISITOR LOCATIONS TAB -->',
            content
        )
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
