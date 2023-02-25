%- Skrypcik sprawdzjacy róznice pomiędzy linearyzacją a prawidłową metodą liniową mierzeniem
%dystansu pomiedzy 2 punktami GPS 
clc; clear;
format long

lat1 = 51.8192337;
lon1 = 19.623996;

lat2 =51.8193337;
lon2 =19.624500;

delta = 0.000005;
lat1_vector = linspace(lat1, lat1, 10000);
lon1_vector = linspace(lon1, lon1, 10000);

lat2_vector = linspace(lat2, lat2 + (1000-1)*delta, 10000);
lon2_vector = linspace(lon2, lon2 + (1000-1)*delta, 10000);




 sfer_vector = haversine(lat1_vector, lon1_vector, lat2_vector, lon2_vector);
 linear_vector = linear(lat1_vector, lon1_vector, lat2_vector, lon2_vector);
 error_bezwzgledny = sfer_vector -linear_vector;
 error_wzgledny = 100*error_bezwzgledny./sfer_vector;
 plot(sfer_vector, error_bezwzgledny, 'linewidth' , 2)
 grid on 
 hold on 
 plot(sfer_vector, error_wzgledny,'linewidth' , 2)
 legend('Błąd bezwzgledny', 'Błąd wzgledny','FontSize',20)
 set(gca,'FontSize',17)
 title('Błąd pomiedzy aproksymacja liniową a odległością sferyczną ','FontSize',20,'FontWeight','bold'); 
 xlabel('Odleglosc 2 punktow od siebie [m]','FontSize',20,'FontWeight','bold'); ylabel('Bład [m]','FontSize',20,'FontWeight','bold'); 
function [distance] = linear(lat1, lon1, lat2, lon2)
    % Długość promienia ziemi w metrach 
    R = 6371200;
    
    % Convert degrees to radians
    lat1 = deg2rad(lat1);
    lon1 = deg2rad(lon1);
    lat2 = deg2rad(lat2);
    lon2 = deg2rad(lon2);


    %- Obliczanie wartości pierwszego punktu
    x1 =R * cos(lon1).*cos(lat1);
    y1 =R * sin(lon1).*cos(lat1);
    z1 = R * sin(lat1);
    
    %- Obliczanie wartości drugiego punktu
    x2 = R * cos(lon2).*cos(lat2);
    y2 = R * sin(lon2).*cos(lat2);
    z2 = R * sin(lat2);
    
    delta_x = x2 - x1;
    delta_y = y2 - y1;
    delta_z = z2 - z1;
    
    distance = sqrt(delta_x.^2 + delta_y.^2 + delta_z.^2);
end
 
function [distance] = haversine(lat1, lon1, lat2, lon2)
    % Convert degrees to radians
    lat1 = deg2rad(lat1);
    lat2 = deg2rad(lat2);
    lon1 = deg2rad(lon1);
    lon2 = deg2rad(lon2);

    % Compute the difference between the two points
    delta_lat = lat2 - lat1;
    delta_lon = lon2 - lon1;

    % Apply the haversine formula
    a = sin(delta_lat/2).^2 + cos(lat1).* cos(lat2).* sin(delta_lon/2).^2;
    c = 2 * atan2(sqrt(a), sqrt(1-a));

    % Earth's average radius (in kilometers)
    R = 6371200;

    % Compute the distance between the two points
    distance = R * c;

end
