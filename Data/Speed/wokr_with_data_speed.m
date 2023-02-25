% -- praca z danymi 
clc; clear;
%- Tworzenie struktry z danymi 
dane = dir('Data_speed'); %Tu podaje scieżkę do folderu z plikami 
dane = dane(3:end);

% -- Wczytanie danych z jazdy testowej 
path = horzcat('Data_speed/',dane(1).name);
[idl , kom] = fopen(path);
if(idl <0) % Jeżeli jest błąd z odczytu 
    disp(kom);
end

[macierz, count] = fscanf(idl, '%f ');
fclose(idl);

% -- Wczytanie danych z GPS
path1 = horzcat('Data_speed/',dane(2).name);
[idl , kom] = fopen(path1);
if(idl <0) % Jeżeli jest błąd z odczytu 
    disp(kom);
end

[m_fake, count1] = fscanf(idl, '%f ');
fclose(idl);

X = 0.1;
for i=1:1:max(size(m_fake))
   a =  m_fake(i);
   if a >20
       if mod(i,10) == 0
           X = randi(5)/10;
       end
       
       m_fake(i) = m_fake(i)+X;
       
   end
    
    
    
end
diff = m_fake-macierz ;
x = 1:1:max(size(diff));
plot(x,diff)
% -- Wywołanie konstruktora 
DataTab = MyData_speed(macierz,m_fake);
    
    


