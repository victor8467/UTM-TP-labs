from arsenal.windows.inventar import Proces, Eveniment, Inventar


def test_proces_din_temp_e_suspect():
    p = Proces(1, "x.exe", "ana", "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe")
    assert p.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    p = Proces(2, "svchost.exe", "SYSTEM", "C:\\Windows\\System32\\svchost.exe")
    assert p.e_suspect() is False


def test_eveniment_suspect():
    e1 = Eveniment(4625, "warning", "Security", "admin", "Failed logon")
    e2 = Eveniment(4624, "info", "Security", "ana", "Logged on")
    assert e1.e_suspect() is True
    assert e2.e_suspect() is False


def test_inventar_metode():
    p1 = Proces(1, "x.exe", "ana", "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe")
    p2 = Proces(2, "svchost.exe", "SYSTEM", "C:\\Windows\\System32\\svchost.exe")
    inv = Inventar([p1, p2])
    assert len(inv) == 2
    assert inv.suspecte() == [p1]
    assert inv.pe_user() == {"ana": ["x.exe"], "SYSTEM": ["svchost.exe"]}
