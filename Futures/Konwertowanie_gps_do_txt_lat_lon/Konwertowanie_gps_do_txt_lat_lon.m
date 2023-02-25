%- Skrypt s³ó¿ocy do konwertowania plików o formacie gps na pliki tekstowe
% z wspó³rzêdnymi geograficznymi 

% Otwieranie pliku
clc; clear;
fileID = fopen('gravel-po-lodzku-2022.gpx');

tic
% Inicjalizacja macierzy wynikowej
data = [];

% Pêtla przez ka¿dy wiersz pliku
while ~feof(fileID)
   % Odczytywanie wiersza z pliku
   tline = fgetl(fileID);
   
   % Wyszukiwanie wspó³rzêdnych geograficznych i wysokoœci
   latIndex = strfind(tline, 'lat=');
   lonIndex = strfind(tline, 'lon=');
   
   %- Uwaga na przysz³oœæ, w zale¿noœci od formatu pliku trzeba zmieniæ
   %wartoœci le zanków bierzemy pod uwage 
   
   % Jeœli wiersz zawiera wspó³rzêdne geograficzne dodaj je do macierzy
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

