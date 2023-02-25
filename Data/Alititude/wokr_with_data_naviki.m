% -- praca z danymi 
%- W celu zobaczenia wykresów wejdź w strukturę DataTab
clc; clear;
%- Tworzenie struktry z danymi 
dane = dir('Data_Altitude'); %Tu podaje scieżkę do folderu z plikami 
dane = dane(3:end);


% -- Wczytanie danych z nawigacji
path = horzcat('Data_Altitude/',dane(2).name);
[idl , kom] = fopen(path);
if(idl <0) % Jeżeli jest błąd z odczytu 
    disp(kom);
end

%- sprawdzenie długości listy 
[A, count] = fscanf(idl, '%f ');
count;
fclose(idl);
A = A';
%- przeskalowanie wektora na macierz 
macierz_naviki = zeros(count/3, 3);
for i = 1:1:count/3
    for j = 1:1:3
        macierz_naviki(i,j)= A(1,(3*(i-1))+j);
    end
end

% - Pobieranie danych z macierzy 
naviki = macierz_naviki(:,3);
naviki_inv = flipud(naviki);


% -- Wczytanie danych z jazdy testowej 
path = horzcat('Data_Altitude/',dane(1).name);
[idl , kom] = fopen(path);
if(idl <0) % Jeżeli jest błąd z odczytu 
    disp(kom);
end

%- sprawdzenie długości listy 
[A, count] = fscanf(idl, '%f ');
count;
fclose(idl);
A = A';
%- przeskalowanie wektora na macierz 
macierz = zeros(count/2, 2);
for i = 1:1:count/2
    for j = 1:1:2
        macierz(i,j)= A(1,(2*(i-1))+j);
    end
end
% - Pobieranie danych z macierzy 
pomiar = macierz(:,1);
dlugosc_pomiaru = max(size(pomiar)); %- Sprawdzam długość 
dlugosc_naviki = max(size(naviki_inv));
skala = dlugosc_pomiaru/dlugosc_naviki;
re_size_naviki = zeros(dlugosc_pomiaru,0);
n = 0;
odliczanie = 0;
mnoznik = 1;
% - przeskalowanie macierzy pomiarów do odpowiedniej długości 
while n < dlugosc_pomiaru
    if odliczanie > skala
        odliczanie = odliczanie -skala ;
        mnoznik = mnoznik +1;
    end
    re_size_naviki = [re_size_naviki;  naviki_inv(mnoznik)];

    odliczanie = odliczanie + 1;
    n = n+1;
end
re_size_naviki_offset = re_size_naviki + 47.32;
% -- Wywołanie konstruktora 
DataTab.Off_Set = MyData_naviki(pomiar,re_size_naviki_offset);
DataTab.No_Off_Set = MyData_naviki(pomiar,re_size_naviki);   




