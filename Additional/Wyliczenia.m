% % ok, zacznijmy 

hold on;
grid on ;
obwod_kola = 2.155;
x = linspace(2,60,2000);


for i=1:10
     k = 1;
     y =  i*obwod_kola*3.6./x;
     plot(x,y)
end
for i=1:length(x)
     gorna_granica(i)=  1.2;
end
for i=1:length(x)
     dolna_granica(i)=  1;
end

plot (x,gorna_granica,'r', 'LineWidth',1.2)
plot (x,dolna_granica,'r', 'LineWidth',1)
xlabel('Prędkość [Km/h]'), ylabel('Okres [s]'), title('Ilość impulsów'),
axis([0, 45, 0, 2.5])
