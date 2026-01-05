# # case_type_map.py

# # -------------------------
# # Civil case types
# # -------------------------
# CIVIL_CASE_MAP = {
#     "AO": "AO - Appeal from Order",
#     "ARA": "ARA - Arbitration Appeal",
#     "ARP": "ARP - Arbitration Petition",
#     "CAO": "CAO - CA in Others(MCA/TXA/CA)",
#     "CAP": "CAP - Civil Appl. in ARP",
#     "CA": "CA - Civil Application",
#     "CAA": "CAA - Civil Application in AO",
#     "CAE": "CAE - Civil Application in C.REF",
#     "CAT": "CAT - Civil Application in CAPL",
#     "CAN": "CAN - Civil Application in CP",
#     "CAC": "CAC - Civil Application in CRA",
#     "CAF": "CAF - Civil Application in FA",
#     "CAM": "CAM - Civil Application in FCA",
#     "CAFM": "CAFM - Civil Application In FEMA",
#     "CAY": "CAY - Civil Application in FERA",
#     "CAL": "CAL - Civil Application in LPA",
#     "CAI": "CAI - Civil Application in PIL",
#     "CAS": "CAS - Civil Application in SA",
#     "CAW": "CAW - Civil Application in WP",
#     "CAR": "CAR - Civil Appln. in ARA",
#     "C.REF": "C.REF - Civil References",
#     "CRA": "CRA - Civil Revision Application",
#     "SMCPC": "SMCPC - Civil Suo Motu Contempt Petition",
#     "WP": "Civil Writ Petition",
#     "COMAO": "COMAO - Commercial AO",
#     "COARA": "COARA - Commercial Arbitration Appeal",
#     "COARP": "COARP - Commercial Arbitration Petition",
#     "CCAPL": "CCAPL - Commercial Contempt Appeal",
#     "COMCP": "COMCP - Commercial Contempt Petition",
#     "COMFA": "COMFA - Commercial FA",
#     "CP": "CP - Cont. Petition",
#     "CAPL": "CAPL - Contempt Appeal",
#     "CRR": "CRR - Court Receiver Report",
#     "COXOB": "COXOB - Cross Objection In Commercial FA/ARA/CO/ARP/CP/CA",
#     "XOB": "XOB - Cross Objection Stamp",
#     "FCA": "FCA - Family Court Appeal",
#     "FEMA": "FEMA - FEMA Appeal",
#     "FERA": "FERA - FERA Appeal",
#     "FA": "FA - First Appeal",
#     "IA": "IA - INTERIM APPLICATION",
#     "LPA": "LPA - Letter Patent Appeal",
#     "MPA": "MPA - Marriage Petition (A)",
#     "MCA": "MCA - Misc.Civil Application",
#     "PIL": "PIL - Public Interest Litigation",
#     "RC": "RC - Rejected Case",
#     "RPF": "RPF - Review Pent. in FA",
#     "RAP": "RAP - Review Petition in ARA",
#     "COMRP": "COMRP - Review Petition In Commercial FA/ARA/AO/ARP/CP/CA",
#     "RPFM": "RPFM - Review Petition In FEMA Appeal",
#     "RPIA": "RPIA - REVIEW PETITION IN IA",
#     "RPV": "RPV - Review Petition in MCA",
#     "RPI": "RPI - Review Petition In PIL",
#     "RPA": "RPA - Review Petn. in AO",
#     "RPR": "RPR - Review Petn. in ARP",
#     "RPT": "RPT - Review Petn. in CAPL",
#     "RPN": "RPN - Review Petn. in CP",
#     "RPC": "RPC - Review Petn. in CRA",
#     "RPM": "RPM - Review Petn. in FCA",
#     "RPL": "RPL - Review Petn. in LPA",
#     "RPS": "RPS - Review Petn. in SA",
#     "RPW": "RPW - Review Petn. in WP",
#     "SA": "Second Appeal",
#     "SMP": "SMP - Suo Moto Petition",
#     "SMWP": "SMWP - Suo Motu Writ Petition",
#     "SMPIL": "SMPIL - Suo Motuo PIL",
#     "TXA": "TXA - Tax Appeal",
#     "XFER": "XFER - Transfer Case",
# }

