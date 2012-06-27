set terminal png enhanced font  "Helvitica, 14" size 700,450
set output 'keyWordFreq.png'
set style data histogram
set xlabel font "Helvitica, 10"
set ylabel font "Helvitica, 10"
set xlabel 'Anzahl Keywords'
set ylabel 'Anzahl Publikationen'
set style fill solid 0.75 border -1
set xtics rotate by -45
set noborder
unset key
set ytics out nomirror
set xtics out nomirror
set xtics font "Helvitica, 10"
set ytics font "Helvitica, 10"
plot 'keyword_freqs' using 2:xticlabels(1) lc rgb '#1161d9' notitle with boxes