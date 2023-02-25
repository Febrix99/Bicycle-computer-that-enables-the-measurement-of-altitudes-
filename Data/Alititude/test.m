% -- praca z danymi 
clc; clear;
%% Pobieranie danych z pliku tekstowego
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
naviki = flipud(macierz_naviki(:,3));

%% Wywoływanie konstruktowa 

object_2 = Testowa_klasa_2();
object   = Testowa_klasa_1(naviki, object_2);


