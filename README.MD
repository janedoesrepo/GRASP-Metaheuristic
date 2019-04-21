Startpunkt der Implementation ist die Datei „main.py“.

main.py bildet den Versuchsaufbau ab und bezieht alle 320 Instanzen mit ein. In einem Durchlauf der Datei wird für jede Instanz eine Lösung mit den acht heuristischen Regeln sowie mit GRASP-5 und mit GRASP-10 berechnet. Anschließend sucht das Programm noch die beste Lösung BS für die Instanz und berechnet davon ausgehend die Average Relative Deviation ARD der einzelnen Lösungen.

Folgende  Ergebnisse werden ausgegeben:

•	jeweils in eine für jede Instanz individuelle Excel-Datei mit dem Namen „Instanz.xlsx“

•	eine Zusammenstellung aller Ergebnisse in „results.xlsx

dataimport.py liest eine .IN2-Datei aus.

heuristics.py berechnet eine Lösung für eine Instanz mit einer der acht vorgestellten heuristischen Regeln. Die heuristische Regel wird als Parameter „procedure“ in der Form „Strategie-Regel“, also bspw. „SH-max_ts“ angegeben.

grasp.py berechnet eine Lösung für eine Instanz mit dem Greedy Randomized Search Procedure. Außer des Vorranggraphen muss noch die gewünscht Anzahl an Iterationen sowie der Greedy-Faktor Alpha angegeben werden.

construction.py bildet die Konstruktionsphase der GRASP ab.

improvement.py bildet die lokale Suche der GRASP ab.

usecase.py gehört nicht zum eigentlichen Programm. Sie wird genutzt, um die Instanzen eines Fallbeispiels zu erstellen.
