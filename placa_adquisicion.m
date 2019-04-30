s =  daq.createSession('ni');
s.DurationInSeconds =3 ;
s.Rate = 400000;
ch = {};
ch{1} = addAnalogInputChannel(s,'Dev8','ai1','Voltage');
set(ch{1},'InputType','SingleEnded')
[data,time] = startForeground(s);
a = [time,data];
csvwrite('sin_laser.csv',a)