# # -------------------------
# # Criminal case types
# # -------------------------
# CRIMINAL_CASE_MAP = {
#     "APPSC": "APPSC - Application in Cr. Suo Moto CONP",
#     "ALP": "ALP - Appln For Leave To Appeal(PVT.)",
#     "ALS": "ALS - Appln For Leave to Appeal(STATE)",
#     "ABA": "ABA - Cr. Anticipatory Bail Appln.",
#     "APPA": "APPA - Cr. Application in Appeal",
#     "APPP": "APPP - Cr. Application in Application",
#     "APPCO": "APPCO - Cr. Application in Confirmation",
#     "APPCP": "APPCP - Cr. Application in Contempt",
#     "APPI": "APPI - Cr. Application in PIL",
#     "APPCR": "APPCR - Cr. Application in Reference",
#     "APPR": "APPR - Cr. Application in Revision",
#     "APPW": "APPW - Cr. Application in Writ Petition",
#     "APL": "APL - Cr. Application U/s 482",
#     "BA": "BA - Cr. Bail Application",
#     "CRPIL": "CRPIL - Cr. Public Interest Litigation",
#     "SMCP": "SMCP - Cr. Suo-Motu Contempt Petn.",
#     "SOMO": "SOMO - Cr. Suo-Motu Petition",
#     "SMRN": "SMRN - Cr. Suo-Motu Revision Appln.",
#     "SMWP": "SMWP - Cr. Suo-Motu Writ Petition",
#     "APEAL": "APEAL - Criminal Appeal",
#     "APPLN": "APPLN - Criminal Application",
#     "CONF": "CONF - Criminal Confirmation Case",
#     "CONP": "CONP - Criminal Contempt Petition",
#     "REF": "REF - Criminal Reference",
#     "REVW": "REVW - Criminal Review",
#     "REVN": "REVN - Cr. Revision Appln.",
#     "SMAP": "SMAP - Criminal Suo-Motu Application",
#     "WP": "Cr. Writ Petition",
#     "IA": "IA - INTERIM APPLICATION",
#     "SMP": "SMP - Suo-Motu Cr. PIL",
# }

# # -------------------------
# # Resolver function
# # -------------------------
# def resolve_case_type(case_type_raw: str) -> str:
#     """
#     Convert Excel short form (e.g. 'WP', 'Cr.WP', 'Cr.ABA') 
#     into the exact dropdown text for the Bombay HC site.
#     """
#     case_type_raw = case_type_raw.strip()

#     if case_type_raw.startswith("Cr."):
#         short = case_type_raw.replace("Cr.", "").strip()
#         if short in CRIMINAL_CASE_MAP:
#             return CRIMINAL_CASE_MAP[short]
#         else:
#             raise ValueError(f"Unknown criminal case type: {short}")
#     else:
#         short = case_type_raw
#         if short in CIVIL_CASE_MAP:
#             return CIVIL_CASE_MAP[short]
#         else:
#             raise ValueError(f"Unknown civil case type: {short}")
# case_type_map.py

# -------------------------
# Civil case types
# -------------------------
# -------------------------
# Civil case types
# -------------------------
CIVIL_CASE_MAP = {
    "AO": "Appeal from Order",
    "ARA": "Arbitration Appeal",
    "ARP": "Arbitration Petition",
    "CAO": "CA in Others(MCA/TXA/CA)",
    "CAP": "Civil Appl. in ARP",
    "CA": "Civil Application",
    "CAA": "Civil Application in AO",
    "CAE": "Civil Application in C.REF",
    "CAT": "Civil Application in CAPL",
    "CAN": "Civil Application in CP",
    "CAC": "Civil Application in CRA",
    "CAF": "Civil Application in FA",
    "CAM": "Civil Application in FCA",
    "CAFM": "Civil Application In FEMA",
    "CAY": "Civil Application in FERA",
    "CAL": "Civil Application in LPA",
    "CAI": "Civil Application in PIL",
    "CAS": "Civil Application in SA",
    "CAW": "Civil Application in WP",
    "CAR": "Civil Appln. in ARA",
    "CREF": "Civil References",          # normalized from "C.REF"
    "CRA": "Civil Revision Application",
    "SMCPC": "Civil Suo Motu Contempt Petition",
    "WP": "Civil Writ Petition",         # exact dropdown text
    "COMAO": "Commercial AO",
    "COARA": "Commercial Arbitration Appeal",
    "COARP": "Commercial Arbitration Petition",
    "CCAPL": "Commercial Contempt Appeal",
    "COMCP": "Commercial Contempt Petition",
    "COMFA": "Commercial FA",
    "CP": "Contempt Petition",
    "CAPL": "Contempt Appeal",
    "CRR": "Court Receiver Report",
    "COXOB": "Cross Objection In Commercial FA/ARA/CO/ARP/CP/CA",
    "XOB": "Cross Objection Stamp",
    "FCA": "Family Court Appeal",
    "FEMA": "FEMA Appeal",
    "FERA": "FERA Appeal",
    "FA": "First Appeal",
    "IA": "INTERIM APPLICATION",
    "LPA": "Letter Patent Appeal",
    "MPA": "Marriage Petition (A)",
    "MCA": "Misc.Civil Application",
    "PIL": "Public Interest Litigation",
    "RC": "Rejected Case",
    "RPF": "Review Petition in FA",
    "RAP": "Review Petition in ARA",
    "COMRP": "Review Petition In Commercial FA/ARA/AO/ARP/CP/CA",
    "RPFM": "Review Petition In FEMA Appeal",
    "RPIA": "Review Petition in IA",
    "RPV": "Review Petition in MCA",
    "RPI": "Review Petition In PIL",
    "RPA": "Review Petition in AO",
    "RPR": "Review Petition in ARP",
    "RPT": "Review Petition in CAPL",
    "RPN": "Review Petition in CP",
    "RPC": "Review Petition in CRA",
    "RPM": "Review Petition in FCA",
    "RPL": "Review Petition in LPA",
    "RPS": "Review Petition in SA",
    "RPW": "Review Petition in WP",
    "SA": "Second Appeal",               # exact dropdown text
    "SMP": "Suo Moto Petition",
    "SMWP": "Suo Motu Writ Petition",
    "SMPIL": "Suo Motu PIL",
    "TXA": "Tax Appeal",
    "XFER": "Transfer Case",
}

