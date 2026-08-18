import csv
import os
from pathlib import Path


CSV_PATH = os.path.join(
    Path(__file__).parent.parent.parent,
    "kode_wilayah_tingkat_iv_detail.csv"
)

_REGIONS_CACHE = None


def load_regions_from_csv():
    """Load region data from CSV file."""
    if not os.path.exists(CSV_PATH):
        return {}

    regions = {}

    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                prov_code = row.get("kode_provinsi", "").strip()
                prov_name = row.get("nama_provinsi", "").strip()

                kabu_code = row.get("kode_kabupaten_kota", "").strip()
                kabu_name = row.get("nama_kabupaten_kota", "").strip()

                kec_code = row.get("kode_kecamatan", "").strip()
                kec_name = row.get("nama_kecamatan", "").strip()

                desa_code = row.get("kode_desa_kelurahan", "").strip()
                desa_name = row.get("nama_desa_kelurahan", "").strip()

                if not (prov_code and kabu_code and kec_code and desa_code):
                    continue

                if prov_code not in regions:
                    regions[prov_code] = {
                        "name": prov_name,
                        "code": prov_code,
                        "level": 1,
                        "children": {}
                    }

                prov_obj = regions[prov_code]

                if kabu_code not in prov_obj["children"]:
                    prov_obj["children"][kabu_code] = {
                        "name": kabu_name,
                        "code": kabu_code,
                        "level": 2,
                        "children": {}
                    }

                kabu_obj = prov_obj["children"][kabu_code]

                if kec_code not in kabu_obj["children"]:
                    kabu_obj["children"][kec_code] = {
                        "name": kec_name,
                        "code": kec_code,
                        "level": 3,
                        "children": {}
                    }

                kec_obj = kabu_obj["children"][kec_code]

                if desa_code not in kec_obj["children"]:
                    kec_obj["children"][desa_code] = {
                        "name": desa_name,
                        "code": desa_code,
                        "level": 4
                    }

        return regions

    except Exception as e:
        print(f"Error loading regions CSV: {e}")
        return {}


def get_regions_cache():
    """Get cached regions or load from CSV."""
    global _REGIONS_CACHE

    if _REGIONS_CACHE is None:
        _REGIONS_CACHE = load_regions_from_csv()

    return _REGIONS_CACHE


def get_all_provinces():
    """Get all provinces (level 1)."""
    regions = get_regions_cache()

    return [
        {
            "code": code,
            "name": data["name"]
        }
        for code, data in sorted(regions.items())
    ]


def get_kabupaten_by_province(prov_code):
    """Get kabupaten/kota by province code (level 2)."""
    regions = get_regions_cache()

    if prov_code not in regions:
        return []

    prov = regions[prov_code]

    return [
        {
            "code": code,
            "name": data["name"]
        }
        for code, data in sorted(prov["children"].items())
    ]


def get_kecamatan_by_kabupaten(kabu_code):
    """Get kecamatan by kabupaten code (level 3)."""
    regions = get_regions_cache()

    parts = kabu_code.split(".")

    if len(parts) < 2:
        return []

    prov_code = parts[0]

    if prov_code not in regions:
        return []

    prov = regions[prov_code]

    if kabu_code not in prov["children"]:
        return []

    kabu = prov["children"][kabu_code]

    return [
        {
            "code": code,
            "name": data["name"]
        }
        for code, data in sorted(kabu["children"].items())
    ]


def get_desa_by_kecamatan(kec_code):
    """Get desa/kelurahan by kecamatan code (level 4)."""
    regions = get_regions_cache()

    parts = kec_code.split(".")

    if len(parts) < 3:
        return []

    prov_code = parts[0]

    kabu_code = ".".join(parts[:2])

    if prov_code not in regions:
        return []

    prov = regions[prov_code]

    if kabu_code not in prov["children"]:
        return []

    kabu = prov["children"][kabu_code]

    if kec_code not in kabu["children"]:
        return []

    kec = kabu["children"][kec_code]

    return [
        {
            "code": code,
            "name": data["name"]
        }
        for code, data in sorted(kec["children"].items())
    ]


def get_region_by_code(code):
    """Get full region info by code (any level)."""
    regions = get_regions_cache()

    parts = code.split(".")

    if len(parts) == 1:
        if code in regions:
            return regions[code]

    elif len(parts) == 2:
        prov_code = parts[0]

        if prov_code in regions and code in regions[prov_code]["children"]:
            return regions[prov_code]["children"][code]

    elif len(parts) == 3:
        prov_code = parts[0]

        kabu_code = ".".join(parts[:2])

        if (
            prov_code in regions
            and kabu_code in regions[prov_code]["children"]
            and code in regions[prov_code]["children"][kabu_code]["children"]
        ):
            return regions[prov_code]["children"][kabu_code]["children"][code]

    elif len(parts) == 4:
        prov_code = parts[0]

        kabu_code = ".".join(parts[:2])

        kec_code = ".".join(parts[:3])

        if (
            prov_code in regions
            and kabu_code in regions[prov_code]["children"]
            and kec_code in regions[prov_code]["children"][kabu_code]["children"]
            and code in regions[prov_code]["children"][kabu_code]["children"][kec_code]["children"]
        ):
            return regions[prov_code]["children"][kabu_code]["children"][kec_code]["children"][code]

    return None
