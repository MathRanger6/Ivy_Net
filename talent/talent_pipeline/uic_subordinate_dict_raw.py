"""
Canonical seed dictionary for top-level UIC hierarchy anchors.
"""

from copy import deepcopy

UIC_SUBORDINATE_ROWS = [
    ("WDDDFF", {"top_name": "75RR", "simplename": "75RR", "class": "RGR", "sub_class": "rgr", "uic_pde": None, "description": "75th Ranger Regiment", "sub_units_by_fy": dict()}),
    ("WDSTFF", {"top_name": "160SOAR", "simplename": "160SOAR", "class": "SOAR", "sub_class": "soar", "uic_pde": None, "description": "160th SOAR Spec Opns Aviation Regiment", "sub_units_by_fy": dict()}),
    ("WH1DFF", {"top_name": "1SFG", "simplename": "1SFG", "class": "SFG", "sub_class": "sfg", "uic_pde": None, "description": "1SFG - 1st Special Forces Group", "sub_units_by_fy": dict()}),
    ("WA4WFF", {"top_name": "3SFG", "simplename": "3SFG", "class": "SFG", "sub_class": "sfg", "uic_pde": None, "description": "3SFG - 3rd Special Forces Group", "sub_units_by_fy": dict()}),
    ("WH03FF", {"top_name": "5SFG", "simplename": "5SFG", "class": "SFG", "sub_class": "sfg", "uic_pde": None, "description": "5SFG - 5th Special Forces Group", "sub_units_by_fy": dict()}),
    ("WH0YFF", {"top_name": "7SFG", "simplename": "7SFG", "class": "SFG", "sub_class": "sfg", "uic_pde": None, "description": "7SFG - 7th Special Forces Group", "sub_units_by_fy": dict()}),
    ("WH08FF", {"top_name": "10SFG", "simplename": "10SFG", "class": "SFG", "sub_class": "sfg", "uic_pde": None, "description": "10SFG - 10th Special Forces Group", "sub_units_by_fy": dict()}),
    ("WJTDFF", {"top_name": "528SB", "simplename": "528SB", "class": "SFG", "sub_class": "sfg", "uic_pde": None, "description": "528 SusBde - 528th Sustainment Brigade", "sub_units_by_fy": dict()}),
    ("WAMHFF", {"top_name": "1ID", "simplename": "(HDIV) 1ID", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "ZUREYPSUHX", "description": "1ID - 1st Infantry Division", "sub_units_by_fy": dict()}),
    ("WAH4FF", {"top_name": "2ID", "simplename": "(HDIV) 2ID", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "FXEVANSUHX", "description": "2ID - 2nd Infantry Division", "sub_units_by_fy": dict()}),
    ("WAQJFF", {"top_name": "3ID", "simplename": "(HDIV) 3ID", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "DXZEW3SUHX", "description": "3ID - 3rd Infantry Division", "sub_units_by_fy": dict()}),
    ("WANGFF", {"top_name": "4ID", "simplename": "(HDIV) 4ID", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "X5YMUF5UHX", "description": "4ID - 4th Infantry Division", "sub_units_by_fy": dict()}),
    ("W5AAFF", {"top_name": "7ID", "simplename": "(HDIV) 7ID", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "6BARMCSUHX", "description": "7ID - 7th Infantry Division", "sub_units_by_fy": dict()}),
    ("WAPBFF", {"top_name": "1AD", "simplename": "(HDIV) 1AD", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "VRKP92SUHX", "description": "1AD - 1st Armored Division", "sub_units_by_fy": dict()}),
    ("WAGEFF", {"top_name": "1CAV", "simplename": "(HDIV) 1CD", "class": "HDIV", "sub_class": "hdiv", "uic_pde": "FXSNLZSUHX", "description": "1CD - 1st Cavalry Division", "sub_units_by_fy": dict()}),
    ("WAA6FF", {"top_name": "82ABN", "simplename": "(LDIV) 82ABD", "class": "LDIV", "sub_class": "ldiv", "uic_pde": "5HNR3XSUHX", "description": "82ABN - 82nd Airborne Division", "sub_units_by_fy": dict()}),
    ("WAB1FF", {"top_name": "101ABN", "simplename": "(LDIV) 101ABD", "class": "LDIV", "sub_class": "ldiv", "uic_pde": "Y8AV8TSUHX", "description": "101ABN - 101st Airborne Division", "sub_units_by_fy": dict()}),
    ("WAAAFF", {"top_name": "11ABN", "simplename": "(LDIV) 11ABD", "class": "LDIV", "sub_class": "ldiv", "uic_pde": None, "description": "11ABN - 11th Airborne Division", "sub_units_by_fy": dict()}),
    ("WGKEFF", {"top_name": "10MTN", "simplename": "(LHDIV) 10MD", "class": "LDIV", "sub_class": "ldiv", "uic_pde": "XJ7BT35UHX", "description": "10MTN - 10th Mountain Division", "sub_units_by_fy": dict()}),
    ("WALXFF", {"top_name": "25ID", "simplename": "(HDIV) 25ID", "class": "LDIV", "sub_class": "ldiv", "uic_pde": "XOASESUHX", "description": "25ID - 25th Infantry Division", "sub_units_by_fy": dict()}),
    ("WKCSFF", {"top_name": "1SFAB", "simplename": "(SFAB) 1 SFAB", "class": "SFAB", "sub_class": "sfab", "uic_pde": "", "description": "1SFAB - 1st Security Force Assistance Bde", "sub_units_by_fy": dict()}),
    ("WKD7FF", {"top_name": "2SFAB", "simplename": "(SFAB) 2 SFAB", "class": "SFAB", "sub_class": "sfab", "uic_pde": "", "description": "2SFAB - 2nd Security Force Assistance Bde", "sub_units_by_fy": dict()}),
    ("WKDGFF", {"top_name": "3SFAB", "simplename": "(SFAB) 3 SFAB", "class": "SFAB", "sub_class": "sfab", "uic_pde": "", "description": "3SFAB - 3rd Security Force Assistance Bde", "sub_units_by_fy": dict()}),
    ("WKDPFF", {"top_name": "4SFAB", "simplename": "(SFAB) 4 SFAB", "class": "SFAB", "sub_class": "sfab", "uic_pde": "", "description": "4SFAB - 4th Security Force Assistance Bde", "sub_units_by_fy": dict()}),
    ("WKDWFF", {"top_name": "5SFAB", "simplename": "(SFAB) 5 SFAB", "class": "SFAB", "sub_class": "sfab", "uic_pde": "2NCEEP5UHX", "description": "5SFAB - 5th Security Force Assistance Bde", "sub_units_by_fy": dict()}),
    ("W0AKFF", {"top_name": "USARAK", "simplename": "(XDIV) USARAK", "class": "XDIV", "sub_class": "xdiv", "uic_pde": None, "description": "US Army Alaska Command", "sub_units_by_fy": dict()}),
    ("W3YTFF", {"top_name": "TRADOC", "simplename": "TRADOC", "class": "CMD", "sub_class": "tradoc", "uic_pde": None, "description": "TRADOC - Training and Doctrine Command", "sub_units_by_fy": dict()}),
    ("W0CUFF", {"top_name": "AFC", "simplename": "AFC", "class": "CMD", "sub_class": "afc", "uic_pde": None, "description": "AFC - Army Futures Command", "sub_units_by_fy": dict()}),
    ("W0GWFF", {"top_name": "AMC", "simplename": "AMC", "class": "CMD", "sub_class": "amc", "uic_pde": None, "description": "AMC - Army Materiel Command", "sub_units_by_fy": dict()}),
    ("W3YBFF", {"top_name": "FORSCOM", "simplename": "FORSCOM", "class": "CMD", "sub_class": "forscom", "uic_pde": None, "description": "FORSCOM - Army Forces Command", "sub_units_by_fy": dict()}),
    ("W45VFF", {"top_name": "USASOC", "simplename": "USASOC", "class": "XDIV", "sub_class": "usasoc", "uic_pde": None, "description": "USASOC - US Army Special Operations Command", "sub_units_by_fy": dict()}),
    ("W6UXFF", {"top_name": "ARCYBER", "simplename": "ARCYBER", "class": "CMD", "sub_class": "arcyber", "uic_pde": None, "description": "ARCYBER - Army Cyber Command", "sub_units_by_fy": dict()}),
    ("WJMZFF", {"top_name": "PACOM", "simplename": "PACOM", "class": "CMD", "sub_class": "pacom", "uic_pde": None, "description": "PACOM - Army Pacific Command", "sub_units_by_fy": dict()}),
    ("W0QFFF", {"top_name": "ARTRANS", "simplename": "ARTRANS", "class": "CMD", "sub_class": "artrans", "uic_pde": None, "description": "ARTRANS - Army Transportation Command", "sub_units_by_fy": dict()}),
]


def get_uic_subordinate_dict_raw():
    out = {}
    for uic_key, payload in UIC_SUBORDINATE_ROWS:
        key = uic_key
        if key in out:
            key = f"{payload.get('top_name', 'UNKNOWN')}__{key}"
        out[key] = deepcopy(payload)
    return out