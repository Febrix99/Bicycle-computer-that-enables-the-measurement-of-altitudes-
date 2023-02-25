%% -- praca z danymi 
clc; clear;

%- Tworzenie struktry z danymi 
dane = dir('Dane_nowe_2'); dane = dane(3:end); %Tu podaje scieżkę do folderu z plikami 


for k = 1:1:max(size(dane))
    path = horzcat('Dane_nowe_2/',dane(k).name);
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
    altitude = macierz(:,1);
    speed = macierz(:,2);
    
    %-- Wywołanie konstruktora 
    DataTab(k) = MyData_nowe(altitude,speed);
    
 
    
end

