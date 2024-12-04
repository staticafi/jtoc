# Bojový plán

# 19. až 21.10.
- Pomenovanie premenných a funkcií [X]
- volanie funkcií [X]
    - deklarácie funkcií [X]
- printf [X]

# 22. až 28.10.
- `class`, `new`, `interface`
- metódy na triedach [OK]
- predávanie tried ako argument [OK]
- dedičnosť [OK]
- overriding [OK]

# 29. až 4.11.
- lambda výrazy [OK]
- statické triedy [OK]
- stringy [OK]
- array [OK]
- výnimky [OK] 
- threading []
- testy na benchmarkoch [] PRIORITY

- text bakalárky
    - úvod
    - prehľad
        - malo by zaznieť všetko, s čím pracujeme v prototype
        - krátky popis jednotlivých častí goto programov / symbol table

    - rozhodnutie
        - pojednanie o výhodách a nevýchodách iných prístupov
        - prečo sme sa rozhodli pre jbmc - hlavné argumenty

    - implementácia JtoC
        - dizajn - návrhové rozhodnutia
        - myšlienka niekoľkých transformačných passov/prechodov
        - popis vnútornej štruktúry - ast / gramatika
        - ukázať transformaáciu z javy do c na konkrétnom príklade
        - podsekcia obmedzenia/limitations
        - test framework - ako funguje
            - výsledky mojich unit testov
            - pri dizajne testov sme brali zreteľ na sv-comp benchmarky a na základe toho sme navrhovali unit testy.

    - vyhodnotenie / evaluácia
        - popis štruktúry java sv-comp test repa (.yaml a verifier)
        - vlastný evaluátor
        - benchmarky závisia na nedeterministickom verifieri, takže testujeme kompilovateľnosť do c
        - hoci nekontrolujeme výsledok vykonania programu, keďže unit testy pokrývajú veľkú podmnožinu feature, ktoré sú v sv=compe, môžeme predpokladať, že tie programy budú ekvivalentné.
        - minimálne jedna tabuľka - počet benchmarkov, koľko sme zvládli, koľko nie.
            - tie, ktoré sme nezvládli, tak prečo.
            - merania časov - priemer, výkyvy (štatistika a iné radosti)

    - výhľad do budúcna / záver
        - limitácie môžu byť tu
        - plány čo ďalej - passy (ktoré, ako?), možno threading, keďže jbmc to podporuje
        - porovnanie výsledkov vykonávania programov v sv-comp


