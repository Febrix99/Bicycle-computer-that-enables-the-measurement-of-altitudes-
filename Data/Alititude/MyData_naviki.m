%%-- Tworzenie klasy 

classdef MyData_naviki
    
    properties
        Altitude_1
        Altitude_2   
    end 
    properties (Dependent)
        avg_Altitude_1
        avg_Altitude_2
        avg_dif_Altitude
        plotter

    end    
    methods
        %-- Konstruktor 
        function thisMyData_naviki = MyData_naviki(pomiar, naviki)
            
            thisMyData_naviki.Altitude_1 = pomiar;
            thisMyData_naviki.Altitude_2 = naviki;
        end 
        
        %-- Średnia wysokosc 1       
        function [avg_Altitude_1] = get.avg_Altitude_1(MyData_naviki)
            
            avg_Altitude_1 = MyData_naviki.object.multiple(mean(MyData_naviki.Altitude_1));
            
        end    
        
        %-- Średnia wysokosc 2       
        function avg_Altitude_2 = get.avg_Altitude_2(MyData_naviki)
            
            avg_Altitude_2 = mean(MyData_naviki.Altitude_2);
         
        end      
        
        %--  Różnica wysokości     
        function avg_dif_Altitude = get.avg_dif_Altitude(MyData_naviki)
            
            avg_dif_Altitude =   mean(MyData_naviki.Altitude_1)- mean(MyData_naviki.Altitude_2);
         
        end    
     

        
        %-- Wykresy danych       
        function plotter = get.plotter(MyData_naviki)
            %- Dziedzina 
            x = 1:1:max(size(MyData_naviki.Altitude_1)); % Tyle x ile pomiarów 
            x_2 = 1:1:max(size(MyData_naviki.Altitude_2)); % Tyle x ile pomiarów 
            %- Wysokosc      

            y1 = MyData_naviki.Altitude_1;
            plot(x,y1, 'g','LineWidth',2);
            set(gca,'FontSize',17)
            title('Wysokość n.p.m','FontSize',20,'FontWeight','bold'); 
            xlabel('Nr pomiaru','FontSize',20,'FontWeight','bold'); ylabel('[m]','FontSize',20,'FontWeight','bold');   grid on ;

            hold on 
            y2 = MyData_naviki.Altitude_2;
            plot(x_2,y2, 'r','LineWidth',2);         


            lgd = legend('Dane pomiarowe','Dane wczytane z mapy Google','FontSize',20,'Location','northwest');
            title(lgd,'Powrównanie zebranych danych')
            hold off 
        end 
             
    end
end