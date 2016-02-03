Map = csvread('map.csv', 1, 0);
bush = Map(Map(:,1)==1, :);
hole = Map(Map(:,1)==2, :);
tree = Map(Map(:,1)==3, :);
size(tree)
figure
hold on
plot(bush(:,2), bush(:,3), 'r.', 'MarkerSize', 18)
plot(hole(:,2), hole(:,3), 'g.', 'MarkerSize', 18)
plot(tree(:,2), tree(:,3), 'b.', 'MarkerSize', 18)
legend('Bush','Hole','Tree')
xlabel('X-Coordinate')
ylabel('Y-Coordinate')
hold off
%%
data_new = csvread('phase1.csv', 1, 0);
data = [data; data_new];
%data = data(1:100,:);
latitude = data(:,1);
longitude = data(:,2);

% hist(longitude, 1000)
% %plot(latitude, longitude, 'r.')
%generate = @(v) linspace(min(v), max(v), floor((max(v)-min(v))*1));
index = @(i, v) floor(round((v(i)-min(v))/(max(v)-min(v)))*floor((max(v)-min(v))*1));
y = linspace(0,600,300);
x = linspace(0,800,400);
size(y)
[X,Y]=meshgrid(x,y);
Z = zeros(size(X));
miny = min(latitude);
maxy = max(latitude);
ny = length(y);
minx = min(longitude);
maxx = max(longitude);
nx = length(x);
for i=1:length(latitude)
    y = max(floor((latitude(i)-miny)/(maxy-miny)*ny), 1);
    x = max(floor((longitude(i)-minx)/(maxx-minx)*nx), 1);
    if Z(y,x) < 100
        Z(y,x) = Z(y,x)+1;
    end
end
mesh(X,Y,Z)
colormap(hot)
%%
data = csvread('phase1.csv', 1, 0);
%data = data(1:1000,:);
amount = data(:,2);
m = min(amount);
amount = amount-m;
% data = data(1000:2000,:);
%data = data(2000:3000,:);
% data = data(3000:4000,:);
hold on
plot (data(:,1), data(:,2), 'r')
plot (data(:,1), data(:,3), 'b')
x = 1:1000;
%plot (x, 10*sin(x/150)+30, 'g')
x=[0.28 0.28];
y=[0.5 0.55];
annotation('arrow',x,y)

%%
figure
alpha=0:pi/50:2*pi;%??[0,2*pi]
R=0.5;%??
x=R*cos(alpha);
y=R*sin(alpha);
plot(x,y,'-')
axis([-.2 4 -2 0]) 
axis equal

%%
figure
hold on 
data = csvread('phase1.csv', 1, 0);
size(data)
split = [[1:250]; ...
    [251:500];  ...
    [501:750];  ...
    [751:1000];  ...
    [1001:1250];  ...
    [1251:1500]; ...
    [1501:1750]; ...
    [1751:2000]; ...
    [2001:2250]; ...
    [2251:2500]];
for i = 1:10
amount1 = mean(data(split(i,:),1));
amount2 = mean(data(split(i,:),2));
height = amount2/(amount1+amount2);
rec1 = [i-1 0 1 height];
rec2 = [i-1 height 1 1-height];

rate = amount2/(amount1+amount2)
x = [i-1 i i i-1];
y1 = [0 0 height height];
y2 = [height height 1 1];
rectangle('Position',rec1, 'LineWidth',1.5,'LineStyle','-');
rectangle('Position',rec2, 'LineWidth',1.5,'LineStyle','-');
fill(x, y1, [230/255, 123/255, 123/255])

fill(x, y2, [175/255, 210/255, 227/255])
axis([0 10 0 1])
%axis off
ylabel('Relatvie Amount')
set(gca,'XTick',0:1:10)
set(gca,'XTickLabel', [0:500:5000])
end

%%
data = csvread('phase1.csv', 1, 0);
data = data(1000:2000,:);
amount = data(:,2);
energy = data(:,3);
ticks = data(:,1);

a = 6;

amount = (amount + a*mean(amount)) / (a+1);
energy = (energy + a*mean(energy)) / (a+1);
plot(ticks, amount-20, 'r');
hold on
plot(ticks, energy+10, 'b');
set(gca,'XTickLabel', [4000:100:5000])
xlabel('Time Ticks')
ylabel('Value')
legend('Prey Amount', 'Energy Level')




