set terminal png enhanced font  "Helvitica, 14" size 700,450
set output 'mscClassFreq.png'
set style data histogram
set xlabel font "Helvitica, 10"
set ylabel font "Helvitica, 10"
set xlabel 'Anzahl MSC Klassen'
set ylabel 'Anzahl Publikationen'
set style fill solid 0.75 border -1
set boxwidth 0.8
set xtics rotate by -45
set noborder
unset key
set ytics out nomirror
set xtics out nomirror
set xtics font "Helvitica, 10"
set ytics font "Helvitica, 10"
plot 'msc_class_freqs' using 2:xticlabels(1) lc rgb '#1161d9' notitle with boxes
