%- Skrypt s��ocy do konwertowania plik�w o formacie gps na pliki tekstowe
% z wsp�rz�dnymi geograficznymi 

% Otwieranie pliku
clc; clear;
fileID = fopen('gravel-po-lodzku-2022.gpx');

tic
% Inicjalizacja macierzy wynikowej
data = [];

% P�tla przez ka�dy wiersz pliku
while ~feof(fileID)
   % Odczytywanie wiersza z pliku
   tline = fgetl(fileID);
   
   % Wyszukiwanie wsp�rz�dnych geograficznych i wysoko�ci
   latIndex = strfind(tline, 'lat=');
   lonIndex = strfind(tline, 'lon=');
   
   %- Uwaga na przysz�o��, w zale�no�ci od formatu pliku trzeba zmieni�
   %warto�ci le zank�w bierzemy pod uwage 
   
   % Je�li wiersz zawiera wsp�rz�dne geograficzne dodaj je do macierzy
   if ~isempty(latIndex) && ~isempty(lonIndex)
       lat = str2double(tline(latIndex+5:lonIndex-3));
       lon = str2double(tline(lonIndex+5:end-2));
       data = [data; lat lon ];
   end
end

% Zamykanie pliku
fclose(fileID);

% Eksportowanie macierzy do pliku tekstowego
dlmwrite('gps.txt', data, 'precision', 12);

toc