# -------------------------
# Criminal case types
# -------------------------
CRIMINAL_CASE_MAP = {
    "APPSC": "Application in Cr. Suo Moto CONP",
    "ALP": "Appln For Leave To Appeal(PVT.)",
    "ALS": "Appln For Leave to Appeal(STATE)",
    "ABA": "Anticipatory Bail Application",
    "APPA": "Application in Appeal",
    "APPP": "Application in Application",
    "APPCO": "Application in Confirmation",
    "APPCP": "Application in Contempt",
    "APPI": "Application in PIL",
    "APPCR": "Application in Reference",
    "APPR": "Application in Revision",
    "APPW": "Application in Writ Petition",
    "APL": "Application U/s 482",
    "BA": "Bail Application",
    "CRPIL": "Criminal Public Interest Litigation",
    "SMCP": "Suo-Motu Contempt Petition",
    "SOMO": "Suo-Motu Petition",
    "SMRN": "Suo-Motu Revision Application",
    "SMWP": "Suo-Motu Writ Petition",
    "APEAL": "Criminal Appeal",
    "APPLN": "Criminal Application",
    "CONF": "Criminal Confirmation Case",
    "CONP": "Criminal Contempt Petition",
    "REF": "Criminal Reference",
    "REVW": "Criminal Review",
    "REVN": "Criminal Revision Application",
    "SMAP": "Criminal Suo-Motu Application",
    # Do NOT map "WP" here. Use "CR.WP" or explicit criminal string:
    "CRWP": "Criminal Writ Petition",    # normalized shorthand support
    "IA": "INTERIM APPLICATION",
    "SMP": "Suo-Motu Criminal PIL",
}

# -------------------------
# Resolver function
# -------------------------
def resolve_case_type(case_type_raw: str) -> str:
    """
    Convert Excel input (e.g., 'WP', 'Cr.WP', 'SA - Second Appeal', 'Cr. WP')
    into the exact dropdown text.
    """
    raw = (case_type_raw or "").strip()

    # Extract side hint and clean
    is_criminal = raw.lower().startswith("cr")
    # Remove common prefixes and punctuation, normalize
    cleaned = raw.replace("Cr.", "").replace("Cr", "").strip()
    # Remove descriptive suffix after hyphen (e.g., "SA - Second Appeal")
    if " - " in cleaned:
        cleaned = cleaned.split(" - ")[0].strip()
    # Normalize dots in keys (e.g., C.REF -> CREF)
    cleaned_key = cleaned.replace(".", "").upper()

    # Resolve by side
    if is_criminal:
        # Special cases for criminal writs typed as "Cr.WP" or "CR.WP"
        if cleaned_key in ("CRWP", "CWP", "WP"):
            return "Criminal Writ Petition"
        if cleaned_key in CRIMINAL_CASE_MAP:
            return CRIMINAL_CASE_MAP[cleaned_key]
        raise ValueError(f"Unknown criminal case type: {cleaned}")
    else:
        if cleaned_key in CIVIL_CASE_MAP:
            return CIVIL_CASE_MAP[cleaned_key]
        # Friendly fallbacks for common verbose inputs
        if cleaned_key.startswith("SA"):
            return "Second Appeal"
        if cleaned_key.startswith("WP"):
            return "Civil Writ Petition"
        raise ValueError(f"Unknown civil case type: {cleaned}")
