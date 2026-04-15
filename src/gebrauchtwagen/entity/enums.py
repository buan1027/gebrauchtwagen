"""Enumerationen fuer Gebrauchtwagen-Attribute."""

from __future__ import annotations

import enum


class Kraftstoffart(enum.StrEnum):
    """Kraftstoffart eines Fahrzeugs."""

    BENZIN = "BENZIN"
    DIESEL = "DIESEL"
    ELEKTRO = "ELEKTRO"
    HYBRID = "HYBRID"
    ERDGAS = "ERDGAS"
    WASSERSTOFF = "WASSERSTOFF"


class Fahrzeugklasse(enum.StrEnum):
    """Fahrzeugklasse eines Fahrzeugs."""

    KLEINWAGEN = "KLEINWAGEN"
    KOMPAKTKLASSE = "KOMPAKTKLASSE"
    MITTELKLASSE = "MITTELKLASSE"
    OBERKLASSE = "OBERKLASSE"
    SUV = "SUV"
    KOMBI = "KOMBI"
    CABRIO = "CABRIO"
    TRANSPORTER = "TRANSPORTER"
