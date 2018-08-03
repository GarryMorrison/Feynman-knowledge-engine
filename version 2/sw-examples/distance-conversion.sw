to-km |km: *> #=> |_self>
to-km |m: *> #=> |km:> __ round[3] divide-by[1000] extract-value |_self>
to-km |miles: *> #=> |km:> __ round[3] times-by[1.60934] extract-value |_self>

to-m |km: *> #=> |m:> __ round[3] times-by[1000] extract-value |_self>
to-m |m: *> #=> |_self>
to-m |miles: *> #=> |m:> __ round[3] times-by[1609.34] extract-value |_self>

to-miles |km: *> #=> |miles:> __ round[3] divide-by[1.60934] extract-value |_self>
to-miles |m: *> #=> |miles:> __ round[3] divide-by[1609.34] extract-value |_self>
to-miles |miles: *> #=> |_self>

