%%-- Tworzenie klasy 

classdef MyData_speed
    
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
        function thisMyData_speed = MyData_speed(pomiar, naviki)
            

            thisMyData_speed.Altitude_1 = pomiar;
            thisMyData_speed.Altitude_2 = naviki;
            
        end 
        

    
        %-- Średnia wysokosc 1       
        function avg_Altitude_1 = get.avg_Altitude_1(MyData_speed)
            
            avg_Altitude_1 = mean(MyData_speed.Altitude_1);
         
        end    
        
        %-- Średnia wysokosc 2       
        function avg_Altitude_2 = get.avg_Altitude_2(MyData_speed)
            
            avg_Altitude_2 = mean(MyData_speed.Altitude_2);
         
        end      
        
        %--  Różnica wysokości     
        function avg_dif_Altitude = get.avg_dif_Altitude(MyData_speed)
            
            avg_dif_Altitude =   mean(MyData_speed.Altitude_1)- mean(MyData_speed.Altitude_2);
         
        end    
     

        
        %-- Wykresy danych       
        function plotter = get.plotter(MyData_speed)
            %- Dziedzina 
            x = 1:1:max(size(MyData_speed.Altitude_1)); % Tyle x ile pomiarów 
            x_2 = 1:1:max(size(MyData_speed.Altitude_2)); % Tyle x ile pomiarów 
            %- Wysokosc      

            y1 = MyData_speed.Altitude_1;
            plot(x,y1, 'g','LineWidth',2);
            set(gca,'FontSize',17)
            title('Prędkość chwilowa','FontSize',20,'FontWeight','bold'); 
            xlabel('Nr pomiaru','FontSize',20,'FontWeight','bold'); ylabel('[Km/h]','FontSize',20,'FontWeight','bold');   grid on ;

            hold on 
            y2 = MyData_speed.Altitude_2;
            plot(x_2,y2, 'r','LineWidth',2);         


            lgd = legend('Dane pomiarowe','Dane wczytane z GPS','FontSize',20,'Location','north');
            title(lgd,'Powrównanie zebranych danych')
            hold off 
        end 
             
    end
end